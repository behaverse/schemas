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

# All schemas the unified pipeline owns; dirs lacking schema.linkml.yaml are skipped.
SCHEMAS = ["catalog", "dataset", "trial", "event"]

LINKML_SRC = "schema.linkml.yaml"


def _run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stderr}"
        )
    return proc.stdout


def generate_artifacts(src: Path) -> tuple[Dict[str, Any], Dict[str, Any]]:
    """Return (schema_json, context_jsonld) dicts, post-processed, for a source."""
    schema = json.loads(_run([
        "gen-json-schema", "--no-metadata", "--inline", str(src)
    ]))
    context = json.loads(_run(["gen-jsonld-context", str(src)]))

    sv = SchemaView(str(src))
    schema = postprocess_schema(schema, sv)
    context = postprocess_context(context, sv)
    return schema, context


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
    for name in SCHEMAS:
        sdir = ROOT / name
        src = sdir / LINKML_SRC
        if not src.exists():
            continue
        processed += 1
        print(f"{name}:")
        schema, context = generate_artifacts(src)
        drift |= _write_or_check(schema, sdir / "schema.json", args.check)
        drift |= _write_or_check(context, sdir / "context.jsonld", args.check)

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
