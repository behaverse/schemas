# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""Generate published artifacts for the trial schema from field-definitions.yaml.

The trial model is multi-table, so (unlike the single-object dataset/catalog schemas) it
emits two artifacts from the one source of truth:

  - field-definitions.json  — the render artifact consumed by behaverse/data-model (summary
                              tables) and by the docs site. This is what BDM fetches.
  - schema.json             — a JSON Schema (Draft-07) validation contract: one definition
                              per table (columns -> JSON types, `required` from the field
                              requirement), plus a top-level object mapping each table to an
                              array of its rows.

Scope / limitations of schema.json: the YAML's `type` is coarse and `range` is free-text
prose, so this validates **types + required fields only** — it does not enforce enum values,
numeric ranges, or cross-table foreign keys. (context.jsonld is still a follow-up — the
trial fields carry no semantic `mappings` yet.) See trial/README.md.

Usage:
    uv run scripts/generate.py
    uv run scripts/generate.py --check   # dry run; exit 1 if any generated file is stale
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml  # type: ignore

TRIAL_DIR = Path(__file__).parent.parent

# Coarse trial field type -> JSON Schema type. Unknown/`any`/empty -> no type constraint.
_TYPE_MAP: dict[str, dict] = {
    "string": {"type": "string"},
    "url": {"type": "string", "format": "uri"},
    "integer": {"type": "integer"},
    "index": {"type": "integer"},
    "float": {"type": "number"},
    "boolean": {"type": "boolean"},
    "datetime": {"type": "string", "format": "date-time"},
    "enum": {"type": "string"},          # allowed values live in prose `range`, not structured
    "id": {"type": ["integer", "string"]},
    "PRIMARY KEY": {"type": ["integer", "string"]},
    "integer | string": {"type": ["integer", "string"]},
    "list[index]": {"type": "array", "items": {"type": "integer"}},
    "any": {},
}


def build_field_definitions(src: dict) -> dict:
    meta = src["schema_metadata"]
    return {
        "schema": "trial",
        "version": meta["version"],
        "namespace": meta["namespace"],
        "description": meta["description"],
        "tables": src["tables"],
    }


def _field_schema(field: dict) -> dict:
    prop = dict(_TYPE_MAP.get((field.get("type") or "").strip(), {}))
    if field.get("description"):
        prop["description"] = field["description"]
    if field.get("categories"):
        prop["category"] = field["categories"][0]
    return prop


def _table_schema(table: dict) -> dict:
    props = {f["name"]: _field_schema(f) for f in table["fields"]}
    required = [f["name"] for f in table["fields"] if f.get("requirement") == "required"]
    schema: dict = {"type": "object", "properties": props}
    if table.get("description"):
        schema["description"] = table["description"]
    if required:
        schema["required"] = required
    return schema


def build_json_schema(src: dict) -> dict:
    meta = src["schema_metadata"]
    definitions = {t["name"]: _table_schema(t) for t in src["tables"]}
    properties = {
        t["name"]: {
            "type": "array",
            "description": t.get("description", f"Rows of the {t['name']} table."),
            "items": {"$ref": f"#/definitions/{t['name']}"},
        }
        for t in src["tables"]
    }
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": f"{meta['namespace']}/v{meta['version']}/schema.json",
        "title": meta["name"],
        "description": meta["description"],
        "version": meta["version"],
        "type": "object",
        "properties": properties,
        "definitions": definitions,
    }


def _emit(target: Path, data: dict, check: bool) -> bool:
    """Write `data` as JSON to `target`. In check mode, report drift instead. Returns
    True if the file is up to date (or was written), False if stale in check mode."""
    rendered = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if check:
        if (target.read_text() if target.exists() else "") != rendered:
            print(f"stale: {target} would change — run without --check")
            return False
        print(f"up to date: {target}")
        return True
    target.write_text(rendered)
    print(f"✓ generated {target}")
    return True


def main() -> None:
    check = "--check" in sys.argv
    src = yaml.safe_load((TRIAL_DIR / "field-definitions.yaml").read_text())

    ok = _emit(TRIAL_DIR / "field-definitions.json", build_field_definitions(src), check)
    ok = _emit(TRIAL_DIR / "schema.json", build_json_schema(src), check) and ok

    if check and not ok:
        sys.exit(1)
    if not check:
        n_fields = sum(len(t["fields"]) for t in src["tables"])
        print(f"✓ {len(src['tables'])} tables, {n_fields} fields")


if __name__ == "__main__":
    main()
