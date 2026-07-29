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
    type        <- annotations.bdm_type (verbatim original coarse type; may be null);
                   when the annotation is absent, derived from the LinkML range
                   (enum -> "enum", otherwise the range name, "list of X" when
                   multivalued) so families without bdm_type annotations still
                   publish a usable Type column
    requirement <- "required" if slot.required else "optional"
    description <- slot description (optional)
    range       <- annotations.range_description (free-text prose, optional)
    values      <- the slot range's LinkML enum, as [{value, description?}, ...]
                   (only when the range is an enum; description omitted when unset)
    values_exhaustive <- false when the enum is annotated `exhaustive: false`
                   (the values document the known set without closing it), else true
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

import re
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
    # Induced slots (class_induced_slots) hand back a jsonasobj2 JsonObj rather than a
    # plain dict, and that type has no .get(); fall back to attribute access.
    a = anns.get(key) if hasattr(anns, "get") else getattr(anns, key, None)
    if a is None:
        return default
    return a.value


def _derived_type(slot, sv: SchemaView):
    """Fallback `type` for slots without a `bdm_type` annotation, from the LinkML range.

    enum -> "enum"; any other range (scalar type, custom type, class) -> its name;
    `any_of` branches joined with " or "; "list of X" when multivalued. An explicit
    `bdm_type` annotation always wins — this only fills the gap for families
    (studyflow, timeseries) that never annotated their slots.
    """
    def base(rng):
        if rng is None:
            return None
        rng = str(rng)
        return "enum" if rng in sv.all_enums() else rng

    if slot.any_of:
        t = " or ".join(p for p in (base(a.range) for a in slot.any_of) if p)
    else:
        t = base(slot.range)
    if t and slot.multivalued:
        t = f"list of {t}"
    return t or None


def _field(slot, sv: SchemaView, emit_values: bool = True) -> dict:
    """Rebuild one field object, with keys in baseline order and present only when set."""
    out: dict = {}

    cats = _ann(slot, "categories")
    if cats is not _MISSING:
        out["categories"] = cats

    out["name"] = slot.name

    # `type` is always present in the baseline. An explicit annotation wins verbatim
    # (including an authored null); an absent one falls back to the derived type.
    bdm_type = _ann(slot, "bdm_type")
    out["type"] = _derived_type(slot, sv) if bdm_type is _MISSING else bdm_type

    out["requirement"] = "required" if slot.required else "optional"

    if slot.description:
        out["description"] = slot.description

    rng = _ann(slot, "range_description")
    if rng is not _MISSING:
        out["range"] = rng

    enum_def = sv.all_enums().get(str(slot.range)) if (emit_values and slot.range) else None
    if enum_def is not None:
        values = []
        for pv in (enum_def.permissible_values or {}).values():
            v = {"value": str(pv.text)}
            if pv.description:
                v["description"] = pv.description
            values.append(v)
        out["values"] = values
        exhaustive = _ann(enum_def, "exhaustive")
        out["values_exhaustive"] = exhaustive is _MISSING or exhaustive not in (False, "false")

    notes = _ann(slot, "notes")
    if notes is not _MISSING:
        out["notes"] = notes

    return out


def _is_container(c, sv: SchemaView) -> bool:
    """True if a tree_root class is a pure container of other classes, not content itself.

    `trial`'s root (TrialData) only holds one multivalued list per table, so it is a
    container and must not be rendered as a table. `timeseries`'s root
    (TimeseriesMetadata) carries the sidecar's own fields, so it IS content and must be
    rendered. Distinguishing them by shape avoids a per-family flag.
    """
    attrs = list((c.attributes or {}).values())  # container test looks at declared attrs only
    if not attrs:
        return True
    classes = set(sv.all_classes())
    return all(a.multivalued and str(a.range) in classes for a in attrs)


def _slug(name: str) -> str:
    """Path/URL-safe slug for a table name (CamelCase -> kebab-case).

    Published per table in `field-definitions.json` so consumers do not have to
    reimplement it. `behaverse/data-model` and the gh-pages docs generator each kept
    their own copy of this function; if this repo's URL scheme ever changed, their
    outbound links would 404 silently. Must stay identical to the docs generator's
    `_slug()` while those copies still exist.
    """
    s = re.sub(r"(?<!^)(?=[A-Z])", "-", str(name))
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s or "item"


def build_trial(sv: SchemaView, meta: dict) -> dict:
    """Multi-table model: each non-root class -> a table; its attributes -> fields."""
    tables = []
    for cname in sv.all_classes():
        c = sv.get_class(cname)
        if c.abstract or (c.tree_root and _is_container(c, sv)):
            continue
        table: dict = {"name": c.name, "slug": _slug(c.name)}
        table["docs_url"] = f"https://behaverse.org/schemas/{meta['schema']}/{table['slug']}"
        if c.title:
            table["label"] = c.title
        if c.description:
            table["description"] = c.description
        tnotes = _ann(c, "notes")
        if tnotes is not _MISSING:
            table["notes"] = tnotes
        # Induced slots, not just inline `attributes`: a class may take its fields from a
        # parent (`is_a`) or a mixin, as the studyflow family does throughout. Reading only
        # `attributes` publishes those classes as empty sections.
        table["fields"] = [_field(a, sv) for a in sv.class_induced_slots(cname)]
        tables.append(table)
    return {
        "schema": meta["schema"],
        "version": meta["version"],
        "namespace": meta["namespace"],
        "description": meta["description"],
        "tables": tables,
    }


def _plain(obj):
    """Recursively convert jsonasobj2/LinkML structures into plain dict/list/scalars."""
    if hasattr(obj, "_as_dict"):
        return {k: _plain(v) for k, v in obj._as_dict.items()}
    if isinstance(obj, dict):
        return {k: _plain(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_plain(v) for v in obj]
    return obj


def build_event(sv: SchemaView, meta: dict) -> dict:
    """Single-envelope model: the concrete `Event` class -> a flat `fields` list.

    The render artifact's fields come specifically from the `Event` envelope class —
    NOT the abstract `EventDocument` tree_root and NOT `EventBatch`.
    """
    envelope = sv.get_class("Event")
    if envelope is None:
        raise SystemExit("event: no `Event` class found")
    # No per-field `values` here: the event artifact documents its value sets in the
    # top-level `vocabularies` key (richer than {value, description} — layers,
    # object_types), and duplicating the verb list per field would drift from it.
    fields = [_field(a, sv, emit_values=False) for a in (envelope.attributes or {}).values()]
    out: dict = {
        "schema": meta["schema"],
        "version": meta["version"],
        "namespace": meta["namespace"],
        "description": meta["description"],
        "fields": fields,
    }
    vocab = _ann(sv.schema, "vocabularies")
    if vocab is not _MISSING:
        out["vocabularies"] = _plain(vocab)
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
