# Changelog — Behaverse Trial Schema

All notable changes to the trial schema are documented here. CalVer `vYY.MMDD`.

## [26.0721] - 2026-07-21

### Added

- **`Subtrial` table** (19 fields) — per-stage detail for trials composed of successive dependent stages, each with its own stimulus → response → outcome cycle (e.g. the two-step task). The trial row in `Response` remains THE unit and carries the trial-level (aggregate or final) response and evaluation; each `Subtrial` row is a miniature trial anatomy (`subtrial_index`, stimulus reference, response, response_time, evaluation, outcome), keyed by the parent trial, with optional `task_index` so the same mechanism serves compound/concurrent multitasking.
- **`TaskParameter` table** (6 fields) — per-trial ground-truth generative task parameters in long format (`trial_index` | `task_index` | `parameter` | `index_1` | `index_2` | `value`); serves simulation, parameter recovery, and engine calibration. Doctrine noted in-schema: generative state is not behavior, and must not be consumed as a predictor of the responses it generated.
- **`Response.subtrial_count`** (optional integer, derived) — number of stages; 1 for simple trials. Documented contrast: digit-span "3-5-7" = 1 subtrial with `response_count` 3; the two-step = 2 subtrials. `response_count` keeps its existing meaning.
- **`Response.response_type`** (optional enum — the schema's first structured LinkML enum): the form of the response act — `choice` · `rating` · `ranking` (select mode) · `production` · `motor` (generate mode). Orthogonal to `job_type` (membership test: varies while the job is fixed AND recurs across jobs; "recall" is a job, never a response_type). Declared even where derivable; the derivations serve as validation checks.

## [26.0720] - 2026-07-20

### Added

- **`Response.response_index`** (optional integer) — the 1-based ordinal position of the response within the subject's participation in the study, nested within subjects and never reset across sessions or activities (per the BDM indexing conventions). Distinct from `response_id` (table-scoped identifier in temporal order) and from `response_option_index` (which option was chosen). Optional: existing datasets can derive it; new pipelines should populate it.
- **`Response.session_uuid`** (optional string) — a globally unique identifier (UUID, RFC 9562) for the session, assigned by the recording engine. Complements `session_index` (a per-subject ordinal) and closes the second half of known issue D3. Deviation from D3's wording: the field is named `session_uuid`, **not** a re-typed `session_id` — reusing `session_id` with a new type and meaning immediately after the v26.0703 rename would silently break existing consumers. Event streams' `bdm:session_id` extension corresponds to this value.

### Fixed

- Notes under `option_source`, `expected_response_option_index`, and `response_option_index` wrote `response_index`/`expected_response_index` where they meant the option indices (`response_option_index`/`expected_response_option_index`). Because `response_index` names a **different** BDM concept — the ordinal position of a response in the indexing hierarchy, not which option was chosen — the notes now spell out the full names, and a new note on `response_option_index` states the distinction explicitly. Also removed a confusing parenthetical ("there is no Response table") and fixed "occured" → "occurred" in `Input.onset`.

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
