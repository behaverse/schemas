# Behaverse Event Schema (WIP)

**Version:** v26.0608
**Namespace:** `https://behaverse.org/schemas/event#`
**Source of truth:** [`field-definitions.yaml`](field-definitions.yaml) (envelope + vocabulary) — run `uv run scripts/generate.py`. [`schema.json`](schema.json) is the validation contract.

## Overview

Raw experimental events for cognitive tests, questionnaires, and games. An xAPI-style envelope (**actor / verb / object**) carrying a single canonical `bdm:` vocabulary, so one set of analytics tooling can process every domain. Continuous signals (mouse, keyboard, EEG, …) are referenced via `attachments`, not inlined. It is the *Events* layer of the Behaverse Data Model (BDM); see **[behaverse.org/data-model](https://behaverse.org/data-model)**.

## Vocabulary at a glance

- **24 verbs** across 6 layers: RuntimeInstance lifecycle (7), presentation (1 polymorphic), agent interaction (10), system (3), recording (2), navigation (1).
- **15 object types:** RuntimeInstance, Screen, Panel, Stimulus, Option, Trial, UIComponent, Window, Feedback, ConsentForm, Consent, Recording, Timer, Scorer, LocaleSwitch.
- **5 actor types:** Agent, Group, Engine, Orchestrator, Researcher.
- **`bdm:*` extension keys** (open-by-design) carry response data, the scoping hierarchy, environment, and interaction-specific payloads under `result.extensions` / `context.extensions`.

## Scoping hierarchy

Events are positioned in a five-level hierarchy carried in `context.extensions`:
`session → activity → RuntimeInstance → block → trial`. The Activity-vs-RuntimeInstance distinction separates *what was planned* from *a specific execution* (restarts produce distinct RuntimeInstances).

## Artifacts

| File | Status | Purpose |
|------|--------|---------|
| [`field-definitions.yaml`](field-definitions.yaml) | ✅ | Source of truth (envelope + vocabulary). |
| [`field-definitions.json`](field-definitions.json) | ✅ generated | Render contract consumed by `behaverse/data-model` and the docs site. |
| [`schema.json`](schema.json) | ✅ | JSON Schema (Draft 2020-12) for validation. |
| [`context.jsonld`](context.jsonld) | ✅ | JSON-LD context (`bdm:`, `xapi:`, `schema:`, `as2:`). |
| [`examples/`](examples/) | ✅ | Minimal event + PHQ-9 / N-back / kitchensink event batches. |

## Provenance & follow-ups

Relocated from the Behaverse questionnaire project (`schemas/events`, v26.0605), **canonicalized to `event` (singular)** to match `trial` and the BDM convention. Realizes BDM deviations **D4** (this vocabulary), **D5** (`agent` → `actor`, applied), and **D6** (the scoping hierarchy).

- The ~50 `bdm:*` extension keys and their per-key shape contracts are documented in the source design note (`05e_events_vocabulary.md`) and should be relocated into this README or a `vocabulary/` resource.
- `result`/`context` are intentionally `additionalProperties: true` with `bdm:*`-prefixed extension keys; a tighter per-verb result contract is a follow-up.

## Versioning

CalVer `vYY.MMDD`. See the repo-wide [`VERSIONING.md`](../VERSIONING.md).
