# Catalog Schema Changelog

All notable changes to the Catalog schema will be documented in this file.

## [26.0615] - 2026-06-15

### Changed
- Source of truth switched to LinkML: `schema.json` and `context.jsonld` are now generated from `schema.linkml.yaml` via `scripts/generate.py` (replacing `field-definitions.yaml` + the legacy `scripts/schema_gen.py`).
- Artifact shape changes inherited from LinkML's `gen-json-schema`: the `Curator` sub-object is factored into `$defs/Curator` and referenced via `$ref`; optional/recommended properties use explicit nullable unions (e.g. `"type": ["array", "null"]`); `$schema` is now JSON Schema draft 2019-09 (was draft-07); `additionalProperties: false` on the inlined classes and `additionalProperties: true` at the root (so JSON-LD keys like `@type`/`@context` are permitted). The schema-level `description` now comes from the root class description.
- `version` updated to `26.0615`.

### Preserved
- JSON-LD fidelity is restored by a post-process step (`scripts/linkml_postprocess.py`): the published artifacts use the `schema:` prefix (not the internal `sdo:` generation workaround); the `@type` const (`schema:DataCatalog`) discoverability guard is re-injected; `@container: @set` is added to every multivalued term; the reserved-slot `name` term maps to `schema:name` again; per-property `title`s are restored; and secondary mappings (`dc:description`, `dcat:catalog`) are surfaced in the context.

### Note
- The redundant `equivalentProperty` annotation is intentionally dropped from `schema.json`; the same property→IRI mappings live in `context.jsonld`, the canonical location.

### Added
- `catalog/versions/v26.0615/` snapshot for consumer pinning.

## [26.0610] - 2026-06-10

### Changed
- `schema.json` and `context.jsonld` are now regenerated from `field-definitions.yaml`, restored as the single source of truth. The generator was repaired so its output matches the published artifacts (it previously emitted an empty `required`, `"type"` instead of `const` on `@type`, and an invalid context-level `@type`, so the files had been hand-edited and had drifted from the YAML).
- `$id` and `version` updated to `26.0610`.

### Added
- `catalogs` now also maps to `dcat:catalog` (alongside `schema:hasPart`).
- URL-valued array terms (`datasets`, `catalogs`) declare `@type: "@id"` in `context.jsonld` so their values expand as node references rather than string literals.
- `catalog/versions/v26.0610/` snapshot for consumer pinning.

## [26.0605] - 2026-06-05

### Breaking
- `pretty_name` predicate moved from `schema:name` to `dc:title` in `context.jsonld`, fixing a triple collision with the table-level `name` (both previously expanded to `schema:name`).

### Fixed
- Removed the invalid context-level `@type` keyword override (`"@type": "https://schema.org/DataCatalog"`), which caused spec-compliant JSON-LD processors to reject the context entirely (it never expanded). Assigning the `DataCatalog` type via the document data is planned as a follow-up.

### Added
- `@type` optional top-level property (`const: "schema:DataCatalog"`) for schema.org / Google Dataset Search discoverability; added to the bundled examples. Aligned the `pretty_name` `equivalentProperty` annotation with the context (`dc:title`).
- Inner `curator` object term mappings in `context.jsonld`: `email → schema:email`, `orcid → schema:identifier`, `affiliation → schema:affiliation`. Previously these fell through `@vocab` and expanded to the wrong (catalog-namespaced) IRIs.
- `catalog/versions/v26.0107/` snapshot of the prior release for consumer pinning.

### Changed
- `$id` updated to `https://behaverse.org/schemas/catalog/v26.0605/schema.json`.

## [26.0107] - 2026-01-07

### Changed
- Renamed schema from "collection" to "catalog" to align with Schema.org DataCatalog
- Changed type mapping from `schema:Collection` to `schema:DataCatalog`
- Renamed `related_collections` to `related_catalogs`
- Updated `datasets` property to map to `schema:dataset` (DataCatalog standard)
- Updated namespace from `collection` to `catalog`
- Added DCAT vocabulary reference

### Added
- New `catalogs` property for nested/child catalog references (hierarchical organization)
- DCAT namespace mapping in context.jsonld

## [25.1202] - 2025-12-02

### Added
- Initial collection schema (now renamed to catalog)
- Support for longitudinal and multi-task collections
