# Changelog — Behaverse Event Schema

All notable changes to the event schema are documented here. CalVer `vYY.MMDD`.

## [26.0608] - 2026-06-08

### Added

- Initial event schema in `behaverse/schemas`: an xAPI-style envelope (`actor`/`verb`/`object`) plus the canonical `bdm:` vocabulary — 24 verbs, 15 object types, 5 actor types.
- `field-definitions.yaml` (source: 11 envelope fields + the vocabulary) and generated `field-definitions.json` (the render contract).
- `schema.json` (JSON Schema Draft 2020-12, Event / EventBatch), `context.jsonld`, and `examples/` (minimal event + PHQ-9 / N-back / kitchensink batches).
- `scripts/generate.py` to regenerate `field-definitions.json`.

### Changed

- Relocated from the Behaverse questionnaire project (`schemas/events` v26.0605) and **canonicalized to `event` (singular)**: `$id` and namespace rewritten from `…/schemas/events/v26.0605` to `…/schemas/event/v26.0608`.
- Field named `actor` (not `agent`) from the outset — BDM deviation D5.

### Fixed

- Added the top-level `version` field (`"26.0608"`) to `schema.json`; it was missing, so the value now matches the `$id` and the convention used by bcsv/catalog/dataset.

### Notes

- Realizes BDM deviations D4 (canonical events vocabulary), D5 (`agent` → `actor`), D6 (scoping hierarchy).
- The ~50 `bdm:*` extension keys' per-key shape contracts (from the source design note) are a follow-up to relocate here.
