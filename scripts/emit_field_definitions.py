#!/usr/bin/env python3
"""Reconstruct a schema's field-definitions.json render artifact from its LinkML source.

field-definitions.json is the contract consumed by behaverse/data-model and the docs site.
LinkML has no native emitter for it, so this reads the LinkML (including the annotations that
carry categories / range-prose / notes / label / bdm_type) and rebuilds the exact structure
produced by the legacy trial generate.py.

Encoding (see trial/schema.linkml.yaml):
  table  -> non-tree-root, non-abstract LinkML class
    name        <- class name
    label       <- class title       (optional)
    description <- class description (optional)
    notes       <- class annotations.notes  (list, optional)
  field  -> attribute
    categories  <- annotations.categories (list, optional, emitted FIRST when present)
    name        <- slot name
    type        <- annotations.bdm_type (verbatim original coarse type; may be null)
    requirement <- "required" if slot.required else "optional"
    description <- slot description (optional)
    range       <- annotations.range_description (free-text prose, optional)
    notes       <- annotations.notes (list, optional)

Top-level meta comes from the LinkML schema itself:
  schema    <- schema.name      (forced to "trial" via the LinkML `name`)
  version   <- schema.version
  namespace <- schema.id
  description <- schema.description

Usage: python scripts/emit_field_definitions.py SCHEMA_DIR   # e.g. trial  or  event
       python scripts/emit_field_definitions.py SCHEMA_DIR --check
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from linkml_runtime import SchemaView

ROOT = Path(__file__).resolve().parent.parent

# Sentinel distinguishing "annotation key absent" from "annotation value is null".
_MISSING = object()


def _ann(obj, key, default=_MISSING):
    """Return the value of annotation `key` on `obj`, or `default` if the key is absent.

    A present annotation whose value is JSON null round-trips through SchemaView as a
    present key with value ``None`` — so callers must use the ``_MISSING`` sentinel to
    detect genuine absence (some baseline fields carry an explicit ``"type": null``).
    """
    anns = obj.annotations or {}
    a = anns.get(key)
    if a is None:
        return default
    return a.value


def _field(slot) -> dict:
    """Rebuild one field object, with keys in baseline order and present only when set."""
    out: dict = {}

    cats = _ann(slot, "categories")
    if cats is not _MISSING:
        out["categories"] = cats

    out["name"] = slot.name

    # `type` is always present in the baseline (it may be JSON null for one field).
    bdm_type = _ann(slot, "bdm_type")
    out["type"] = None if bdm_type is _MISSING else bdm_type

    out["requirement"] = "required" if slot.required else "optional"

    if slot.description:
        out["description"] = slot.description

    rng = _ann(slot, "range_description")
    if rng is not _MISSING:
        out["range"] = rng

    notes = _ann(slot, "notes")
    if notes is not _MISSING:
        out["notes"] = notes

    return out


def build_trial(sv: SchemaView, meta: dict) -> dict:
    """Multi-table model: each non-root class -> a table; its attributes -> fields."""
    tables = []
    for cname in sv.all_classes():
        c = sv.get_class(cname)
        if c.tree_root or c.abstract:
            continue
        table: dict = {"name": c.name}
        if c.title:
            table["label"] = c.title
        if c.description:
            table["description"] = c.description
        tnotes = _ann(c, "notes")
        if tnotes is not _MISSING:
            table["notes"] = tnotes
        table["fields"] = [_field(a) for a in (c.attributes or {}).values()]
        tables.append(table)
    return {
        "schema": meta["schema"],
        "version": meta["version"],
        "namespace": meta["namespace"],
        "description": meta["description"],
        "tables": tables,
    }


def build_event(sv: SchemaView, meta: dict) -> dict:
    """Single-envelope model: the tree_root Event class -> a flat `fields` list."""
    envelope = None
    for cname in sv.all_classes():
        c = sv.get_class(cname)
        if c.tree_root:
            envelope = c
            break
    if envelope is None:
        raise SystemExit("event: no tree_root class found")
    fields = [_field(a) for a in (envelope.attributes or {}).values()]
    out: dict = {
        "schema": meta["schema"],
        "version": meta["version"],
        "namespace": meta["namespace"],
        "description": meta["description"],
        "fields": fields,
    }
    vocab = _ann(sv.schema, "vocabularies")
    if vocab is not _MISSING:
        out["vocabularies"] = vocab
    return out


def build(sdir: Path) -> dict:
    sv = SchemaView(str(sdir / "schema.linkml.yaml"))
    meta = {
        "schema": sv.schema.name,
        "version": sv.schema.version,
        "namespace": str(sv.schema.id),
        "description": sv.schema.description,
    }
    return build_event(sv, meta) if sdir.name == "event" else build_trial(sv, meta)


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--check"]
    check = "--check" in sys.argv
    if not args:
        print("usage: emit_field_definitions.py SCHEMA_DIR [--check]")
        return 2
    sdir = Path(args[0])
    if not sdir.is_absolute():
        sdir = ROOT / sdir

    data = build(sdir)
    rendered = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    target = sdir / "field-definitions.json"

    if check:
        current = target.read_text() if target.exists() else ""
        if current != rendered:
            print(f"stale: {target} would change — run without --check")
            return 1
        print(f"up to date: {target}")
        return 0

    target.write_text(rendered)
    print(f"✓ generated {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
