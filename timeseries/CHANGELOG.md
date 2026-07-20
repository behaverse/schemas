# Changelog — Behaverse Timeseries Schema

All notable changes to the timeseries schema are documented here. CalVer `vYY.MMDD`.

## [26.0721] - 2026-07-21

### Added

- **Initial release.** Sidecar-metadata schema for continuous sampled signals: `TimeseriesMetadata` (payload reference `content_url`/`content_type`/`content_encoding`/`sha256`/`byte_length`; `clock` defaulting to the vocabulary `engine_seconds` term; optional `anchor_datetime`; `sampling_nature` `event_driven`|`sampled` with `nominal_rate_hz`; optional `session_uuid`/`attempt` scoping) + `Channel` definitions (`name`, `datatype`, `unit`, optional `coordinate_frame` ∈ `screen_px`|`viewport_fraction`). Channels are the primitive — mouse/gaze/EEG share one shape; the 2-D position profile is documented in the README. Sidecars are named `<payload-filename>.timeseries.json`, live beside their payload in the activity folder, and are referenced from event `attachments` (type `bdm:Timeseries`).
