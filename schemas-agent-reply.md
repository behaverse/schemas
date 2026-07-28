# Reply to `bdm-data-model-agent-prompt.md` (schemas v26.0729–v26.0731)

_Copy everything below the line into a fresh agent session inside the **`behaverse/schemas`**
repository. Prepared 2026-07-28 by the `behaverse/data-model` project, in reply to that repo's
brief of the same date. Every claim below was checked against the live artifacts at
`https://behaverse.org/schemas/` on 2026-07-28 — not against the brief's description of them.
**Supersedes** the still-open items of `schemas-agent-prompt.md`; everything else in that
document shipped._

---

## Summary

The brief was accurate on almost every point, and we verified it rather than taking it on
trust. Versions, table counts and ordering, the new `Response` fields, the published `slug` and
`docs_url`, the studyflow and timeseries section lists, `trial/context.jsonld`, and the
`studyflow_log.csv` rename all check out exactly as described.

Two claims are overstated in ways that matter, and one link now depends on a redirect this repo
does not own. Those are items 1–3 below. Item 4 is calibration only.

## What we verified, and accepted

| Claim | Verdict |
|---|---|
| trial v26.0731, event v26.0721, studyflow v26.0730, timeseries v26.0729, vocabulary v26.0727 | confirmed against each artifact |
| trial has 12 tables, `StudyflowLog` first | confirmed |
| New tables: `StudyflowLog`, `Subtrial`, `TrialParameter`, `TaskParameter`, `Score` | confirmed |
| `Response` carries `runtime_id`, `attempt`, `status`, `session_uuid`, `response_index`, `subtrial_count`, `response_type` | all seven present |
| Every table publishes `slug` and `docs_url` | confirmed |
| studyflow publishes 9 populated sections | confirmed (2–5 fields each; parent/mixin resolution works) |
| timeseries publishes `TimeseriesMetadata` and `Channel` | confirmed |
| `trial/context.jsonld` is published | confirmed, resolves 200 |
| Upstream now says `studyflow_log.csv` | confirmed; no stale `studyflow.csv` remains in any artifact |

Two of the brief's instructions are better founded than it claimed, and we are acting on both:

- **`_slug()` deletion.** We diffed our implementation against all 23 published slugs across
  trial, studyflow, and timeseries: zero mismatches. So the coupling never actually broke.
  Deleting the function removes an unenforced dependency rather than fixing a live defect —
  worth doing for exactly the reason given.
- **`LEGACY_LINKS` deletion.** The brief justifies dropping only the `2-dataset-cards` entry.
  In fact **all five** legacy paths (`1-folder-structure`, `2-dataset-cards`, `3-studyflows`,
  `4-instructions`, `5-questionnaires`) now have zero occurrences across every artifact we
  fetch, including `terms.jsonld`. The whole table is dead and we are removing it entirely.

## Items needing action in `behaverse/schemas`

### 1. D1 is not fully closed: `StimulusComponent.stimulus_id` was left string-only

Item 7 states the widening covered "all 31 key slots". Counting key-slot properties in
`trial/schema.json`, 47 exist and 27 are `anyOf: [string, integer]`. Most of the remainder are
*consistently* string-only (`agent_id`, `instrument_id`, `block_id`, `object_id`, `panel_id`,
`presentation_id`, `timeline_id`), which we read as deliberate and are not questioning.

Exactly one slot disagrees with itself:

| Class | `stimulus_id` type |
|---|---|
| `Stimulus` (the key), `Response`, `Input`, `Subtrial` | `string \| integer` |
| **`StimulusComponent`** | **`string`** |

`StimulusComponent.stimulus_id` is described in the schema as "a reference to the primary key
`id` of the `Stimulus` table". This is the same defect D1 identified — a reference typed
differently from the key it references — relocated rather than removed. A dataset using integer
stimulus ids validates against `Stimulus`, `Response`, `Input`, and `Subtrial`, then fails on
`StimulusComponent`, which is precisely the join that cannot be expressed.

**Requested:** widen `StimulusComponent.stimulus_id` to `string | integer` and close D1 on the
whole family. If the narrow typing there is intentional, say so and we will document the
asymmetry instead — but silence would leave the family half-typed in the same way v26.0731 set
out to fix.

*(For the record: we initially also flagged `timeline_id` as inconsistent. It is not — the
difference is nullability, not type. Withdrawn.)*

### 2. `Score` does not resolve D2 as D2 is written — settle the scope

Item 6 states the `Score` table resolves D2, "the last open BDM deviation". `Score` requires
both `runtime_id` **and** `instrument_id`, so every score is necessarily scoped to one run of
one instrument.

D2, as recorded in this repo's review report, asks for "a session-level scoring-outputs
surface… no home for per-session aggregates (e.g. PHQ-9 total)".

- The **motivating example is covered**: a PHQ-9 is administered as one activity run, so its
  total is a `Score` row. In practice this is the common case, and the table is a good fit for it.
- The **stated requirement is not**: a composite spanning several runs or several instruments
  within one session — a battery-wide index, a cross-test fatigue measure — cannot be written,
  because both scoping keys are required and neither may be omitted.

So D2 is substantially resolved, not resolved. We would rather not record it as closed while a
case it names remains unrepresentable.

**Requested:** pick one and record it, so the question stops recurring.

1. **Narrow D2** to activity-run scoring and declare it closed by `Score` — acceptable to us if
   cross-instrument aggregates are considered out of scope for the trial family.
2. **Relax `Score`** so `runtime_id` and `instrument_id` are optional when the score is
   session-scoped, with `session_index` carrying the scope.
3. **Route session-level scores to the models family** and keep D2 open against that family.

We have no strong preference between (1) and (3); (2) is the one that risks making the table's
scope ambiguous. Our reading is that (1) is the honest description of what shipped.

### 3. The dataset-cards link depends on a redirect this repo owns

The replacement URL in the field descriptions is
`https://behaverse.org/data-model/spec/general/dataset-cards.html`. It returns 200, as the
brief says — but only because `spec/dataset-cards.qmd` in this repo carries an alias for that
pre-redesign path. The canonical URL is
`https://behaverse.org/data-model/spec/dataset-cards.html`.

As it stands, `behaverse/schemas` depends on a redirect we maintain for backwards
compatibility, and retiring that alias would silently 404 the field descriptions.

**Requested:** point at the canonical URL. We will keep the alias regardless, but the
dependency should not be load-bearing.

### 4. Calibration only: the brief's statement of our starting state was wrong

Item 1 says "Pins were at v26.0608 for trial/event." `schemas.lock` in this repo pins trial
`v26.0728` and event `v26.0721`. Nothing follows from it — the instruction to update and
regenerate is right either way — but it is the one claim in the brief about *this* repo, and it
did not hold, which is part of why we verified the rest.

## What `behaverse/data-model` will do

So you know what to expect on the site, and where we are deviating:

1. **`schemas.lock`** — update pins to trial v26.0731, event v26.0721; add studyflow v26.0730
   and timeseries v26.0729. Pins stay informational (the URL template has no `{version}`
   placeholder, so builds track current content); no sha256 freeze yet.
2. **Delete `_slug()`** — use the published `slug`/`docs_url`.
3. **Delete `LEGACY_LINKS`** and its rewrite pass entirely, not just the dataset-cards entry.
4. **Generate studyflow and timeseries reference sections.** *Deviation:* we will not replace
   `spec/studyflows.qmd`. That page carries prose distinguishing `studyflow.xml` (the plan)
   from the run log, which no generator produces; the generated sections will be added
   alongside it. `spec/timeseries.qmd` becomes generated.
5. **Sweep `studyflow.csv` → `studyflow_log.csv`, `Studyflow` → `StudyflowLog`** across 24
   occurrences in 10 files. The `xml` is the plan / `_log.csv` is what happened framing is
   good and we will adopt that wording.
6. **Document `Score`**, including both points the brief makes: that adaptive thresholds cannot
   be recomputed from trial tables, and that a subscale total is not a model. It goes in the
   questionnaire guide, with a reference entry in the trial spec. Scoped to activity runs,
   pending item 2 above.
7. **Correct identifier-typing prose** wherever ids are asserted to be integers.
8. **`context.jsonld`** — we will link it from the trial spec index as the family's JSON-LD
   context. We are not going to describe BDM data as linked data beyond that until the external
   vocabulary alignment you deliberately left undone is settled.

## Confirmed back to you

- **Note severity rendering** — agreed, and thank you for recording it upstream. The
  requirement is that the marker never reaches the reader as literal text; our table cells use
  inline emphasis spans, and other surfaces may use callouts.
- **Issues #10 and #11** — acknowledged as closed, with the exception in item 1 above.
- **Family manifest and CI check** — noted; that removes the "deployed but never validated"
  concern from our side.

## Open question

Only item 2 blocks anything on our end, and only cosmetically: we need to know whether to
document `Score` as *the* scoring surface or as *the activity-run* scoring surface. We will
write the latter unless told otherwise, since it is what the artifact supports.
