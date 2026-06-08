# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""Generate field-definitions.json for the event schema from field-definitions.yaml.

The event schema is a single object (the event envelope) plus the canonical bdm: vocabulary.
This emits field-definitions.json — the render artifact consumed by behaverse/data-model and
the docs site. The validation contract (schema.json) and context.jsonld are maintained
alongside (relocated from the questionnaire_apps events schema).

Usage:
    uv run scripts/generate.py
    uv run scripts/generate.py --check
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml  # type: ignore

EVENT_DIR = Path(__file__).parent.parent


def build_field_definitions(src: dict) -> dict:
    meta = src["schema_metadata"]
    out = {
        "schema": "event",
        "version": meta["version"],
        "namespace": meta["namespace"],
        "description": meta["description"],
        "fields": src["fields"],
    }
    if "vocabularies" in src:
        out["vocabularies"] = src["vocabularies"]
    return out


def main() -> None:
    check = "--check" in sys.argv
    src = yaml.safe_load((EVENT_DIR / "field-definitions.yaml").read_text())
    rendered = json.dumps(build_field_definitions(src), indent=2, ensure_ascii=False) + "\n"

    target = EVENT_DIR / "field-definitions.json"
    if check:
        if (target.read_text() if target.exists() else "") != rendered:
            print(f"stale: {target} would change — run without --check")
            sys.exit(1)
        print(f"up to date: {target}")
        return

    target.write_text(rendered)
    src_yaml = yaml.safe_load((EVENT_DIR / "field-definitions.yaml").read_text())
    v = src_yaml.get("vocabularies", {})
    print(f"✓ generated {target} — {len(src['fields'])} envelope fields, "
          f"{len(v.get('verbs', []))} verbs, {len(v.get('object_types', []))} object types, "
          f"{len(v.get('actor_types', []))} actor types")


if __name__ == "__main__":
    main()
