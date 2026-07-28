# Agent prompt: bring `behaverse/data-model` in line with schemas v26.0727–v26.0728

_Copy everything below the line into a fresh agent session inside the `behaverse/data-model`
repository (the Quarto site behind https://behaverse.org/data-model/). Prepared 2026-07-27 by
the `behaverse/schemas` project. This supersedes the earlier hand-off prepared 2026-07-21 —
that one is obsolete: several of its items are now decided upstream, and the schema changed
substantially after it was written._

---

You are working in `behaverse/data-model`, the Quarto site publishing the human-facing
Behaverse Data Model. It is a **downstream consumer** of `behaverse/schemas`: `schemas.lock`
plus `scripts/build_spec.py` fetch each family's `field-definitions.json` (trial, event) and
the vocabulary's `terms.jsonld`, and generate the `/spec/trial/`, `/spec/event/`, and glossary
pages. Before changing anything, read `schemas.lock`, `scripts/build_spec.py`, this repo's
contribution conventions, and the upstream CHANGELOGs for **trial**, **event**, **timeseries**,
**vocabulary**, and **studyflow** (in the schemas repo, or at
`https://behaverse.org/schemas/<family>/CHANGELOG.md`). Remember that underscore-prefixed
`.qmd` files are unpublished drafts.

## Why: the schema layer changed shape

Since this site was last aligned, the trial family went from 7 tables to **11**, and — most
importantly — **data files stopped depending on their folder for identity**. In order:

- **trial v26.0720/0721** — `session_id` → `session_index` plus a new `session_uuid`;
  `response_index`; `Subtrial` and the first `TaskParameter` table; `response_type` enum.
- **event v26.0721** — `bdm:key_released` (25 verbs); `Attachment` formalized (required
  `type`/`contentType`/`url`, optional `sha256`/`length`/`description`, `url` resolved relative
  to the referencing file); **events at rest are NDJSON**, one `Event` per line, in the activity
  folder; `EventBatch` is the interchange shape only.
- **timeseries v26.0721/0727 (new family)** — sidecar metadata (`<payload>.timeseries.json`)
  beside a format-agnostic payload; channels are the primitive; now also carries `runtime_id`.
- **vocabulary v26.0721/0727** — new `time` scheme (`engine_seconds`, `anchor_datetime`, `t`);
  the **`bdm:` prefix now binds to `https://behaverse.org/schemas/vocabulary/`** everywhere (it
  used to be `…/data-model/vocab/` on this site); `anchor_datetime` is recorded **once per
  runtime instance**, not per session.
- **trial v26.0727 — the big one.** A new **`Studyflow` table** (the run log: one row per
  activity run, i.e. one execution of one activity by one agent, restarts counted separately),
  and **every table now carries `runtime_id`**. Local ids (`response_id`, `stimulus_id`, …) are
  unique only *within a run*, so the dataset-wide key is the pair `(runtime_id, response_id)`.
  `Response` also gained `attempt` and an optional `status`. `TaskParameter` was split by grain
  into `TrialParameter` (trial-varying) and a new activity-run-grained `TaskParameter`.
- **trial v26.0728** — questionnaire field guidance migrated *from this site* into the schema
  (see item 2), plus a note-severity convention.
- **studyflow v26.0728** — the family's first tagged release (was `25.1217.dev2`).

Items are ordered by priority. Regenerate generated pages rather than hand-editing them, verify
against the live artifacts, and record any deviation with a rationale.

### 1. Regenerate the spec pages, and update the pins

`schemas.lock` pins trial/event at v26.0608. Update the pins (or confirm the "track current"
path picks them up) and rebuild. Expected results to verify:

- `/spec/trial/` gains pages for **`Studyflow`**, **`Subtrial`**, **`TrialParameter`**, and
  **`TaskParameter`** — 11 tables in total. Check that the numbered-filename scheme
  (`1-response.qmd` … `7-instrument.qmd`) extends cleanly and the sidebar ordering is sane;
  `Studyflow` arguably belongs first, since it is the entity everything else references.
- The Response page shows `runtime_id`, `attempt`, `status`, `session_index`, `session_uuid`,
  `response_index`, `subtrial_count`, `response_type`.
- `/spec/event/` shows 25 verbs including `bdm:key_released`, and the formalized attachment.
- The glossary ingests the vocabulary's `time` scheme (`engine_seconds`, `anchor_datetime`, `t`).

### 2. Teach `build_spec.py` the note-severity markers

Upstream now marks a note's severity with a **leading marker inside the note string** —
`.warning`, `.important`, `.tip` — documented in the schemas repo's `CONTRIBUTING.md`. The
shape of `field-definitions.json` is unchanged (`notes` is still a list of strings), precisely
so this repo's parser does not break.

`build_spec.py` currently renders every note as a generic "*Note:* …", so a marked note would
print its marker literally. Strip the marker and emit the matching Quarto callout
(`::: {.callout-warning}` etc.); unmarked notes keep their current rendering. The schemas repo's
docs generator does exactly this — see `_split_note_level` in its `gh-pages:scripts/generate_docs.py`.

**Why it matters immediately:** the first user of this is the `response_numeric` / `score`
warning (below), which is precisely the note that must not be rendered as an easily-skipped
aside.

### 3. Questionnaire guide: drop what is now redundant

The field-by-field guidance from `guides/4-questionnaire-data.qmd` has been **migrated into the
trial schema** as field notes on `Response.stimulus_index`, `stimulus_description`,
`stimulus_onset`, `option_id`, `option_source`, `response_description`,
`response_option_index`, `response_numeric`, `score`, and `Option.onset`. It now appears
automatically on the generated spec pages. Remove any guide wording that merely restates it, and
link to the generated reference instead.

Two corrections worth knowing: the guide's `option_onset` note was reattached to **`Option.onset`**
(there is no `option_onset` field on `Response`, nor `option_duration` or `stimulus_duration`);
and the `response_numeric` / `score` distinction is now stated on **both** fields as a
`.warning`.

### 4. The attempt suffix is gone — sweep the site

Data filenames no longer carry an attempt suffix: `response.csv`, not `response_1.csv`. Several
runs of the same activity now live in one file, distinguished by the `runtime_id` and `attempt`
columns. **Boundary:** this applies to the tidy CSV tables and to the events NDJSON (whose lines
each carry `bdm:runtime_id`), but **not** to timeseries payloads — a binary recording cannot be
concatenated and two files cannot share a name, so those keep a per-run filename.

Measured on 2026-07-27, the suffix appears **60 times across 7 pages**: `response_1.csv` ×23,
`mouse_1.ndjson.gz` ×8, `stimulus_1.csv` ×7, `response_2.csv` ×7, `option_1.csv` ×6,
`events_1.ndjson` ×5, `input_1.csv` ×2, plus `stimulus_2.csv` and `option_2.csv` — in
`guides/1-getting-started.qmd`, `guides/3-organize-your-data.qmd`,
`guides/4-questionnaire-data.qmd`, `guides/7-events-data.qmd`, `concepts/index.qmd`,
`spec/timeseries.qmd`, `spec/conventions/folder-structure.qmd`.

The guide previously argued the filename made attempt counts and incomplete data visible without
opening files. **That property was not lost — it was improved**, and the replacement should be
described: filenames could only reveal attempts that produced data, whereas a run abandoned
before its first trial wrote no file at all and was invisible. The `Studyflow` run log records
it as a row, with `status` and `attempt`.

### 5. Folder structure: document the run log and the new placement

In `spec/conventions/folder-structure.qmd` (and the getting-started walkthrough):

- **`studyflow.csv` now has a schema** — the `Studyflow` table in the trial family. Document its
  columns: `runtime_id`, the scope (`agent_id`, `session_index`, `session_uuid`,
  `activity_index`, `instrument_id`, `timeline_id`), `attempt`, `instrument_repetition`,
  `timeline_repetition`, `status`, `abandon_reason`, `start_datetime`, `end_datetime`,
  `anchor_datetime`.
- Where the events layer lives: `…/<activity>/events.ndjson[.gz]`, one `Event` per line.
- Where timeseries live: payload plus its `<payload>.timeseries.json` sidecar in the same
  activity folder, with per-run filenames.
- An **acquisition→dataset mapping** section: `agent_id` → `agent_{x}` + a row in `agents.csv`;
  `session_index` → `session_{n}/`; task → `<activity>/`; derived tables → the activity's CSVs;
  raw events and timeseries beside them. Note that trial datetime columns are derived from the
  monotonic clock via `anchor_datetime`, which belongs to the **run**, not the session.

### 6. Correct the partitioning framing

The site currently describes the folder hierarchy as Hive/Arrow-style directory partitioning,
whose defining premise is that partition keys live in the **path** and not in the files. The
owner's ruling is the opposite: **a data file must carry the scoping needed to interpret it**,
and the folder tree is a *view* — the long-term model being a catalog database that *exports*
the BDM layout. That is why `runtime_id` is duplicated into every table. Rewrite the framing
accordingly; keep the practical guidance about the tree, drop the claim that the path is the
source of truth.

### 7. Events data: fix the `events.csv` claim, write the guide

- `guides/1-getting-started.qmd` says events are stored in `events.csv`. They are NDJSON:
  `events.ndjson[.gz]`, one canonical `Event` object per line, in the activity folder.
- `guides/_7-events-data.qmd` is an empty stub. Write and publish it: the three-level model, the
  envelope, the NDJSON at-rest decision and its rationale (events are nested and heterogeneous,
  so not tabular; crash-flushable; every line validates against the event schema), `EventBatch`
  as interchange only, the formalized `attachments` with relative-path addressing, the
  attachment → timeseries-sidecar → payload chain, and the clock mapping
  (`timestamp = anchor_datetime + t`).

### 8. Session identity, indexing, and consistency

- `explanations/7-indexing-things.qmd`: `session_uuid` is the global session identity while
  `session_index` remains the per-agent ordinal; `response_index` is now a real trial-schema
  field (its definition was taken *from* this page — confirm they agree). Resolve the
  contradiction with getting-started's claim that "session identifiers are unique within the
  dataset". Consider documenting `runtime_id` here as the run-level identifier.
- Consistency fixes: `subject_index` (explanations) vs `agent_{x}`/`agents.csv` (folder spec);
  `session_01` in prose vs `session_1` in examples; the `agent__001` double-underscore typo;
  `explanations/files-and-folders.qmd`'s `subject_001/session_1/response.csv` path.

### 9. Namespace statements

Any statement that `bdm:` is `https://behaverse.org/data-model/vocab/` is now wrong — it is
`https://behaverse.org/schemas/vocabulary/`. Compact `bdm:*` strings are unchanged. The event
spec's Timeseries section should link the timeseries schema
(https://behaverse.org/schemas/timeseries/) rather than describing sidecars ad hoc, and its
example attachment should use the formalized shape (relative `url`, not `file:///…`).

### 10. Low priority

Point the `spec/extensions/4-eeg.qmd` and `5-resting-state.qmd` stubs at the timeseries schema
as their data-layer foundation; add a site changelog entry.

## Method and output

- One coherent change-set per item; regenerate generated pages rather than editing them; verify
  against the live artifacts at `https://behaverse.org/schemas/...` rather than cached copies.
- House rules win: where an item conflicts with this site's conventions, the conventions win and
  the deviation is recorded.
- Final output: per item — what changed (files + a one-line summary), what was decided
  differently and why, and anything `behaverse/schemas` must change on its side. That last part
  feeds back to the schemas project; the previous round's feedback is what produced items 2 and 3.
