# Catalog Schema Changelog

All notable changes to the Catalog schema will be documented in this file.

## [26.0605] - 2026-06-05

### Breaking
- `pretty_name` predicate moved from `schema:name` to `dc:title` in `context.jsonld`, fixing a triple collision with the table-level `name` (both previously expanded to `schema:name`).

### Fixed
- Removed the invalid context-level `@type` keyword override (`"@type": "https://schema.org/DataCatalog"`), which caused spec-compliant JSON-LD processors to reject the context entirely (it never expanded). Assigning the `DataCatalog` type via the document data is planned as a follow-up.

### Added
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
