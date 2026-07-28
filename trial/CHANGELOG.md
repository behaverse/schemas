# Changelog — Behaverse Trial Schema

All notable changes to the trial schema are documented here. CalVer `vYY.MMDD`.

## [26.0729] - 2026-07-29

*(Dated 26.0729 because the 26.0728 slot was already published and snapshots are immutable.)*

### Added

- **Every table now publishes its documentation `slug` and `docs_url`** in `field-definitions.json`. Downstream renderers previously each reimplemented the CamelCase→kebab-case slug rule to build "Full reference →" links; the two copies (in `behaverse/data-model`'s `build_spec.py` and this repo's docs generator) were character-identical by luck, and a change to the URL scheme here would have 404'd every outbound link silently. The answer is now published rather than guessed.

### Changed

- **`Studyflow` is now the first table.** It is the run log every other table references through `runtime_id`, so it reads first — outermost scope inward — and no table is introduced before the entity it points at. Consumers render tables in the order this file lists them.

## [26.0728] - 2026-07-28

*(Dated 26.0728 because the 26.0727 slot was published and snapshotted the same day, and
snapshots are immutable.)*

### Added

- **Questionnaire guidance moved into the schema**, migrated from the `behaverse/data-model`
  questionnaire guide where it had been maintained separately (and had drifted — that page
  documented a `trial_id` column that does not exist here). Field notes added to
  `Response.stimulus_index`, `stimulus_description`, `stimulus_onset`, `option_id`,
  `option_source`, `response_description`, `response_option_index`, `response_numeric`,
  `score`, and `Option.onset`. Because the guidance is a property of the fields rather than of
  the task of building a dataset, it now travels with the field definitions and appears on both
  documentation sites automatically.
  - The `option_onset` guidance from that guide was reattached to **`Option.onset`**: there is
    no `option_onset` field in `Response`, so the note had no valid home as written.
  - **The `response_numeric` / `score` distinction is now stated on both fields, as a
    `.warning`** — the single most consequential item in that guide, and previously recorded
    only on the data-model site. `response_numeric` is the raw answer, independent of the
    question; `score` is the value the experimenter assigns to it in context. Collapsing them
    into one column leaves a reader unable to distinguish raw answers, option positions, and
    reverse-coded values.
- **Note severity convention** (`.warning` / `.important` / `.tip` markers at the start of a
  note) documented in `CONTRIBUTING.md` and used here for the first time in this family. Kept
  as a string prefix rather than a structured field so that the shape of
  `field-definitions.json` — consumed by another repository's generator — stays unchanged.

### Fixed

- Four field descriptions linked to `/spec/general/2-dataset-cards.qmd`, a legacy site path the
  data-model site had been rewriting at build time as a stopgap; they now point at the
  published dataset-card page.

## [26.0727] - 2026-07-27

### Breaking

- **Every table now carries `runtime_id`** (required), identifying the activity run — one execution of one activity by one agent, with restarts counted separately. Until now a table's identity depended on the folder it sat in: `response_id` was unique only within a file, so concatenating all `stimulus.csv` files in a dataset silently mixed agents. The dataset-wide key is now the pair (`runtime_id`, `response_id`) — and correspondingly (`runtime_id`, `stimulus_id`), (`runtime_id`, `option_id`), etc. Every affected `range_description` was reworded from "of the same agent/session/activity/attempt" to "within the same `runtime_id`". Folder layout is unchanged, but it is no longer load-bearing: it becomes an export view of data that carries its own scope.
- **`TaskParameter` renamed to `TrialParameter`**, and its payload restructured (below). The name `TaskParameter` is now used for a different, coarser-grained table (also below).
- **Parameter payload restructured** in both parameter tables: `index_1` / `index_2` / `value` are replaced by `parameter_dimensions` (semicolon-separated axis names, e.g. `state;action`), `parameter_index` (the matching coordinates, e.g. `1;2`), `value_numeric`, and `value_description`. Three fixes in one: values are no longer an untyped `any` (the `*_numeric` / `*_description` pairing already used for responses and outcomes keeps CSV columns typed); the arbitrary two-dimension cap is gone, so a transition tensor indexed by state, action, and next state is now expressible; and the index is self-describing, where previously nothing recorded that `index_1` meant "state".

### Added

- **`Studyflow` table** (15 fields) — the run log, shipped as `studyflow.csv` in the agent's folder, with one row per activity run: `runtime_id` (PK), the full scope (`agent_id`, `session_index`, `session_uuid`, `activity_index`, `instrument_id`, `timeline_id`, `attempt`, the two repetition counts), `status`, `abandon_reason`, `start_datetime`, `end_datetime`, and `anchor_datetime`. It resolves the schema's long-standing dangling reference to a "`Studyflow` table" and gives `studyflow.csv` a schema for the first time. It is the **realized run log**, distinct from the study-level BPMN plan modeled by the `studyflow` schema family.
  - **`RunStatusEnum`** (`initialized` · `in_progress` · `completed` · `abandoned`), derived from the event layer's lifecycle verbs. This makes "the last complete attempt" a filter plus a join instead of a reconstruction, and — decisively — makes a run that was abandoned before any trial finished representable at all: such a run produces no rows in any other table, so its `Studyflow` row is the only record that it happened.
- **`TaskParameter` table** (10 fields), rebuilt at the **activity-run** grain — values constant across one run but varying between runs and agents (a per-agent reward mapping, a per-group volatility level). Carries `runtime_id` plus `agent_id`, `session_index`, and `instrument_id` so the file names the activity it is about without a join. Joining it with `TrialParameter` on `runtime_id` reconstructs the full generative state in effect on any trial.
- **`Response.attempt`** (required) — the 1-based ordinal of the activity run within the session, which identifies a session that was interrupted and restarted. Files are no longer split by attempt, so this column is what separates several runs now sharing one file.
- **`Response.status`** (optional) — a copy of the run's status so trials from abandoned runs can be filtered without a join. `Studyflow` is authoritative; disagreement is a dataset error.
- **`TrialParameter.subtrial_index`** (optional) — for parameters realized at a specific stage of a staged trial.

### Changed

- `instrument_repetition` now states explicitly that it counts **this agent's own** prior completions across sessions — never completions across participants — and is distinct from `attempt`, which counts restarts within a session.

## [26.0722] - 2026-07-22

### Changed

- Field-description prose now says **agent(s)** wherever it said subject(s)/participant(s) (75 replacements across all tables), aligning the schema's wording with BDM naming Rule 6 ("use 'agent' to refer to the entity generating the response data"). Also reworded the `stop_signal` stimulus-role description to gender-neutral phrasing. No structural changes — field names, types, requirements, and ranges are untouched.

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
