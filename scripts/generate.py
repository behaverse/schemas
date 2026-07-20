#!/usr/bin/env python3
"""Unified, SchemaView-driven generator: schema.json + context.jsonld from LinkML.

For each schema directory that has a `schema.linkml.yaml`, this:

  1. runs `gen-json-schema --no-metadata --inline` -> schema.json,
  2. runs `gen-jsonld-context` -> context.jsonld,
  3. applies the JSON-LD / discoverability post-process (scripts/linkml_postprocess.py),
  4. writes the two files (or, with --check, reports drift without writing).

It is deliberately generic — nothing here is catalog-specific. Schemas without a
`schema.linkml.yaml` are skipped (dataset/event are migrated later).

Usage:
    python scripts/generate.py            # regenerate committed artifacts
    python scripts/generate.py --check    # CI drift guard: exit 1 if any would change
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

from linkml_runtime import SchemaView

sys.path.insert(0, str(Path(__file__).resolve().parent))
from linkml_postprocess import postprocess_context, postprocess_schema  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Per-schema artifact config. Every schema with a schema.linkml.yaml emits schema.json;
# the flags below toggle the two optional render artifacts:
#   emits_context           -> context.jsonld (JSON-LD discoverability)
#   emits_field_definitions -> field-definitions.json (multi-table render artifact, via
#                              scripts/emit_field_definitions.py)
# trial carries no semantic mappings, so it deliberately emits NO context.jsonld.
# Dirs lacking schema.linkml.yaml are skipped (migrated later). bcsv is excluded entirely.
SCHEMAS: list[dict[str, Any]] = [
    {"name": "catalog", "emits_context": True, "emits_field_definitions": False},
    {"name": "dataset", "emits_context": True, "emits_field_definitions": False},
    {"name": "trial", "emits_context": False, "emits_field_definitions": True},
    {"name": "event", "emits_context": True, "emits_field_definitions": True},
    {"name": "timeseries", "emits_context": False, "emits_field_definitions": False},
]

LINKML_SRC = "schema.linkml.yaml"


def _run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stderr}"
        )
    return proc.stdout


def generate_schema(src: Path) -> Dict[str, Any]:
    """Return the post-processed schema.json dict for a LinkML source."""
    schema = json.loads(_run([
        "gen-json-schema", "--no-metadata", "--inline", str(src)
    ]))
    sv = SchemaView(str(src))
    return postprocess_schema(schema, sv)


def generate_context(src: Path) -> Dict[str, Any]:
    """Return the post-processed context.jsonld dict for a LinkML source."""
    context = json.loads(_run(["gen-jsonld-context", str(src)]))
    sv = SchemaView(str(src))
    return postprocess_context(context, sv)


def _emit_field_definitions(name: str, check: bool) -> bool:
    """Invoke the field-definitions.json emitter. Returns True on drift (check mode)."""
    cmd = [sys.executable, str(Path(__file__).resolve().parent / "emit_field_definitions.py"), name]
    if check:
        cmd.append("--check")
    return subprocess.run(cmd).returncode != 0


def _dumps(data: Dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def _write_or_check(data: Dict[str, Any], path: Path, check: bool) -> bool:
    """Write `data` to `path`. In check mode, only report whether it would change."""
    new = _dumps(data)
    if check:
        if not path.exists():
            print(f"  would create: {path.relative_to(ROOT)}")
            return True
        if path.read_text() != new:
            print(f"  would update: {path.relative_to(ROOT)}")
            return True
        return False
    path.write_text(new)
    print(f"  wrote: {path.relative_to(ROOT)}")
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="dry run: exit 1 if any committed artifact would change")
    args = ap.parse_args()

    drift = False
    processed = 0
    for cfg in SCHEMAS:
        name = cfg["name"]
        sdir = ROOT / name
        src = sdir / LINKML_SRC
        if not src.exists():
            continue
        processed += 1
        print(f"{name}:")
        # schema.json: every LinkML schema emits one (LinkML gen + post-process).
        drift |= _write_or_check(generate_schema(src), sdir / "schema.json", args.check)
        # context.jsonld: only schemas that publish semantic mappings (trial does not).
        if cfg["emits_context"]:
            drift |= _write_or_check(generate_context(src), sdir / "context.jsonld", args.check)
        # field-definitions.json: multi-table render artifact (trial/event).
        if cfg["emits_field_definitions"]:
            drift |= _emit_field_definitions(name, args.check)

    if processed == 0:
        print("no schemas with schema.linkml.yaml found")

    if args.check:
        if drift:
            print("\ndrift detected: committed artifacts differ from regeneration")
            return 1
        print("\nup to date: committed artifacts match regeneration")
    return 0


if __name__ == "__main__":
    sys.exit(main())
