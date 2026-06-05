# Dataset Schema Changelog

All notable changes to the Dataset schema will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses [Calendar Versioning](https://calver.org/) (YY.MMDD).

## [26.0605] - 2026-06-05

### Breaking
- `license` enum changed to valid SPDX-canonical casing (`CC-BY-4.0`, `CC-BY-SA-4.0`, `CC-BY-NC-4.0`, `CC-BY-NC-SA-4.0`, `CC0-1.0`, `MIT`, `Apache-2.0`, `GPL-3.0-only`, `other`). The previous lowercase tokens (`cc-by-4.0`, …) were not valid SPDX identifiers despite the "SPDX format" description; this aligns with the bcsv `license` convention.

### Added
- `@type` optional top-level property (`const: "schema:Dataset"`) for schema.org / Google Dataset Search discoverability; added to the bundled example.
- Inner `creator`/`curator` object term mappings in `context.jsonld`: `email → schema:email`, `orcid → schema:identifier`, `affiliation → schema:affiliation`. Previously these structured-person fields fell through `@vocab` and expanded to the wrong (dataset-namespaced) IRIs.
- `dataset/versions/v25.1201/` snapshot of the prior release for consumer pinning.

### Changed
- `$id` updated to `https://behaverse.org/schemas/dataset/v26.0605/schema.json`.

### Fixed
- `age_category`, `intervention_type`, and `measurement_technique[].response_type` had their `enum` on the array itself, so no value could ever validate (the array would have had to equal an enum string). Moved the `enum` onto `items`; these array-of-enum fields now validate correctly.
- `examples/demo-dataset.json` reconciled to the schema: `population_category` set to a single enum value (`healthy`) and `citation[].type` set to `primary` (`license` stays `CC-BY-4.0`, now valid under the corrected SPDX enum — see Breaking).

## [25.1201] - 2025-12-01

### Added
- Initial dataset schema
- Renamed `status` to `requirement` for clarity
- Core properties: @context, id, name, title, description, etc.
- Task and variable definitions
