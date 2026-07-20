# Changelog — Behaverse Event Schema

All notable changes to the event schema are documented here. CalVer `vYY.MMDD`.

## [26.0721] - 2026-07-21

### Breaking

- **`Attachment` formalized** (was an unconstrained `linkml:Any`): each attachment now requires `type` (a `bdm:` term such as `bdm:Timeseries`), `contentType` (MIME), and `url`, with optional `sha256` (SHA-256, validated pattern), `length` (bytes), and `description`. Addressing rule: `url` is a relative path resolved against the location of the file containing the reference, or an absolute URL. Field names follow xAPI's attachment conventions where a standard name exists (`contentType`, `length`). Documents with previously arbitrary attachment shapes no longer validate.
- **`bdm:` prefix rebound** to `https://behaverse.org/schemas/vocabulary/` (was `https://behaverse.org/data-model/vocab/`), unifying the ecosystem on one resolvable vocabulary namespace (see vocabulary v26.0721). Compact JSON forms (`"bdm:key_pressed"`, extension keys) are unchanged; only JSON-LD-expanded RDF IRIs move.

### Added

- The kitchensink example's mouse `bdm:recording_ended` event now carries an `attachments` entry demonstrating the formalized shape (pointing at a timeseries sidecar file).
- README: attachment addressing rule and the clock-mapping note (`timestamp = anchor_datetime + t`; optional `bdm:t` context extension), referencing the vocabulary `time` scheme.

## [26.0720] - 2026-07-20

### Added

- **`bdm:key_released`** interaction verb (objects: `bdm:UIComponent`, `bdm:Stimulus`) — the release counterpart to `bdm:key_pressed`, so a pure event stream can express a key release (press duration derives from the paired press/release timestamps). The trial `Input` table already modeled releases (`key-release` in `input_action_type`, press duration in `duration`); the event vocabulary could not. 25 verbs total.

### Fixed

- `kitchensink_event_batch.json` used `bdm:sha256` where the `bdm:recording_ended` verb documents `bdm:recording_sha256`; the example now matches the documented key. The kitchensink also gains a `bdm:key_released` event, keeping its all-verbs coverage.

### Documentation

- **Events-at-rest decision recorded** (README "Storage" section): the canonical at-rest representation of the events layer in a BDM dataset is **NDJSON** — one `Event` object per line, UTF-8, append-only, `events_<attempt>.ndjson[.gz]` in the dataset's activity folder beside the trial tables. `EventBatch` is the interchange shape, not the at-rest format; derived copies (e.g. Parquet) are permitted; engines with private compact recording formats must document a lossless mapping to canonical `Event` objects. Added `examples/events.ndjson` (every line schema-validated). No schema change — this is a storage convention over the existing `Event` model.

## [26.0615] - 2026-06-15

### Changed

- **Source of truth switched to LinkML** (`schema.linkml.yaml`). `schema.json`, `context.jsonld`, and `field-definitions.json` are now generated from this single source via `scripts/generate.py`, matching the catalog/dataset/trial pipeline.
- **`schema.json` redesigned** as an abstract root `EventDocument = Event | EventBatch` (a root `oneOf` over the two concrete subclasses), replacing the hand-crafted `oneOf`. `Event` is a single event/statement; `EventBatch` is `{batch_id?, events: [Event]}` — mirroring an API (GET /id → one Event, GET collection → a batch).
- The canonical `bdm:` vocabulary and the JSON-LD `@context` are now LinkML-sourced (carried as schema-level `vocabularies` and `context_overrides` annotations) rather than hand-maintained.

### Added

- **Enum validation** for `verb` (`VerbEnum`), `actor.objectType` (`ActorTypeEnum`), and `object.objectType` (`ObjectTypeEnum`), drawn from the canonical vocabulary.

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
