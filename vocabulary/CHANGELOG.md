# Vocabulary Changelog

All notable changes to the vocabulary (SKOS concept schemes + concepts) will be
documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses [Calendar Versioning](https://calver.org/) (YY.MMDD).

## [26.0809] - 2026-08-09

### Added

- **`source`** (general scheme): the device/stream identifier the event layer already
  carried on `bdm:recording_started` but the vocabulary never defined. Documented as the
  join key across layers: recording events, discrete events of the same device, and the
  timeseries sidecar's `source` field.

## [26.0808] - 2026-08-08

### Changed

- The `*_hash` term's note now states the corpus default: SHA-256, lowercase hexadecimal (64 characters), matching `bcsv.file_hash` and the `sha256` fields of the timeseries sidecar and event attachments. The previous note was internally wrong: its "CRC32" example was 32 hex characters (MD5 length; CRC32 is 8) and its "SHA256 (base64)" example was a 56-character hex string (SHA-224 length).

## [26.0727] - 2026-07-27

### Changed
- **`anchor_datetime` is recorded once per runtime instance, not once per session.**
  `engine_seconds` counts from engine start, so a restart begins a new clock and
  therefore a new anchor — and a session may contain several runs. The definition
  now says so; the anchor's home in the data is the trial schema's `Studyflow`
  table (v26.0727).
- First `versions/` snapshot published for the vocabulary (`versions/v26.0727/`);
  earlier releases were never archived.

## [26.0721] - 2026-07-21

### Added
- **`time` scheme** — clock and timing terms for raw data acquisition:
  `engine_seconds` (monotonic per-session clock, seconds since engine start),
  `anchor_datetime` (the RFC 9557 datetime at `engine_seconds` = 0; the single
  per-session bridge to wall-clock time), and `t` (per-sample time in seconds on
  the declared clock; events may carry it as the optional `bdm:t` extension).

### Changed
- **`bdm:` prefix unified** to `https://behaverse.org/schemas/vocabulary/`
  (was `…/schemas/vocabulary#` here, while the event schema bound the same
  prefix to `…/data-model/vocab/` — two namespaces under one prefix). One
  resolvable namespace, full word "vocabulary", now serves the whole ecosystem;
  the event schema adopts the same binding in its v26.0721. Compact JSON forms
  (`data_type`, `status`, `bdm:*` strings) are unchanged; only expanded RDF IRIs
  move (`…vocabulary#dataType` → `…vocabulary/dataType`).

## [26.0703] - 2026-07-03

### Fixed
- `terms.jsonld` was invalid JSON-LD: its context aliased both `schemes` and
  `concepts` to `@graph`, which JSON-LD 1.1 processors reject as "colliding
  keywords" — pyld could not expand the document at all. The two keys now map to
  distinct containment properties (`bdm:schemes` / `bdm:concepts`, `@container:
  @set`). **The JSON shape is unchanged** (consumers still read `schemes` and
  `concepts` arrays); only the RDF expansion differs: scheme/concept nodes are now
  linked from the vocabulary node via those properties instead of being asserted
  as (unreachable, since expansion failed) default-graph nodes.
- CI now expands `terms.jsonld` with pyld on every run, so this class of bug
  cannot ship again.

### Notes
- This is the vocabulary's first CHANGELOG entry; earlier releases (`26.0611` and
  before) predate it. See the git history of `terms.yaml` for prior changes.
