# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""Generate published artifacts for the trial schema from field-definitions.yaml.

The trial model is multi-table, so (unlike the single-object dataset/catalog schemas) its
render contract is a `tables` document. This generates:

  - field-definitions.json  — the render artifact consumed by behaverse/data-model (summary
                              tables) and by the docs site. This is what BDM fetches.

Planned (follow-up, not yet emitted): schema.json (per-table JSON Schema for validation) and
context.jsonld. See trial/README.md.

Usage:
    uv run scripts/generate.py
    uv run scripts/generate.py --check   # dry run; exit 1 if field-definitions.json is stale
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml  # type: ignore

TRIAL_DIR = Path(__file__).parent.parent


def build_field_definitions(src: dict) -> dict:
    meta = src["schema_metadata"]
    return {
        "schema": "trial",
        "version": meta["version"],
        "namespace": meta["namespace"],
        "description": meta["description"],
        "tables": src["tables"],
    }


def main() -> None:
    check = "--check" in sys.argv
    src = yaml.safe_load((TRIAL_DIR / "field-definitions.yaml").read_text())
    out = build_field_definitions(src)
    rendered = json.dumps(out, indent=2, ensure_ascii=False) + "\n"

    target = TRIAL_DIR / "field-definitions.json"
    if check:
        current = target.read_text() if target.exists() else ""
        if current != rendered:
            print(f"stale: {target} would change — run without --check")
            sys.exit(1)
        print(f"up to date: {target}")
        return

    target.write_text(rendered)
    n_fields = sum(len(t["fields"]) for t in out["tables"])
    print(f"✓ generated {target} — {len(out['tables'])} tables, {n_fields} fields")


if __name__ == "__main__":
    main()
