# Behaverse Trial Schema (WIP)

**Version:** v26.0801
**Namespace:** `https://behaverse.org/schemas/trial#`
**Source of truth:** [`schema.linkml.yaml`](schema.linkml.yaml) — edit it, then run `python scripts/generate.py`

## Overview

The Behaverse Trial Schema defines a set of tidy tables describing **trial-level** behavioral data — the task-specific aggregates derived from raw events — for cognitive tests and questionnaires. It is the *Trials* layer of the Behaverse Data Model (BDM); see **[behaverse.org/data-model](https://behaverse.org/data-model)** for the human-facing guides, conventions, and explanations.

A trial is a single instance of a participant interacting with a task. Trial information is spread across several related tables, joined by `_id` foreign keys.

## Tables

| Table | Fields | Description |
|-------|-------:|-------------|
| **StudyflowLog** | 15 | The run log: one row per activity run (`studyflow_log.csv`). |
| **Response** | 82 | Main table; one row per response in a trial. |
| **Stimulus** | 20 | Each stimulus shown during a trial. |
| **Option** | 19 | Each option an agent could choose from. |
| **Input** | 16 | Detailed log of inputs/clicks during the trial. |
| **StimulusComponent** | 14 | Components that make up a stimulus. |
| **OptionComponent** | 15 | Components that make up an option. |
| **Instrument** | 7 | The instrument (and its parameterizations) used for acquisition. |
| **Subtrial** | 20 | Per-stage detail for staged trials (e.g. the two-step); the trial row stays the unit. |
| **TrialParameter** | 10 | Ground-truth generative parameters that vary trial to trial, long format. |
| **TaskParameter** | 10 | Ground-truth generative parameters constant across an activity run, long format. |
| **Score** | 14 | Scores summarising a whole activity run (subscale totals, thresholds), long format. |

## Conventions

- A trailing `_id` denotes a **foreign key** into the table of that name (e.g. `stimulus_id` → the Stimulus table).
- When several entities occur in one trial (e.g. multiple stimuli), their ids/values are concatenated into a single string on CSV export.
- **Every table carries `runtime_id`**, identifying the activity run — one execution of one activity by one agent, with restarts counted separately. Local keys (`response_id`, `stimulus_id`, …) are unique *within a run*, so the dataset-wide key is the pair, e.g. (`runtime_id`, `response_id`). This is what lets files of the same type be concatenated across agents, sessions, and attempts without losing scope: a data file carries the information needed to interpret it, and the folder layout is a view rather than the source of truth.
- `runtime_id` is the same identifier the event layer carries as `bdm:runtime_id`, so events and trials join directly.

## The run log

`StudyflowLog` (shipped as `studyflow_log.csv` in the agent's folder) records what an agent **actually did** — one row per activity run, with its scope, `attempt`, `status`, timing, and the `anchor_datetime` that bridges the monotonic recording clock to wall-clock time. It is distinct from the study-level *plan*: the BPMN studyflow diagram described by the [`studyflow`](../studyflow/) schema family, which says what was designed to happen.

Because it exists per run rather than per trial, it can represent a run that was started and abandoned before any trial finished — such a run produces no rows in any other table. Selecting the last complete attempt is a filter plus a join: keep `status = completed`, take the largest `attempt` per (`agent_id`, `instrument_id`), then join `Response` on `runtime_id`.

## Artifacts

| File | Status | Purpose |
|------|--------|---------|
| [`schema.linkml.yaml`](schema.linkml.yaml) | ✅ | Source of truth (LinkML). Edit it, then run `python scripts/generate.py`. |
| [`field-definitions.json`](field-definitions.json) | ✅ generated | Render contract consumed by `behaverse/data-model` and the docs site. |
| [`schema.json`](schema.json) | ✅ generated | JSON Schema (Draft-07): per-table definitions + a top-level table→rows object. Validates types + required fields (not enums/ranges/foreign keys — the source is coarse). |
| [`context.jsonld`](context.jsonld) | ✅ generated | JSON-LD context: every field gets a stable, resolvable URI under the trial namespace (`@vocab`), with typed literals declared. |

## Status & follow-ups

Relocated from `behaverse/data-model` (where it was generated from a Google Sheet). Published **as-is**; these known issues are tracked as follow-ups, not yet applied:

- **D1** — `Response.stimulus_id` typing (`integer` → `string | integer`) for compositional questionnaire stimuli.
- **D3** — **resolved**: renamed `session_id` → `session_index` (v26.0703) and added `session_uuid` (v26.0720). Deviation from the issue's wording: the UUID field is named `session_uuid`, not `session_id` — reusing `session_id` with a new type and meaning right after it had meant "integer index" would silently break existing consumers.
- **D5** — events `agent` → `actor` (applied in the `event` schema).
- Several `description`/`range` fields still mix prose with enum listings that could become structured `enum` constraints.

## Versioning

CalVer `vYY.MMDD`. See the repo-wide [`VERSIONING.md`](../VERSIONING.md).
