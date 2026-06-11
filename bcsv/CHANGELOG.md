# BCSV Schema Changelog

All notable changes to the BCSV schema will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses [Calendar Versioning](https://calver.org/) (YY.MMDD).

## [26.0610] - 2026-06-10

### Changed

- **`bcsv` now expands to "Better CSV"** (was "Behaverse CSV") — the format is a general CSVW extension for R/Python data analysis, not Behaverse-specific. Updated `schema.json`'s `description`, the README, the root README, and the docs site. No structural change to the schema; the namespace and hosting (`behaverse.org/schemas/bcsv`) are unchanged.
- `$id` / `version` bumped to `v26.0610`.

## [26.0608] - 2026-06-08

### Breaking
- Table-level `description` is now **required** — a bcsv metadata document must describe what the table is about (aligns with catalog and dataset, which already require it). Conformance fixtures were regenerated to include a `description`; consumer packages should re-vendor the schema and fixtures together.

### Changed
- `$id` updated to `https://behaverse.org/schemas/bcsv/v26.0608/schema.json`.
- `README.md` current version updated to v26.0608.

## [26.0605] - 2026-06-05

### Added
- `@type` optional top-level property (`const: "csvw:Table"`) so a bcsv document can declare its JSON-LD node type (`rdf:type`); added to the bundled examples.
- `dialect` top-level property in `schema.json` documenting the CSV serialization hints bcsv honors in v0 (`delimiter`, `encoding`). Other CSVW dialect sub-properties pass through (`additionalProperties: true`) and are not interpreted by bcsv tooling; consumer tooling MAY emit a `DIALECT_UNSUPPORTED` warning for unhonored keys.
- "Dialect" subsection in `README.md` documenting the honored vs. pass-through stance.
- Consumer pinning guidance and a snapshot-immutability note in the `README.md` Versioning section.

### Changed
- `$id` updated to `https://behaverse.org/schemas/bcsv/v26.0605/schema.json`.
- `README.md` Versioning section now reports the correct current version (was stale at v26.0513).

## [26.0522] - 2026-05-22

### Breaking
- `primaryKey` renamed to `primary_key` in `schema.json` and `context.jsonld` (under `table_schema`). `foreignKeys` retained in CSVW casing — bcsv only renames CSVW properties it actively validates. The underlying JSON-LD IRI is unchanged (`csvw:primaryKey`). (H3)

### Added
- `levels` accepts numeric items (integers and numbers) in addition to strings — supports Likert-scale and other numerically-encoded ordinal data. (H1)
- `creator` accepts a single structured object (`{"name": ..., "orcid": ...}`) in addition to a string or array of objects. (H2)
- Explicit `license` term mapping in `context.jsonld` (`license → schema:license`); previously fell through `@vocab` and expanded to the wrong IRI. (H6)
- Property Reference entry for `license` in `README.md`. (H6)
- `bcsv/versions/v26.0513/` snapshot of the prior release for consumer pinning.

### Changed
- Type Mapping table in `README.md` now lists pandas nullable extension dtypes (`Int64`, `Float64`, `boolean`, `string`) — uniform missing-value handling via `pd.NA`. (H8)
- CSVW built-in datatype list in `README.md` trimmed to the bcsv-supported subset (`string, integer, number, boolean, date, datetime, time`); deferred types (`duration`, `binary`, `hexBinary`, `anyURI`, `json`, `xml`, `decimal`) documented as treated as `string` until mapped. (H9)
- `README.md` "Using bcsv for data processing" section replaced with a forward-looking placeholder; signature reference removed pending publication of the consumer R/Python packages. (H7)
- `bcsv/examples/measurements.json` updated to use `primary_key` (was `primaryKey`).
- `$id` updated to `https://behaverse.org/schemas/bcsv/v26.0522/schema.json`.

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
