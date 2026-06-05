#!/usr/bin/env python3
"""Generate the bcsv conformance fixture suite.

Each fixture lives in its own directory under ``positive/`` or ``negative/`` and
contains exactly three files:

* ``data.csv``     — the CSV payload.
* ``metadata.json`` — the paired bcsv metadata. For fixtures that test integrity,
                       this file's ``file_hash`` is computed automatically from the
                       generated CSV (rather than hard-coded).
* ``expected.json`` — the expected ``ValidationResult`` shape that any conforming
                       implementation of ``validate_bcsv`` must produce.

Run from the schema repo root::

    python bcsv/conformance/_generate.py

This overwrites existing fixtures with freshly-computed hashes. Don't edit
the .csv / .json files by hand — edit this script and regenerate.

The expected.json format is documented in conformance/README.md.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

CONFORMANCE_DIR = Path(__file__).resolve().parent
CONTEXT_URL = "https://behaverse.org/schemas/bcsv/context.jsonld"


@dataclass
class Fixture:
    name: str
    kind: Literal["positive", "negative"]
    csv: str | None  # None → fixture has no data.csv (e.g. FILE_NOT_FOUND case)
    metadata: dict[str, Any] | None  # None → fixture has no metadata.json
    expected: dict[str, Any]
    add_hash: bool = False  # if True, compute SHA-256 of csv and inject into metadata
    invalid_metadata_text: str | None = None  # write this raw text instead of JSON-serialised metadata


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _write_fixture(fx: Fixture) -> None:
    dir_path = CONFORMANCE_DIR / fx.kind / fx.name
    dir_path.mkdir(parents=True, exist_ok=True)
    # Clean any stale files left from previous runs.
    for child in dir_path.iterdir():
        child.unlink()

    if fx.csv is not None:
        (dir_path / "data.csv").write_text(fx.csv, encoding="utf-8")

    meta = dict(fx.metadata) if fx.metadata is not None else None
    if meta is not None and fx.add_hash:
        meta["file_hash"] = _sha256(fx.csv or "")

    if fx.invalid_metadata_text is not None:
        (dir_path / "metadata.json").write_text(fx.invalid_metadata_text, encoding="utf-8")
    elif meta is not None:
        (dir_path / "metadata.json").write_text(
            json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    (dir_path / "expected.json").write_text(
        json.dumps(fx.expected, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def _meta(columns: list[dict], **extra: Any) -> dict:
    meta: dict[str, Any] = {
        "@context": CONTEXT_URL,
        "url": "data.csv",
        "table_schema": {"columns": columns, **extra.pop("table_schema_extra", {})},
    }
    meta.update(extra)
    return meta


def _ok(warnings: list[dict] | None = None) -> dict:
    return {"valid": True, "errors": [], "warnings": warnings or []}


def _bad(errors: list[dict], warnings: list[dict] | None = None, **extra) -> dict:
    return {"valid": False, "errors": errors, "warnings": warnings or [], **extra}


# --- positive fixtures ----------------------------------------------------

POSITIVE: list[Fixture] = [
    Fixture(
        name="string",
        kind="positive",
        csv="name\nalice\nbob\ncharlie\n",
        metadata=_meta([{"name": "name", "datatype": "string"}]),
        expected=_ok(),
        add_hash=True,
    ),
    Fixture(
        name="integer",
        kind="positive",
        csv="n\n1\n2\n3\n",
        metadata=_meta([{"name": "n", "datatype": "integer"}]),
        expected=_ok(),
        add_hash=True,
    ),
    Fixture(
        name="number",
        kind="positive",
        csv="x\n1.5\n2.0\n3.25\n",
        metadata=_meta([{"name": "x", "datatype": "number"}]),
        expected=_ok(),
        add_hash=True,
    ),
    Fixture(
        name="boolean",
        kind="positive",
        csv="flag\ntrue\nfalse\ntrue\n",
        metadata=_meta([{"name": "flag", "datatype": "boolean"}]),
        expected=_ok(),
        add_hash=True,
    ),
    Fixture(
        name="date",
        kind="positive",
        csv="d\n2026-01-15\n2026-02-20\n2026-03-15\n",
        metadata=_meta([{"name": "d", "datatype": "date"}]),
        expected=_ok(),
        add_hash=True,
    ),
    Fixture(
        name="datetime",
        kind="positive",
        csv="ts\n2026-01-15T13:30:00\n2026-01-15T14:00:00\n2026-01-15T14:30:00\n",
        metadata=_meta([{"name": "ts", "datatype": "datetime"}]),
        expected=_ok(),
        add_hash=True,
    ),
    Fixture(
        name="time",
        kind="positive",
        csv="t\n13:30:00\n14:00:00\n14:30:00\n",
        metadata=_meta([{"name": "t", "datatype": "time"}]),
        expected=_ok(),
        add_hash=True,
    ),
    Fixture(
        name="categorical",
        kind="positive",
        csv="group\nA\nB\nA\nC\n",
        metadata=_meta([
            {"name": "group", "datatype": "categorical", "levels": ["A", "B", "C"]},
        ]),
        expected=_ok(),
        add_hash=True,
    ),
    Fixture(
        name="ordered",
        kind="positive",
        csv="severity\nmild\nsevere\nmoderate\n",
        metadata=_meta([
            {"name": "severity", "datatype": "ordered", "levels": ["mild", "moderate", "severe"]},
        ]),
        expected=_ok(),
        add_hash=True,
    ),
]


# --- negative fixtures ----------------------------------------------------

NEGATIVE: list[Fixture] = [
    Fixture(
        name="FILE_NOT_FOUND",
        kind="negative",
        csv=None,  # deliberately absent
        metadata=_meta([{"name": "x", "datatype": "integer"}]),
        expected=_bad([{"code": "FILE_NOT_FOUND", "location": "data.csv"}]),
    ),
    Fixture(
        name="METADATA_INVALID_JSON",
        kind="negative",
        csv="x\n1\n",
        metadata=None,
        invalid_metadata_text='{"this is": "not valid JSON", "trailing": ,}\n',
        expected=_bad([{"code": "METADATA_INVALID_JSON", "location": "metadata.json"}]),
    ),
    Fixture(
        name="SCHEMA_VIOLATION",
        kind="negative",
        csv="x\nA\nB\n",
        # categorical with no `levels` — schema's allOf forbids this. Scoped to schema
        # check only; the same broken metadata would *also* trigger LEVELS_REQUIRED in
        # the constraint stage (which has its own fixture), so we isolate here.
        metadata=_meta([{"name": "x", "datatype": "categorical"}]),
        expected=_bad(
            [{"code": "SCHEMA_VIOLATION", "location": "/table_schema/columns/0"}],
            validate_with={"check_constraints": False},
        ),
        add_hash=True,
    ),
    Fixture(
        name="HASH_MISMATCH",
        kind="negative",
        csv="x\n1\n2\n",
        metadata=_meta(
            [{"name": "x", "datatype": "integer"}],
            # Deliberately wrong hash (sha256 of "different content").
            file_hash="0000000000000000000000000000000000000000000000000000000000000000",
        ),
        expected=_bad([{"code": "HASH_MISMATCH", "location": "data.csv"}]),
    ),
    Fixture(
        name="HASH_ABSENT",
        kind="negative",
        csv="x\n1\n2\n",
        metadata=_meta([{"name": "x", "datatype": "integer"}]),  # no file_hash key
        expected=_ok(warnings=[{"code": "HASH_ABSENT", "location": "/file_hash"}]),
    ),
    Fixture(
        name="COLUMN_MISSING_IN_DATA",
        kind="negative",
        csv="a\n1\n",
        metadata=_meta([
            {"name": "a", "datatype": "integer"},
            {"name": "b", "datatype": "string"},  # not in CSV
        ]),
        expected=_bad([{"code": "COLUMN_MISSING_IN_DATA", "location": "b"}]),
        add_hash=True,
    ),
    Fixture(
        name="COLUMN_MISSING_IN_METADATA",
        kind="negative",
        csv="a,b\n1,x\n",
        metadata=_meta([{"name": "a", "datatype": "integer"}]),  # b not described
        expected=_bad([{"code": "COLUMN_MISSING_IN_METADATA", "location": "b"}]),
        add_hash=True,
    ),
    Fixture(
        name="COLUMN_ORDER_DIFFERS",
        kind="negative",
        csv="b,a\nx,1\n",  # metadata declares [a, b]
        metadata=_meta([
            {"name": "a", "datatype": "integer"},
            {"name": "b", "datatype": "string"},
        ]),
        expected=_ok(warnings=[{"code": "COLUMN_ORDER_DIFFERS", "location": None}]),
        add_hash=True,
    ),
    Fixture(
        name="LEVELS_REQUIRED",
        kind="negative",
        csv="g\nA\nB\n",
        metadata=_meta([{"name": "g", "datatype": "categorical"}]),  # no levels
        expected=_bad(
            [{"code": "LEVELS_REQUIRED", "location": "g"}],
            validate_with={"check_schema": False},
        ),
        add_hash=True,
    ),
    Fixture(
        name="LEVELS_FORBIDDEN",
        kind="negative",
        csv="n\n1\n2\n",
        metadata=_meta([
            {"name": "n", "datatype": "integer", "levels": ["a", "b"]},  # forbidden combo
        ]),
        expected=_bad(
            [{"code": "LEVELS_FORBIDDEN", "location": "n"}],
            validate_with={"check_schema": False},
        ),
        add_hash=True,
    ),
    Fixture(
        name="LEVEL_NOT_DECLARED",
        kind="negative",
        csv="g\nA\nC\nA\n",  # C not in declared levels
        metadata=_meta([
            {"name": "g", "datatype": "categorical", "levels": ["A", "B"]},
        ]),
        expected=_ok(warnings=[{"code": "LEVEL_NOT_DECLARED", "location": "g"}]),
        add_hash=True,
    ),
    Fixture(
        name="RANGE_VIOLATION",
        kind="negative",
        csv="age\n25\n200\n",  # 200 > 120
        metadata=_meta([
            {"name": "age", "datatype": "integer", "minimum": 0, "maximum": 120},
        ]),
        expected=_ok(warnings=[{"code": "RANGE_VIOLATION", "location": "age"}]),
        add_hash=True,
    ),
    Fixture(
        name="LENGTH_VIOLATION",
        kind="negative",
        csv="code\nAB\nABCDEFGH\n",  # 2 < min_length=3 and 8 > max_length=5
        metadata=_meta([
            {"name": "code", "datatype": "string", "min_length": 3, "max_length": 5},
        ]),
        expected=_ok(warnings=[
            {"code": "LENGTH_VIOLATION", "location": "code"},
            {"code": "LENGTH_VIOLATION", "location": "code"},
        ]),
        add_hash=True,
    ),
    Fixture(
        name="REQUIRED_VIOLATION",
        kind="negative",
        csv="id,_\n1,x\nNA,x\n",
        metadata=_meta([
            {"name": "id", "datatype": "integer", "required": True, "na_strings": ["NA"]},
            {"name": "_", "datatype": "string"},
        ]),
        expected=_ok(warnings=[{"code": "REQUIRED_VIOLATION", "location": "id"}]),
        add_hash=True,
    ),
    Fixture(
        name="COERCION_FAILED",
        kind="negative",
        csv="n\n1\nabc\n3\n",
        metadata=_meta([{"name": "n", "datatype": "integer"}]),
        expected=_ok(warnings=[{"code": "COERCION_FAILED", "location": "n"}]),
        add_hash=True,
    ),
    Fixture(
        name="PRIMARY_KEY_VIOLATION",
        kind="negative",
        csv="id\n1\n1\n2\n",
        metadata=_meta(
            [{"name": "id", "datatype": "integer"}],
            table_schema_extra={"primary_key": "id"},
        ),
        expected=_ok(warnings=[{"code": "PRIMARY_KEY_VIOLATION", "location": None}]),
        add_hash=True,
    ),
    Fixture(
        name="DIALECT_UNSUPPORTED",
        kind="negative",
        csv="x\n1\n",
        metadata=_meta(
            [{"name": "x", "datatype": "integer"}],
            dialect={"delimiter": ",", "quoteChar": '"'},  # quoteChar not honored in v0
        ),
        expected=_ok(warnings=[{"code": "DIALECT_UNSUPPORTED", "location": "/dialect"}]),
        add_hash=True,
    ),
]


def main() -> None:
    for fx in POSITIVE + NEGATIVE:
        _write_fixture(fx)
    print(f"Wrote {len(POSITIVE)} positive + {len(NEGATIVE)} negative fixtures to {CONFORMANCE_DIR}")


if __name__ == "__main__":
    main()
