# Dataset Schema Changelog

All notable changes to the Dataset schema will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses [Calendar Versioning](https://calver.org/) (YY.MMDD).

## [26.0605] - 2026-06-05

### Added
- Inner `creator`/`curator` object term mappings in `context.jsonld`: `email → schema:email`, `orcid → schema:identifier`, `affiliation → schema:affiliation`. Previously these structured-person fields fell through `@vocab` and expanded to the wrong (dataset-namespaced) IRIs.
- `dataset/versions/v25.1201/` snapshot of the prior release for consumer pinning.

### Changed
- `$id` updated to `https://behaverse.org/schemas/dataset/v26.0605/schema.json`.

## [25.1201] - 2025-12-01

### Added
- Initial dataset schema
- Renamed `status` to `requirement` for clarity
- Core properties: @context, id, name, title, description, etc.
- Task and variable definitions
