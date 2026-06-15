#!/usr/bin/env python3
"""Post-process LinkML generator output for JSON-LD / discoverability fidelity.

The LinkML generators (`gen-json-schema`, `gen-jsonld-context`) produce faithful
*validation* artifacts but drop a handful of things the legacy hand-rolled
generator emitted and that downstream consumers (Google Dataset Search, JSON-LD
processors) rely on. This module re-applies those, driven generically from a
`linkml_runtime.SchemaView` so the same logic works for every schema:

  a. Publish the `schema:` prefix, not the internal `sdo:` workaround label.
  b. Inject the `@type` const for the tree_root class (schema.org node type).
  c. Add `@container: @set` (or `@list` for numeric ranges) to multivalued terms.
  d. Fix the self-referential `@id` LinkML emits for reserved slots (e.g. `name`).
  e. Surface `exact_mappings` (secondary IRIs) in the published context.
  f. Add a per-property `title` to schema.json (snake_case -> Title Case).

The `sdo`-prefix workaround exists only to dodge a `schema:` vs `linkml:types`
collision at generation time; it must never leak into published artifacts.
"""
from __future__ import annotations

from typing import Any, Dict

from linkml_runtime import SchemaView

# The internal prefix label used in the LinkML source to dodge the
# `schema:` (https) vs linkml:types `schema:` (http) collision, and the
# published label/URI it must be normalized back to.
SDO_INTERNAL_PREFIX = "sdo"
SDO_PUBLISHED_PREFIX = "schema"
SDO_NAMESPACE = "https://schema.org/"

_NUMERIC_RANGES = {"integer", "float", "double", "decimal"}


def _title_case(name: str) -> str:
    """`pretty_name` -> `Pretty Name` (mirrors legacy auto-titling)."""
    return name.replace("_", " ").title()


def _to_published_curie(curie_or_uri: str) -> str:
    """Rewrite an `sdo:...` CURIE to `schema:...`; leave everything else alone."""
    if curie_or_uri.startswith(SDO_INTERNAL_PREFIX + ":"):
        return SDO_PUBLISHED_PREFIX + ":" + curie_or_uri[len(SDO_INTERNAL_PREFIX) + 1:]
    return curie_or_uri


def _slot_uri_published(sv: SchemaView, slot) -> str:
    """slot_uri in published (`schema:`) CURIE form, or a sensible default."""
    uri = slot.slot_uri
    if not uri:
        # LinkML falls back to default_prefix:slot_name when slot_uri is unset.
        return uri
    return _to_published_curie(uri)


def postprocess_schema(schema: Dict[str, Any], sv: SchemaView) -> Dict[str, Any]:
    """Apply schema.json transforms (a-type-const, f-titles, a-sdo-normalize, g-versioned-$id)."""
    tree_root = _tree_root_class(sv)

    # (g) Versioned, self-identifying `$id` (VERSIONING.md: each release bumps `$id`,
    # and snapshots under versions/vYY.MMDD/ must carry their own immutable identifier).
    # LinkML emits the bare schema `id`; restore the `.../vYY.MMDD/schema.json` form.
    schema_id = str(sv.schema.id).rstrip("/")
    if sv.schema.version:
        schema["$id"] = f"{schema_id}/v{sv.schema.version}/schema.json"

    # (f) Per-property titles on every `properties` block (top-level + $defs).
    for props in _iter_property_blocks(schema):
        for pname, pschema in props.items():
            if pname.startswith("@"):
                continue
            if isinstance(pschema, dict) and "title" not in pschema:
                pschema["title"] = _title_case(pname)

    # (b) @type const for the tree_root class, in the published `schema:` form.
    # Skipped for an abstract tree_root: an abstract umbrella (e.g. event's
    # EventDocument = Event | EventBatch) is not itself a concrete node type, so a
    # single top-level @type const would be wrong. Concrete roots are unchanged.
    if tree_root is not None and not tree_root.abstract:
        class_uri = sv.get_uri(tree_root, expand=False)  # e.g. sdo:DataCatalog
        const = _to_published_curie(class_uri)
        # Inject into the top-level (root) properties block only.
        props = schema.get("properties")
        if isinstance(props, dict):
            type_entry = {
                "const": const,
                "title": "Type",
                "description": (
                    "JSON-LD node type (rdf:type) for schema.org / "
                    "Google Dataset Search discoverability."
                ),
            }
            # Place @type first for readability.
            schema["properties"] = {"@type": type_entry, **props}

    # (h) Abstract tree_root -> root `oneOf` over its concrete descendants.
    # gen-json-schema emits a bare permissive `type: object` root for an abstract
    # tree_root; replace its validation with a oneOf of the non-abstract descendant
    # `$defs` (e.g. Event, EventBatch), preserving $defs/$schema/$id/title/version.
    if tree_root is not None and tree_root.abstract:
        _abstract_root_to_oneof(schema, sv, tree_root)

    # (a) Normalize any lingering `sdo:` CURIE strings (e.g. const values) to `schema:`.
    _normalize_sdo_in_place(schema)

    return schema


def _abstract_root_to_oneof(schema: Dict[str, Any], sv: SchemaView, tree_root) -> None:
    """Rewrite the root validation to a oneOf over the abstract tree_root's concrete descendants.

    Driven generically from SchemaView: the concrete (non-abstract) descendants of the
    abstract tree_root become the `oneOf` branches, ordered to match class definition
    order. The structural inventory ($defs, $schema, $id, title, version, description) is
    preserved; the loose root `properties`/`type`/`required`/`additionalProperties` that
    gen-json-schema emitted for the empty umbrella class are removed.
    """
    descendants = {tree_root.name, *sv.class_descendants(tree_root.name)}
    concrete = [
        cname for cname in sv.all_classes()
        if cname in descendants and cname != tree_root.name
        and not sv.get_class(cname).abstract
    ]
    if not concrete:
        return
    for key in ("properties", "type", "required", "additionalProperties"):
        schema.pop(key, None)
    schema["oneOf"] = [{"$ref": f"#/$defs/{cname}"} for cname in concrete]


def _uses_sdo(sv: SchemaView) -> bool:
    """True iff the LinkML source actually declares the internal `sdo` prefix.

    The `sdo`->`schema` normalization is a workaround for one specific collision and
    must be a no-op for schemas that never use `sdo` (e.g. event, whose published
    context legitimately carries `schema: http://schema.org/`).
    """
    return SDO_INTERNAL_PREFIX in sv.namespaces()


def postprocess_context(context_doc: Dict[str, Any], sv: SchemaView) -> Dict[str, Any]:
    """Apply context.jsonld transforms (a-prefix, c-container, d-selfref, e-mappings)."""
    ctx = context_doc.get("@context", {})

    # Drop the generator's `comments` block: it carries a wall-clock
    # `generation_date` that would make every regeneration differ, defeating the
    # --check drift guard. It is pure provenance (not in the baseline anyway).
    context_doc.pop("comments", None)

    # (a) Rename the `sdo` prefix entry -> `schema`, and rewrite every `sdo:` CURIE.
    # Only when the source actually uses `sdo`; otherwise leave the context alone so
    # a schema that publishes its own `schema:` prefix (e.g. event) is not clobbered.
    if _uses_sdo(sv):
        if SDO_INTERNAL_PREFIX in ctx:
            del ctx[SDO_INTERNAL_PREFIX]
        ctx[SDO_PUBLISHED_PREFIX] = SDO_NAMESPACE
        for key, val in list(ctx.items()):
            if isinstance(val, str):
                ctx[key] = _to_published_curie(val)
            elif isinstance(val, dict) and "@id" in val and isinstance(val["@id"], str):
                val["@id"] = _to_published_curie(val["@id"])

    # Build a name->slot lookup once (induced slots of every class, plus all slots).
    slots_by_name = {s.name: s for s in sv.all_slots().values()}
    for cls in sv.all_classes().values():
        for s in sv.class_induced_slots(cls.name):
            slots_by_name.setdefault(s.name, s)

    for term, val in list(ctx.items()):
        if not isinstance(val, dict):
            continue
        slot = slots_by_name.get(term)

        # (d) Self-referential @id fix: LinkML emits `@id: <term>` for reserved
        # slots (e.g. `name`). Replace with the slot's published slot_uri.
        if val.get("@id") == term and slot is not None:
            pub = _slot_uri_published(sv, slot)
            if pub:
                val["@id"] = pub

        # (c) @container on multivalued slots: @list for numeric ranges, else @set.
        if slot is not None and slot.multivalued and "@container" not in val:
            val["@container"] = "@list" if slot.range in _NUMERIC_RANGES else "@set"

    # (e) Secondary mappings (exact_mappings) surfaced as additional context terms.
    _add_secondary_mappings(ctx, sv, slots_by_name)

    # (h) Deep-merge the schema-level `context_overrides` annotation (bespoke JSON-LD
    # constructs LinkML cannot generate from slots alone — e.g. objectType->@type,
    # @container:@list, extra prefixes, @type:@id terms). Applied last so it wins.
    overrides = _schema_annotation_json(sv, "context_overrides")
    if isinstance(overrides, dict):
        _deep_merge(ctx, overrides)

    context_doc["@context"] = ctx
    return context_doc


def _plain(obj):
    """Recursively convert LinkML/jsonasobj2 structures into plain dict/list/scalars."""
    # jsonasobj2 JsonObj exposes its items via _as_dict / iteration; detect by attr.
    if hasattr(obj, "_as_dict"):
        return {k: _plain(v) for k, v in obj._as_dict.items()}
    if isinstance(obj, dict):
        return {k: _plain(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_plain(v) for v in obj]
    return obj


def _schema_annotation_json(sv: SchemaView, key: str):
    """Return a schema-level annotation's value as a plain JSON-compatible structure.

    LinkML may surface the value as a jsonasobj2 `JsonObj`, a plain dict/list, or a
    raw JSON string; all are normalized to plain Python here.
    """
    anns = sv.schema.annotations or {}
    a = anns.get(key)
    if a is None:
        return None
    val = a.value
    if isinstance(val, str):
        try:
            import json as _json
            return _json.loads(val)
        except (ValueError, TypeError):
            return None
    return _plain(val)


def _deep_merge(base: Dict[str, Any], overlay: Dict[str, Any]) -> None:
    """Recursively merge `overlay` into `base` in place (overlay wins on conflicts)."""
    for k, v in overlay.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v


def _add_secondary_mappings(ctx, sv, slots_by_name) -> None:
    """Surface each slot's `exact_mappings` as an extra top-level context term.

    A JSON-LD term carries a single `@id`, so secondary IRIs cannot ride on the
    primary slot term. We instead (1) ensure the mapping's prefix is defined in
    the context (so the CURIE is resolvable) and (2) add a dedicated alias term
    so the secondary property is usable from instance documents. To avoid
    clobbering an existing prefix or slot term, the alias is keyed by the full
    CURIE (e.g. `dcterms:description`) when the bare local name collides; this is
    valid JSON-LD (the value is the same CURIE expanded), and otherwise by the
    bare local name.
    """
    ns = sv.namespaces()
    for slot in slots_by_name.values():
        for mapping in (slot.exact_mappings or []):
            mapping = _to_published_curie(mapping)
            if ":" not in mapping:
                continue
            prefix, local = mapping.split(":", 1)
            # (1) ensure the prefix is defined in the published context.
            if prefix not in ctx:
                expanded = str(ns.get(prefix)) if ns.get(prefix) else None
                if expanded:
                    ctx[prefix] = expanded
            # (2) add an alias term that does not collide with an existing
            #     prefix or slot/class term. Prefer the bare local name; fall
            #     back to the full CURIE key if it would clobber something.
            collides = (
                local in ctx  # existing term/prefix (e.g. `catalog` prefix)
                or local in slots_by_name  # existing slot term (e.g. `description`)
            )
            key = mapping if collides else local
            if key not in ctx:
                ctx[key] = {"@id": mapping}


def _tree_root_class(sv: SchemaView):
    for cls in sv.all_classes().values():
        if cls.tree_root:
            return cls
    return None


def _iter_property_blocks(schema: Dict[str, Any]):
    """Yield every `properties` dict in the schema (root + each $defs class)."""
    if isinstance(schema.get("properties"), dict):
        yield schema["properties"]
    for d in (schema.get("$defs") or {}).values():
        if isinstance(d, dict) and isinstance(d.get("properties"), dict):
            yield d["properties"]


def _normalize_sdo_in_place(obj: Any) -> None:
    """Rewrite any `sdo:...` string value to `schema:...` anywhere in the tree."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                obj[k] = _to_published_curie(v)
            else:
                _normalize_sdo_in_place(v)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, str):
                obj[i] = _to_published_curie(v)
            else:
                _normalize_sdo_in_place(v)
