# Dataset Schema Changelog

All notable changes to the Dataset schema will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses [Calendar Versioning](https://calver.org/) (YY.MMDD).

## [26.0615] - 2026-06-15

### Changed
- Source of truth switched to LinkML: `schema.json` and `context.jsonld` are now generated from `schema.linkml.yaml` via `scripts/generate.py` (replacing `field-definitions.yaml` + the legacy generator).
- Artifact shape changes inherited from LinkML's `gen-json-schema`: nested objects (`Person` for `creator`/`curator`, `Citation`, `SexDistribution`, `MeasurementTechnique`, `Activity`, `AccessConditions`, `EthicalApproval`) and every enum (`License`, `AgeCategory`, `MeasurementTechniqueType`, etc.) are factored into `$defs` and referenced via `$ref`; optional/recommended properties use explicit nullable unions (`"type": ["array", "null"]`, or `anyOf: [{$ref}, {"type": "null"}]` for optional objects/enums); `$schema` is now JSON Schema draft 2019-09 (was draft-07); `additionalProperties: false` on the inlined classes and `additionalProperties: true` at the root (so JSON-LD keys like `@type`/`@context` are permitted). The schema-level `description` now comes from the root class description.
- `language`'s `^[a-z]{2}$` pattern now sits on the array `items` (per-element) rather than on the array itself, where it had no effect.
- `description`'s `minLength: 10` is expressed as the equivalent `pattern: "^[\\s\\S]{10,}$"` (LinkML 1.8.5 has no string-min-length facet); the ≥10-character constraint is preserved.
- `version` updated to `26.0615`.

### Preserved
- JSON-LD fidelity is restored by a post-process step (`scripts/linkml_postprocess.py`): the published artifacts use the `schema:` prefix (not the internal `sdo:` generation workaround); the `@type` const (`schema:Dataset`) discoverability guard is re-injected; `@container: @set` is added to every multivalued term (and `@container: @list` to `age_range`); the reserved-slot `name` term maps to `schema:name` again; per-property `title`s are restored; and secondary mappings (e.g. `dc:identifier`, `dc:description`, `dc:rights`, `dc:subject`, `schema:editor`, BIDS/ClinicalTrials sample-size mappings) are surfaced in the context.
- All validation constraints are unchanged: identical `required` sets (root and nested), all enum permissible values (incl. the full SPDX `license` list), all patterns/formats, `keywords` `minItems: 1`, `age_range` `minItems/maxItems: 2`, and numeric `minimum`s. `creator`/`curator` inner mappings (`schema:email`, `schema:identifier` for ORCID, `schema:affiliation`) and `pretty_name`'s HuggingFace mapping are retained.

### Note
- The redundant `equivalentProperty` annotation is intentionally dropped from `schema.json`; the same property→IRI mappings live in `context.jsonld`, the canonical location.
- `dataset/examples/demo-dataset.json`: `sex_distribution.non_binary` changed to the modeled `other` key (nested objects are now closed; `other` is the schema's field for non-binary/other gender).

### Added
- A validation `pattern` (`^\S+@\S+\.\S+$`) on the shared `Person.email` (used by both `creator` and `curator`).
- Per-field `examples` restored on ~12 fields (`creator`, `sex_distribution`, `inclusion_criteria`/`exclusion_criteria`, `measurement_technique`, etc.) so the docs Overview renders them.
- `dataset/schema.linkml.yaml` as the LinkML source of truth.
- `dataset/versions/v26.0615/` snapshot for consumer pinning.

### Fixed
- `Person` is shared by `creator` and `curator`; its sub-field descriptions are now generic ("Full name of the person", "Email address") so they read correctly under both roles.
- `sex_distribution` requirement restored to `recommended`.

## [26.0610] - 2026-06-10

### Changed
- `schema.json` and `context.jsonld` are now regenerated from `field-definitions.yaml`, restored as the single source of truth. The generator was repaired so its output matches the published artifacts (it previously emitted an empty `required`, `"type"` instead of `const` on `@type`, `"type": "enum"` on enum fields, and put `enum` on array properties instead of their `items`).
- `$id` and `version` updated to `26.0610`.

### Added
- Descriptions for `curator` and `sex_distribution` sub-properties, plus `format`/`pattern` constraints on `curator.email`/`curator.orcid` (matching `creator`).
- Explicit `items` typing for the `activity` sub-arrays (`measurements`, `conditions`, `measures`, `constructs`).
- `dataset/versions/v26.0610/` snapshot for consumer pinning.

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
