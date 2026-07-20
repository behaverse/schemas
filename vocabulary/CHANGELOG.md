# Vocabulary Changelog

All notable changes to the vocabulary (SKOS concept schemes + concepts) will be
documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses [Calendar Versioning](https://calver.org/) (YY.MMDD).

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
