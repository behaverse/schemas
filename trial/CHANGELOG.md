# Changelog — Behaverse Trial Schema

All notable changes to the trial schema are documented here. CalVer `vYY.MMDD`.

## [26.0608] - 2026-06-08

### Added

- Initial relocation of the trial tables from `behaverse/data-model` into `behaverse/schemas`.
- `field-definitions.yaml` (source of truth) and generated `field-definitions.json` for the 7 published tables — Response, Stimulus, Option, Input, StimulusComponent, OptionComponent, Instrument (161 fields total).
- `schema.json` — a generated JSON Schema (Draft-07) validation contract: one definition per table (columns → JSON types, `required` from each field's requirement) and a top-level object mapping each table to an array of its rows. Validates **types + required fields only** — enum values, numeric ranges, and cross-table foreign keys are not enforced (the source `type`/`range` are coarse / free-text prose).
- `scripts/generate.py` to regenerate `field-definitions.json` **and `schema.json`** from the source.

### Changed

- Re-keyed fields to the schemas-repo convention: `variable_name` → `name`, `data_type` → `type`, `required` (bool) → `requirement` (`required` / `optional`).
- Stripped Quarto/Bootstrap markup from descriptions and notes (table references such as the `Stimulus` table are now plain backticked names); dropped `.tip` / `.important` / `.warning` callout-level markers (text retained).

### Notes

- Published as-is; known data issues (D1 `stimulus_id` typing, D3 `session_id`/`session_index`, D5 `agent` → `actor`) are tracked as follow-ups, not applied in this relocation.
- `context.jsonld` is not yet generated — the trial fields carry no semantic `mappings` yet.
