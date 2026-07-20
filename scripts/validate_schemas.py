#!/usr/bin/env python3
"""Validate the JSON-Schema-based schemas and their bundled examples.

Four check families, all run by CI (validate-schemas.yml):

1. Schemas + examples — assert every `schema.json` is a well-formed schema (draft
   chosen from its `$schema`), then validate every `examples/*.json` against it
   (trial has no examples, so only well-formedness is checked). Custom annotation
   keywords (e.g. `equivalentProperty`) are ignored by the validator, as are string
   formats (uri/date/email) — we check structure, matching `ajv --strict=false`.
2. bcsv conformance fixtures — every positive fixture's metadata.json must validate
   against bcsv/schema.json; negative fixtures' metadata must match what their
   expected.json implies (schema-invalid for SCHEMA_VIOLATION-class fixtures,
   schema-valid for data-stage fixtures); embedded file_hash values must (mis)match
   data.csv as the fixture intends.
3. JSON-LD contexts — every context.jsonld (and vocabulary/terms.jsonld) must expand
   cleanly with pyld, with remote fetches forbidden; each example must survive
   expansion against its schema's local context.
4. LinkML enum consistency — on every enum-ranged slot in */schema.linkml.yaml, the
   slot's examples and `ifabsent: string(...)` default must be permissible values
   (the metamodel lint does not enforce either).

Exit non-zero listing every problem found. studyflow has no schema.json (LinkML,
consumed directly) so only checks 4 covers it.

Usage:  python scripts/validate_schemas.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ["bcsv", "catalog", "dataset", "trial", "event", "timeseries"]
CONTEXT_SCHEMAS = ["bcsv", "catalog", "dataset", "event"]  # trial ships no context.jsonld


def _validator_cls(schema: dict):
    """Pick the JSON Schema draft validator from the schema's `$schema` (default Draft-07)."""
    s = schema.get("$schema", "")
    if "2020-12" in s:
        return jsonschema.Draft202012Validator
    if "2019-09" in s:
        return jsonschema.Draft201909Validator
    return jsonschema.Draft7Validator


def check_bcsv_conformance(failures: list[str]) -> None:
    """Assert the conformance fixtures agree with bcsv/schema.json and their own expected.json."""
    schema = json.loads((ROOT / "bcsv" / "schema.json").read_text())
    validator = _validator_cls(schema)(schema)
    conf = ROOT / "bcsv" / "conformance"

    for fixture in sorted(p for kind in ("positive", "negative") for p in (conf / kind).iterdir() if p.is_dir()):
        rel = fixture.relative_to(ROOT)
        expected_path = fixture / "expected.json"
        if not expected_path.exists():
            failures.append(f"{rel}: missing expected.json")
            continue
        expected = json.loads(expected_path.read_text())
        codes = {e["code"] for e in expected.get("errors", [])}
        check_schema = expected.get("validate_with", {}).get("check_schema", True)

        meta_path = fixture / "metadata.json"
        meta = None
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text())
            except json.JSONDecodeError:
                if "METADATA_INVALID_JSON" not in codes:
                    failures.append(f"{rel}: metadata.json is unparseable but expected.json "
                                    f"does not declare METADATA_INVALID_JSON")
                continue
        if "METADATA_INVALID_JSON" in codes:
            failures.append(f"{rel}: expected METADATA_INVALID_JSON but metadata.json parsed cleanly")
            continue
        if meta is None:
            continue  # fixture without metadata (nothing schema-level to assert)

        schema_errors = list(validator.iter_errors(meta))
        if "SCHEMA_VIOLATION" in codes:
            if not schema_errors:
                failures.append(f"{rel}: expected a schema violation but metadata.json validates")
        elif check_schema and schema_errors:
            failures.append(f"{rel}: metadata.json unexpectedly fails schema validation: "
                            f"{schema_errors[0].message}")

        # file_hash integrity: must match data.csv unless the fixture tests a mismatch.
        data_path = fixture / "data.csv"
        if "file_hash" in meta and data_path.exists():
            actual = hashlib.sha256(data_path.read_bytes()).hexdigest()
            if "HASH_MISMATCH" in codes:
                if meta["file_hash"] == actual:
                    failures.append(f"{rel}: HASH_MISMATCH fixture's file_hash matches data.csv")
            elif meta["file_hash"] != actual:
                failures.append(f"{rel}: file_hash does not match sha256(data.csv)")


def check_jsonld_contexts(failures: list[str]) -> None:
    """Expand every JSON-LD context (and each example against it) with pyld; no network."""
    from pyld import jsonld

    def _no_network(url, options=None):  # any remote fetch is a bug: contexts must be self-contained
        raise jsonld.JsonLdError(f"remote context fetch attempted: {url}", "loadDocument")

    jsonld.set_document_loader(_no_network)

    for name in CONTEXT_SCHEMAS:
        ctx_doc = json.loads((ROOT / name / "context.jsonld").read_text())
        context = ctx_doc.get("@context")
        if context is None:
            failures.append(f"{name}/context.jsonld: no top-level @context key")
            continue
        probes = [(f"{name}/context.jsonld (minimal probe)", {"@context": context})]
        for example in sorted((ROOT / name / "examples").glob("*.json")):
            doc = json.loads(example.read_text())
            doc["@context"] = context  # replace the remote URL with the local context
            probes.append((str(example.relative_to(ROOT)), doc))
        for label, doc in probes:
            try:
                expanded = jsonld.expand(doc)
            except Exception as e:  # noqa: BLE001 — report any expansion failure
                failures.append(f"{label}: JSON-LD expansion failed: {e}")
                continue
            if "examples" in label and not expanded:
                failures.append(f"{label}: JSON-LD expansion produced no output "
                                f"(no term in the example is mapped by the context)")
        print(f"✓ {name}/context.jsonld expands (with {len(probes) - 1} example(s))")

    terms = json.loads((ROOT / "vocabulary" / "terms.jsonld").read_text())
    try:
        if not jsonld.expand(terms):
            failures.append("vocabulary/terms.jsonld: expansion produced no output")
        else:
            print("✓ vocabulary/terms.jsonld expands")
    except Exception as e:  # noqa: BLE001
        failures.append(f"vocabulary/terms.jsonld: JSON-LD expansion failed: {e}")


def check_linkml_enum_consistency(failures: list[str]) -> None:
    """Enum-ranged slots: examples and ifabsent defaults must be permissible values."""
    from linkml_runtime.utils.schemaview import SchemaView

    ifabsent_re = re.compile(r"^string\((.+)\)$")
    for path in sorted(ROOT.glob("*/schema.linkml.yaml")):
        sv = SchemaView(str(path))
        enums = sv.all_enums()
        rel = path.relative_to(ROOT)
        for slot in sv.all_slots().values():
            if slot.range not in enums:
                continue
            allowed = set(enums[slot.range].permissible_values.keys())
            for ex in slot.examples or []:
                val = getattr(ex, "value", None)
                if val is not None and val not in allowed:
                    failures.append(f"{rel}: slot '{slot.name}' example {val!r} is not a "
                                    f"permissible value of enum {slot.range}")
            if slot.ifabsent:
                m = ifabsent_re.match(str(slot.ifabsent))
                if m and m.group(1) not in allowed:
                    failures.append(f"{rel}: slot '{slot.name}' default {m.group(1)!r} is not a "
                                    f"permissible value of enum {slot.range}")


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

    for check, label in [
        (check_bcsv_conformance, "bcsv conformance fixtures agree with schema.json + expected.json"),
        (check_jsonld_contexts, "JSON-LD contexts expand"),
        (check_linkml_enum_consistency, "LinkML enum examples/defaults are permissible values"),
    ]:
        before = len(failures)
        check(failures)
        if len(failures) == before:
            print(f"✓ {label}")

    if failures:
        print("\n✗ validation failed:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print("\n✓ all schemas well-formed; examples, conformance fixtures, JSON-LD contexts, "
          "and LinkML enum usage all valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
