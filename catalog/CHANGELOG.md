# Catalog Schema Changelog

All notable changes to the Catalog schema will be documented in this file.

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
