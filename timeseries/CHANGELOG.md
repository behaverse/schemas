# Changelog — Behaverse Timeseries Schema

All notable changes to the timeseries schema are documented here. CalVer `vYY.MMDD`.

## [26.0803] - 2026-08-03

### Added

- `field-definitions.json` now publishes each enum-ranged field's value set as
  `values` (a list of `{value, description?}` objects) plus `values_exhaustive` —
  the artifact-shape addition introduced with trial v26.0803, applied uniformly to
  every family that ships `field-definitions.json`. Three fields gain it
  (`sampling_nature`, channel `datatype`, `coordinate_frame`). `schema.json`
  validation is unchanged.
- Every field now publishes a non-null `type`, derived from its LinkML range (`enum`,
  `string`, `integer`, `datetime`, `list of Channel`, …) when no explicit `bdm_type`
  annotation exists. All 21 fields previously carried `type: null`, leaving the
  documentation site's Type column empty. Requested by `behaverse/data-model`.

## [26.0729] - 2026-07-29

### Added

- **`field-definitions.json` is now published** for this family, so documentation sites can render a generated reference instead of hand-written prose that drifts. It carries two sections — `TimeseriesMetadata` (the sidecar's own fields) and `Channel` — plus each section's `slug` and `docs_url`.
  - This required teaching the emitter that a `tree_root` class is only skipped when it is a *pure container* of other classes (as `trial`'s `TrialData` is). `TimeseriesMetadata` is the tree root **and** the content, so skipping it would have published a reference containing only `Channel`.

## [26.0727] - 2026-07-27

### Added

- **`runtime_id`** (optional) — identifies the activity run the series was recorded during, resolving in the trial schema's new `Studyflow` table and equal to the event layer's `bdm:runtime_id`. A sidecar can now be tied to its run without relying on where the file sits. Both examples updated.

### Changed

- `attempt`'s description now defines it against `Studyflow.attempt` and explains why timeseries payloads keep a per-run filename while the tidy tables and the event stream do not: unlike those, a binary recording cannot be concatenated into a single file.

## [26.0721] - 2026-07-21

### Added

- **Initial release.** Sidecar-metadata schema for continuous sampled signals: `TimeseriesMetadata` (payload reference `content_url`/`content_type`/`content_encoding`/`sha256`/`byte_length`; `clock` defaulting to the vocabulary `engine_seconds` term; optional `anchor_datetime`; `sampling_nature` `event_driven`|`sampled` with `nominal_rate_hz`; optional `session_uuid`/`attempt` scoping) + `Channel` definitions (`name`, `datatype`, `unit`, optional `coordinate_frame` ∈ `screen_px`|`viewport_fraction`). Channels are the primitive — mouse/gaze/EEG share one shape; the 2-D position profile is documented in the README. Sidecars are named `<payload-filename>.timeseries.json`, live beside their payload in the activity folder, and are referenced from event `attachments` (type `bdm:Timeseries`).
