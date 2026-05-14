# BCSV Schema Changelog

All notable changes to the BCSV schema will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses [Calendar Versioning](https://calver.org/) (YY.MMDD).

## [26.0513] - 2026-05-13

### Breaking
- Renamed schema directory and short name: `bcsvw` → `bcsv`. URI base changed: `https://behaverse.org/schemas/bcsvw#` → `https://behaverse.org/schemas/bcsv#`. (Includes the directory rename committed in 0af64bd.)
- `pretty_name` predicate moved from `schema:name` to `dc:title` (fixes triple collision with table-level `name`).
- Removed camelCase aliases `minLength`/`maxLength` from `context.jsonld` and `schema.json`. Use snake_case `min_length`/`max_length`.
- `format` is now forbidden when `datatype` is `categorical` or `ordered`. Use `levels` to enumerate.
- `@context` is now a required top-level property.
- `file_hash` must match the SHA-256 hex regex `^[a-f0-9]{64}$`.
- `levels` is forbidden outside `categorical`/`ordered`; `minimum`/`maximum` are forbidden outside numeric datatypes; `min_length`/`max_length` are forbidden outside string.
- `$id` now includes the version (`https://behaverse.org/schemas/bcsv/v26.0513/schema.json`), matching catalog/dataset convention.

### Added
- Inner `creator` object term mappings: `email → schema:email`, `orcid → schema:identifier`, `affiliation → schema:affiliation`.
- Explicit datatype-value term mappings: `string → xsd:string`, `integer → xsd:integer`, `number → xsd:double`, `boolean → xsd:boolean`, `date → xsd:date`, `datetime → xsd:dateTime`, `time → xsd:time`, `categorical → bcsv:categorical`, `ordered → bcsv:ordered`. Fixes incorrect `bcsv:string` (etc.) expansion under `@vocab`.
- `bcsv/versions/v25.1201/` snapshot of the prior schema and context for consumer pinning.

### Changed
- README value-proposition section replaced with gap-analysis table + non-goals.
- README adds CSVW pass-through property note.
- README adds callout explaining table-level vs column-level `name`.

## [25.1201] - 2025-12-01

### Added
- Initial schema with license property (SPDX format)
- Renamed `tableSchema` to `table_schema` for consistency
- Core properties: @context, name, url, title, description, etc.
- Column definitions with metadata (name, title, datatype, required, etc.)
