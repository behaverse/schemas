# behaverse/schemas — open issues

**The** working note for this repo: everything still open, in one place. Consolidated
2026-07-27 from `HANDOFF.md`, `bcsv/HANDOFF.md`, `improvements.md`, `docs-architecture.md`,
`bdm_extensions.md`, and the executed `bdm-schemas-agent-prompt.md` — all now in
[`_archive/`](_archive/) (gitignored; kept for rationale and history, not as live state).

Untracked working note, like its predecessors. Every claim below was re-verified against the
working tree on **2026-07-27** unless marked otherwise; items inherited from the 2026-07-03
review that could not be re-verified are marked `[unverified]`.

Live companion document at the repo root:
- [`bdm-data-model-agent-prompt.md`](bdm-data-model-agent-prompt.md) — the ready-to-run agent
  brief for §5 (the `behaverse/data-model` site round), rewritten 2026-07-27 against schemas
  v26.0728. Hand it to an agent in that repo verbatim.
  (`DESIGN-scoping-and-run-log.md` is now implemented; kept as the record of the decisions.)

---

## 0. In flight

- ✅ **DONE (trial v26.0727).** **Scoping redesign — run log + two-tier scoping.** `studyflow.csv` ships in every dataset's
  agent folder and records each agent's activity runs (attempts), but **has no schema
  anywhere**: the `studyflow` family models the BPMN *plan* (Study/Activity/gateways), not
  execution. The trial schema already dangles a reference to a nonexistent "`Studyflow` table"
  ([trial/schema.linkml.yaml:180](trial/schema.linkml.yaml#L180)). Decided direction
  (2026-07-27): schematize the run log, key it with `runtime_id` (matching the event layer's
  existing `bdm:RuntimeInstance` / `bdm:runtime_id`), carry lifecycle-derived `status` so
  "last complete attempt" is a filter rather than a reconstruction, and adopt **two-tier
  scoping** — main files (`Response`) generously denormalized for standalone readability,
  detail tables lean. Detail tables join on `(runtime_id, response_id)` because `response_id`
  is only unique *within a file* (option (b), ratified 2026-07-27). Design doc pending.
- ✅ **DONE (trial v26.0727).** **Generative-parameter grain split.** Rename the shipped trial-grained `TaskParameter` →
  `TrialParameter` (+ required `response_id`, optional `subtrial_index`); add a new
  activity-run-grained `TaskParameter`. **Blocked on** the scoping redesign above, so the new
  table's scoping lands right the first time. Source proposal archived at
  `_archive/trial-PROPOSAL_task_vs_trial_parameters.md`.
- **data-model site round.** Not started; itemized in §5 and written up as a hand-off brief
  ([`bdm-data-model-agent-prompt.md`](bdm-data-model-agent-prompt.md)). **This is the next
  substantial piece of work**, and it lives in the other repository.

---

## 1. Schema content

- **~25 prose-only enums in `trial`.** 25 slots carry `bdm_type: "enum"` with the value set
  written as prose in `range_description`, so `schema.json` cannot validate them.
  `Response.response_type` (v26.0721) is the only real LinkML enum. Migrating the rest is the
  single biggest quality win available in the trial family.
- **Two dangling table references in `trial`.** `agent_id` says "See `Agent` table"
  ([:131](trial/schema.linkml.yaml#L131)) and `activity_index` says "See `Studyflow` table"
  ([:180](trial/schema.linkml.yaml#L180)). Neither table exists in any family. `agents.csv`
  ships in datasets and is likewise unspecified — the Agent table is a real gap, not just a
  bad cross-reference.
- **`trial` has no semantic mappings**, so it deliberately emits no `context.jsonld`. Adding
  `slot_uri`/`exact_mappings` would unlock it.
- ✅ **RESOLVED (studyflow v26.0728).** The family was confirmed alive and given its first
  tagged release: real CalVer, a written changelog entry, its first `versions/` snapshot, and
  the commented-out placeholder classes removed.
- **`dataset` semantic-mapping bugs** (2026-07-03 review, re-verified where noted):
  - `sample_size` → `ddiuniverse:Universe.html` — a documentation *page*, not a term URI. ✔confirmed
  - `study_design_type` → `sdo:MedicalStudy` — a schema.org *class* used as a slot URI. ✔confirmed
  - `age_mean` → `cdisc:AGE`; check whether `age_range` shares the same URI. `[partially verified]`
  - `language` pattern reportedly rejects valid BCP-47 tags. `[unverified]`
- **`bdm_extensions.md` items still open** (full rationale in `_archive/bdm_extensions.md`;
  §1 Subtrial, §2 response_type, and §7 TaskParameter shipped in v26.0721):
  - **§3 Instructed/forced trials** — `decided_by` / `executed_by` with a shared value set
    (`self` · `task` · an `agent_id`, reserved token `other_agent`). Value design agreed;
    use-case list open. Note its validation rule ("any other value must resolve in the Agent
    table") presupposes the missing Agent table above.
  - **§4 Task-dependence facts** — `outcome_depends_on_response` / `trials_depend_on_response`,
    and reconciling them with `has_reward_dynamics`; informed by the existing `adaptive_*`
    precedent.
  - **§5 `task_structure` vocabulary** — curated predicate vocabulary; drafted modeling-side.
  - **§6 Stimulus feature vectors / column groups / binds** — modeling-side (dataset + study
    cards), nothing needed here yet.
  - **§8 Tasks as first-class entities with levels** — spec vs instrument vs implementation,
    plus parameter provenance (recovered vs from-source). Needs a design pass; overlaps the
    existing `Instrument` table.
  - **§9 Per-option attributes** — deferred to the future Behaverse data catalog.

## 2. Cross-cutting

- **Self-scoping rule not yet applied schema-wide.** Ruling (2026-07-27): a data file must
  carry the scoping needed to interpret it; folder hierarchy is a *view*, not the source of
  truth (the eventual model being a catalog database that *exports* the BDM folder layout).
  Today `Stimulus`, `Option`, `Input`, `Subtrial` scope only by `response_id`/`trial_index`,
  and `StimulusComponent`, `OptionComponent`, `Instrument` carry no scoping at all. The
  in-flight redesign covers `Response` and the parameter tables; the rest is a follow-up
  release. Note this also contradicts the data-model site's "Hive/Arrow-style partitioning"
  framing, which must be corrected there.
- **No shared LinkML module.** `catalog` and `dataset` independently define near-identical
  person shapes (`Curator` vs `Person`), the License enum, and email/orcid/doi patterns. A
  `common.linkml.yaml` would remove the drift risk. (The July note said "Person duplication";
  in fact only `dataset` has `Person` — `catalog` has `Curator`. Same problem, different names.)
- **Divergent `behaverse:` prefix.** Each family binds `behaverse:` to its own namespace
  (`…/schemas/<family>#`), so the prefix means something different per file. The `bdm:` prefix
  was unified in v26.0721; `behaverse:` was not.
- **Hash vocabulary.** bcsv's `file_hash` mandates SHA-256 (`^[a-f0-9]{64}$`), the timeseries
  and event schemas use `sha256` fields, while the vocabulary's `*_hash` term is
  algorithm-agnostic. Not a contradiction, but the vocabulary term could state the SHA-256
  default.
- **License vocabulary** differs across families: bcsv free-form SPDX string, `dataset` an
  SPDX enum, `catalog` none. Unify only if desired.

## 3. Process & release

- **No git tags** — zero tags in the repo despite 20+ published versions. Tagging releases
  would make `versions/` snapshots navigable from git history.
- **Snapshot backfill — mostly closed.** `studyflow` and `vocabulary` published their first
  snapshots in v26.0728/v26.0727. Remaining gaps are historical: `event` 26.0608 and `catalog`
  25.1202 were released but never archived.
- **No `versions/` immutability guard in CI.** The policy says snapshots are immutable; nothing
  enforces it. An add-only check (fail if a file under any `versions/` is modified or deleted)
  is cheap and directly protects the pinning promise.
- **No stability/pinning policy in `VERSIONING.md`** — CalVer does not telegraph breaking
  changes; there is no documented "compatible-with-X" statement for consumers.
- **Adding a family still touches two Python lists** (`scripts/generate.py`,
  `scripts/validate_schemas.py`). The deploy workflow was reduced to a single `SCHEMA_DIRS`
  env var in v26.0721; glob-discovery for the Python side remains.
- **Release automation** — the whole bump/regenerate/snapshot/changelog dance is manual by
  design; revisit only if it becomes a burden. (`scripts/version_schema.py` was retired; the
  stale reference in `VERSIONING.md` is already gone.)
- **`gh-pages` carries stale copies** of the schema dirs (gitignored there; CI re-fetches from
  `main` each build). Optional `git rm` cleanup.

## 4. Docs & site

- **No `CITATION.cff`**, and the repo's CC BY 4.0 `LICENSE` covers the Python code under
  `scripts/` — code wants a software license (the LinkML sources already declare `license: MIT`).
- **`timeseries` has no examples page** on the docs site (the schema ships two examples in the
  repo); `trial` and `event` have no `examples.md` either.
- **Docs-generator gotchas** (from the archived `HANDOFF.md`, still true): the studyflow path
  hardcodes `requirement: optional`; `gh-pages:docs/src/css/custom.css` forces 4-column widths
  with `!important` on every article table, so 2- and 3-column tables need `:has()` overrides.
- **Only `catalog`'s README shows a runnable validation command** — the others leave consumers
  to guess.
- The durable parts of the archived `docs-architecture.md` — the content-ownership matrix (§4),
  per-artifact target structure (§6), and cross-linking rules (§7) — remain the reference for
  deciding where a piece of documentation belongs.

## 5. behaverse/data-model site (separate repo)

The Quarto site at behaverse.org/data-model consumes this repo's artifacts: `schemas.lock` +
`scripts/build_spec.py` fetch `field-definitions.json` (trial, event) and
`vocabulary/terms.jsonld`, and generate the `/spec/trial/`, `/spec/event/`, and glossary pages.
**None of the items below is done.** A ready-to-use agent brief covering all of them, with the
full upstream digest, is archived at `_archive/bdm-data-model-agent-prompt.md` — it can be handed
to an agent in that repo verbatim, but items 1–7 must be re-checked against §0 first (the
in-flight run-log design will add to items 3 and 8).

1. **Regenerate the spec pages.** Trial now has **9 tables** — the generated spec needs pages for
   `Subtrial` and `TaskParameter`, and the Response page needs `session_index`, `session_uuid`,
   `response_index`, `subtrial_count`, `response_type`. Event needs 25 verbs incl.
   `bdm:key_released`, plus the formalized attachment shape. Check the numbered-filename scheme
   (`1-response.qmd` … `7-instrument.qmd`) extends cleanly, and update the `schemas.lock` pins
   (trial/event were pinned at v26.0608; both are now v26.0721+).
2. **Fix the `events.csv` claim.** `guides/1-getting-started.qmd` says events live in
   `events.csv`; the settled convention is NDJSON — `events_<attempt>.ndjson[.gz]`, one `Event`
   per line, in the activity folder.
3. **Write the events-data guide.** `guides/_7-events-data.qmd` is an empty stub (underscore =
   unpublished). Content: the three-level model, the envelope, the NDJSON at-rest decision and
   its rationale, `EventBatch` as interchange only, the formalized `attachments` + relative-path
   addressing, the attachment → timeseries-sidecar → payload chain, and the clock mapping
   (`timestamp = anchor_datetime + t`).
4. **Dataset structure: file placement + acquisition mapping.** Document where the events layer
   and timeseries payloads/sidecars live in the activity folder, and add an acquisition→dataset
   mapping section (`agent_id` → `agent_{x}` + `agents.csv` row; `session_index` → `session_{n}/`;
   task → `<activity>/`; derived tables → the activity's CSVs). State that trial datetime columns
   are derived from the monotonic clock via `anchor_datetime`.
5. **Session identity and indexing.** `explanations/7-indexing-things.qmd` must reflect
   `session_uuid` as the global identity (with `session_index` staying the per-agent ordinal), and
   `response_index` now being a real trial-schema field — its definition was taken *from* that
   page, so confirm the two agree. Resolve the contradiction with getting-started's claim that
   "session identifiers are unique within the dataset".
6. **Consistency fixes.** `subject_index` (explanations) vs `agent_{x}`/`agents.csv` (folder spec);
   `session_01` in prose vs `session_1` in examples; the `agent__001` double-underscore typo;
   `explanations/files-and-folders.qmd`'s `subject_001/session_1/response.csv` path.
7. **Namespace statements.** Any `bdm:` = `https://behaverse.org/data-model/vocab/` statement is
   now wrong — it is `https://behaverse.org/schemas/vocabulary/`. The event spec's Timeseries
   section should link the new timeseries schema rather than describing sidecars ad hoc, and its
   example attachment should use the formalized shape (relative `url`, not `file:///…`).
8. **Pending the §0 run-log design** (do not write until it lands): document `studyflow.csv`'s
   columns in the dataset-structure spec, and **correct the "Hive/Arrow-style partitioning"
   framing** — under the self-scoping ruling, partition keys are duplicated into the data rather
   than delegated to the path.
9. **Low priority.** Point the `spec/extensions/4-eeg.qmd` and `5-resting-state.qmd` stubs at the
   timeseries schema as their data-layer foundation; add a site changelog entry.

## 6. Ecosystem & future

- **Vocabulary SKOS mappings** to external ontologies (NCIT, OBI, Cognitive Atlas), and backing
  the event schema's `bdm:` enums with vocabulary terms.
- **Machine-readable index of the schema collection** — dogfood the `catalog` schema to
  describe this repo's own families.
- **Interop profiles**: Croissant, Psych-DS, Frictionless.
- **schemastore.org registration** so editors autocomplete Behaverse JSON files.
- **R/Python consumer packages** (`bcsv-py`, `bcsv-r`) live in a separate repo; this repo only
  ships the artifacts they consume. Do not reference them in user-facing docs until they ship.
- **Behaverse data catalog** — the BDM-conformant dataset collection; the home for wide→Option
  reformatting (`bdm_extensions.md` §9).

---

## Settled — do not reopen without new evidence

- **Source of truth:** LinkML for catalog/dataset/trial/event/timeseries/studyflow; native
  formats for bcsv (hand-maintained `schema.json`) and vocabulary (`terms.yaml`).
- **Events at rest:** NDJSON, one `Event` per line, `events_<attempt>.ndjson[.gz]` in the
  activity folder. `EventBatch` is the interchange shape only. No separate `acquisition/`
  family — engines with private formats owe a documented lossless mapping.
- **Timeseries:** sidecar metadata (`<payload>.timeseries.json`) beside a format-agnostic
  payload; channels are the primitive, not per-modality classes.
- **`bdm:` namespace:** `https://behaverse.org/schemas/vocabulary/` everywhere.
- **Naming:** `session_uuid` (not a re-typed `session_id`); `response_index` (subject-nested
  response ordinal) is distinct from `response_option_index`; dataset's input-modality field is
  `response_modality`, leaving `response_type` to mean the answer's form in `trial`.
- **bcsv:** `categorical`/`ordered` datatypes kept over strict CSVW compatibility; `name` kept
  at both table and column level; table-level `name` maps to `csvw:name`, not `schema:name`;
  `bcsvw → bcsv` URI 404s accepted.
- **Docs:** two audiences, single-source by content type (README for the repo reader, generated
  Overview + per-property pages for the site, hand-written About for narrative).
- **No vaporware:** consumer packages stay out of user-facing docs until they ship.
