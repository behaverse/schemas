# Behaverse Trial Schema (WIP)

**Version:** v26.0721
**Namespace:** `https://behaverse.org/schemas/trial#`
**Source of truth:** [`schema.linkml.yaml`](schema.linkml.yaml) — edit it, then run `python scripts/generate.py`

## Overview

The Behaverse Trial Schema defines a set of tidy tables describing **trial-level** behavioral data — the task-specific aggregates derived from raw events — for cognitive tests and questionnaires. It is the *Trials* layer of the Behaverse Data Model (BDM); see **[behaverse.org/data-model](https://behaverse.org/data-model)** for the human-facing guides, conventions, and explanations.

A trial is a single instance of a participant interacting with a task. Trial information is spread across several related tables, joined by `_id` foreign keys.

## Tables

| Table | Fields | Description |
|-------|-------:|-------------|
| **Response** | 79 | Main table; one row per response in a trial. |
| **Stimulus** | 19 | Each stimulus shown during a trial. |
| **Option** | 18 | Each option a subject could choose from. |
| **Input** | 15 | Detailed log of inputs/clicks during the trial. |
| **StimulusComponent** | 13 | Components that make up a stimulus. |
| **OptionComponent** | 14 | Components that make up an option. |
| **Instrument** | 7 | The instrument (and its parameterizations) used for acquisition. |
| **Subtrial** | 19 | Per-stage detail for staged trials (e.g. the two-step); the trial row stays the unit. |
| **TaskParameter** | 6 | Per-trial ground-truth generative task parameters, long format. |

## Conventions

- A trailing `_id` denotes a **foreign key** into the table of that name (e.g. `stimulus_id` → the Stimulus table).
- When several entities occur in one trial (e.g. multiple stimuli), their ids/values are concatenated into a single string on CSV export.

## Artifacts

| File | Status | Purpose |
|------|--------|---------|
| [`schema.linkml.yaml`](schema.linkml.yaml) | ✅ | Source of truth (LinkML). Edit it, then run `python scripts/generate.py`. |
| [`field-definitions.json`](field-definitions.json) | ✅ generated | Render contract consumed by `behaverse/data-model` and the docs site. |
| [`schema.json`](schema.json) | ✅ generated | JSON Schema (Draft-07): per-table definitions + a top-level table→rows object. Validates types + required fields (not enums/ranges/foreign keys — the source is coarse). |
| `context.jsonld` | — | Not emitted (the trial fields carry no semantic `mappings`). |

## Status & follow-ups

Relocated from `behaverse/data-model` (where it was generated from a Google Sheet). Published **as-is**; these known issues are tracked as follow-ups, not yet applied:

- **D1** — `Response.stimulus_id` typing (`integer` → `string | integer`) for compositional questionnaire stimuli.
- **D3** — **resolved**: renamed `session_id` → `session_index` (v26.0703) and added `session_uuid` (v26.0720). Deviation from the issue's wording: the UUID field is named `session_uuid`, not `session_id` — reusing `session_id` with a new type and meaning right after it had meant "integer index" would silently break existing consumers.
- **D5** — events `agent` → `actor` (applied in the `event` schema).
- Several `description`/`range` fields still mix prose with enum listings that could become structured `enum` constraints.

## Versioning

CalVer `vYY.MMDD`. See the repo-wide [`VERSIONING.md`](../VERSIONING.md).
