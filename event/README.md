# Behaverse Event Schema (WIP)

**Version:** v26.0720
**Namespace:** `https://behaverse.org/schemas/event#`
**Source of truth:** [`schema.linkml.yaml`](schema.linkml.yaml) (envelope + vocabulary) — run `python scripts/generate.py`. [`schema.json`](schema.json) is the validation contract.

## Overview

Raw experimental events for cognitive tests, questionnaires, and games. An xAPI-style envelope (**actor / verb / object**) carrying a single canonical `bdm:` vocabulary, so one set of analytics tooling can process every domain. Continuous signals (mouse, keyboard, EEG, …) are referenced via `attachments`, not inlined. It is the *Events* layer of the Behaverse Data Model (BDM); see **[behaverse.org/data-model](https://behaverse.org/data-model)**.

## Vocabulary at a glance

- **25 verbs** across 6 layers: RuntimeInstance lifecycle (7), presentation (1 polymorphic), agent interaction (11), system (3), recording (2), navigation (1).
- **15 object types:** RuntimeInstance, Screen, Panel, Stimulus, Option, Trial, UIComponent, Window, Feedback, ConsentForm, Consent, Recording, Timer, Scorer, LocaleSwitch.
- **5 actor types:** Agent, Group, Engine, Orchestrator, Researcher.
- **`bdm:*` extension keys** (open-by-design) carry response data, the scoping hierarchy, environment, and interaction-specific payloads under `result.extensions` / `context.extensions`.

## Scoping hierarchy

Events are positioned in a five-level hierarchy carried in `context.extensions`:
`session → activity → RuntimeInstance → block → trial`. The Activity-vs-RuntimeInstance distinction separates *what was planned* from *a specific execution* (restarts produce distinct RuntimeInstances).

## Storage (events at rest)

**Decision (2026-07-20).** The canonical at-rest representation of the events layer in a BDM dataset is **NDJSON**: one canonical `Event` object per line, UTF-8, append-only — `events_<attempt>.ndjson` (optionally gzipped to `.ndjson.gz` once the recording closes), stored in the dataset's activity folder beside the trial tables: `data/agent_{x}/[session_{n}/]<activity>/events_1.ndjson`, partitioned by attempt like `response_1.csv`.

- **Why NDJSON:** events are nested and heterogeneous (per-verb `result`/`context` extensions), so they are not tabular — CSV would force JSON-in-cells or an unbounded sparse column set. NDJSON is crash-flushable (a session that dies mid-recording keeps every event written so far), streams without a whole-file parse, and every line validates against this schema's `Event` branch as-is.
- **`EventBatch` is the interchange shape** (API/LRS responses, exports) — not the at-rest format.
- **Derived copies** (e.g. Parquet for analytics) are permitted; the NDJSON stream remains the raw source of truth.
- Recording engines with private compact formats must document a **lossless mapping** from their rows to canonical `Event` objects.

See [`examples/events.ndjson`](examples/events.ndjson) for a worked stream.

## Artifacts

| File | Status | Purpose |
|------|--------|---------|
| [`schema.linkml.yaml`](schema.linkml.yaml) | ✅ | Source of truth (LinkML; envelope + vocabulary). Edit it, then run `python scripts/generate.py`. |
| [`field-definitions.json`](field-definitions.json) | ✅ generated | Render contract consumed by `behaverse/data-model` and the docs site. |
| [`schema.json`](schema.json) | ✅ generated | JSON Schema (Draft 2019-09) for validation: `EventDocument = Event \| EventBatch`, with `verb`/`actor.objectType`/`object.objectType` enum-validated against the canonical vocabulary. |
| [`context.jsonld`](context.jsonld) | ✅ generated | JSON-LD context (`bdm:`, `xapi:`, `schema:`, `as2:`). |
| [`examples/`](examples/) | ✅ | Minimal event + PHQ-9 / N-back / kitchensink event batches + an NDJSON at-rest stream. |

## Provenance & follow-ups

Relocated from the Behaverse questionnaire project (`schemas/events`, v26.0605), **canonicalized to `event` (singular)** to match `trial` and the BDM convention. Realizes BDM deviations **D4** (this vocabulary), **D5** (`agent` → `actor`, applied), and **D6** (the scoping hierarchy).

- The ~50 `bdm:*` extension keys and their per-key shape contracts are documented in the source design note (`05e_events_vocabulary.md`) and should be relocated into this README or a `vocabulary/` resource.
- `result`/`context` are intentionally `additionalProperties: true` with `bdm:*`-prefixed extension keys; a tighter per-verb result contract is a follow-up.

## Versioning

CalVer `vYY.MMDD`. See the repo-wide [`VERSIONING.md`](../VERSIONING.md).
