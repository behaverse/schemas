# Changelog — Behaverse Trial Schema

All notable changes to the trial schema are documented here. CalVer `vYY.MMDD`.

## [26.0703] - 2026-07-03

### Breaking

- `Response.session_id` renamed to **`session_index`** — the field holds the 1-based order of the session within a subject (its own description and range already said "index"), and the table's notes explicitly state `session_id` is not used in this table.
- `Stimulus.trial_id` renamed to **`trial_index`** — it refers to `trial_index` in the `Response` table; the `Option` table already used `trial_index` for the same reference, and the event schema's vocabulary also uses `bdm:trial_index`. One reference, one name.

### Fixed

- Signal-detection definitions in `evaluation_label`: a `miss` and a `fa` (false alarm) are now correctly described as **incorrect** responses (previously both said "correctly responded").
- `Input.response_id` description was a copy-paste of an index definition; it now describes the foreign-key reference to `Response.response_id`.
- `Response.trial_index` note said "BDM uses `trial_id` instead"; it now says `trial_index`, matching the actual field name.
- Typos: "auditoy-visual", "interger", "occured", "pojected_trial_index", "opiton_index_in_source", "DS_FOWARD_TEST", "more then one", "an trial", "multitasking_type" (for `multitask_type`), unbalanced parentheses in `session_index`/`activity_index` descriptions, and "the second session" in the `activity_index` description (now "the second activity").

## [26.0608] - 2026-06-08

### Added

- Initial relocation of the trial tables from `behaverse/data-model` into `behaverse/schemas`.
- `schema.linkml.yaml` (LinkML source of truth) and generated `field-definitions.json` for the 7 published tables — Response, Stimulus, Option, Input, StimulusComponent, OptionComponent, Instrument (161 fields total).
- `schema.json` — a generated JSON Schema (Draft-07) validation contract: one definition per table (columns → JSON types, `required` from each field's requirement) and a top-level object mapping each table to an array of its rows. Validates **types + required fields only** — enum values, numeric ranges, and cross-table foreign keys are not enforced (the source `type`/`range` are coarse / free-text prose).
- Both `field-definitions.json` and `schema.json` are regenerated from the LinkML source via the repo-wide `python scripts/generate.py`.

### Changed

- Re-keyed fields to the schemas-repo convention: `variable_name` → `name`, `data_type` → `type`, `required` (bool) → `requirement` (`required` / `optional`).
- Stripped Quarto/Bootstrap markup from descriptions and notes (table references such as the `Stimulus` table are now plain backticked names); dropped `.tip` / `.important` / `.warning` callout-level markers (text retained).

### Notes

- Published as-is; known data issues (D1 `stimulus_id` typing, D3 `session_id`/`session_index`, D5 `agent` → `actor`) are tracked as follow-ups, not applied in this relocation.
- No `context.jsonld` is emitted — the trial fields carry no semantic `mappings`.
