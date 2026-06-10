#!/usr/bin/env python3
"""Validate the JSON-Schema-based schemas and their bundled examples.

For each schema directory: assert `schema.json` is a well-formed schema (Draft-07 or
2020-12, chosen from its `$schema`), then validate every `examples/*.json` against it
(trial has no examples, so only well-formedness is checked). Custom annotation keywords
(e.g. `equivalentProperty`) are ignored by the validator, as are string formats
(uri/date/email) — we check structure, matching the `ajv --strict=false` policy.

Exit non-zero on the first problem. studyflow is LinkML-based and is checked by
its own toolchain, so it is not included here.

Usage:  python scripts/validate_schemas.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ["bcsv", "catalog", "dataset", "trial", "event"]


def _validator_cls(schema: dict):
    """Pick the JSON Schema draft validator from the schema's `$schema` (default Draft-07)."""
    s = schema.get("$schema", "")
    if "2020-12" in s:
        return jsonschema.Draft202012Validator
    if "2019-09" in s:
        return jsonschema.Draft201909Validator
    return jsonschema.Draft7Validator


def main() -> int:
    failures: list[str] = []

    for name in SCHEMAS:
        sdir = ROOT / name
        schema_path = sdir / "schema.json"
        if not schema_path.exists():
            failures.append(f"{name}: schema.json not found")
            continue

        schema = json.loads(schema_path.read_text())
        vcls = _validator_cls(schema)
        try:
            vcls.check_schema(schema)
            print(f"✓ {name}/schema.json is a well-formed schema ({vcls.__name__})")
        except jsonschema.exceptions.SchemaError as e:
            failures.append(f"{name}/schema.json is not well-formed: {e.message}")
            continue

        validator = vcls(schema)
        for example in sorted((sdir / "examples").glob("*.json")):
            errors = sorted(validator.iter_errors(json.loads(example.read_text())),
                            key=lambda e: e.path)
            rel = example.relative_to(ROOT)
            if errors:
                for err in errors:
                    loc = "/".join(map(str, err.path)) or "<root>"
                    failures.append(f"{rel}: {loc}: {err.message}")
            else:
                print(f"✓ {rel} validates")

    if failures:
        print("\n✗ validation failed:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print("\n✓ all schemas well-formed and all examples valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
