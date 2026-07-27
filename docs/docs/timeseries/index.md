---
id: index
title: timeseries
sidebar_label: Overview
slug: /timeseries
---

<!-- THIS FILE IS AUTO-GENERATED. DO NOT EDIT MANUALLY. -->

# timeseries

**Version**: v26.0727  
**Namespace**: `https://behaverse.org/schemas/timeseries`

Sidecar metadata for continuous sampled signals (mouse trajectories, gaze, EEG). A small JSON document — named `<payload-filename>.timeseries.json`, stored beside its payload in the dataset's activity folder — declaring the payload's location, encoding, clock, sampling nature, and channels. Referenced from event streams via `attachments` (type `bdm:Timeseries`).

## Properties

This schema defines **16 properties** for describing timeseries metadata.

### All Properties

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [type](timeseries/type) | `string` | required | Discriminator for the document kind; always `bdm:Timeseries`. |
| [name](timeseries/name) | `string` | optional | Short machine-friendly name of the series (e.g. `mouse_trajectory`, `gaze`, `eeg... |
| [description](timeseries/description) | `string` | optional | Human-readable description of what was recorded and how. |
| [content_url](timeseries/content_url) | `string` | required | Where the payload file lives: a relative path resolved against this sidecar's ow... |
| [content_type](timeseries/content_type) | `string` | required | MIME type of the payload (e.g. `application/x-ndjson`, `text/csv`, `application/... |
| [content_encoding](timeseries/content_encoding) | `string` | optional | Optional transport encoding of the payload file, e.g. `gzip`. Absent means the p... |
| [sha256](timeseries/sha256) | `string` | optional | SHA-256 hash of the payload file's bytes (after any content_encoding), lowercase... |
| [byte_length](timeseries/byte_length) | `integer` | optional | Size of the payload file in bytes (after any content_encoding). |
| [clock](timeseries/clock) | `string` | optional | URI of the clock every `t` value is on. Defaults to the vocabulary `engine_secon... |
| [anchor_datetime](timeseries/anchor_datetime) | `string` | optional | The RFC 9557 datetime (with timezone offset) corresponding to `t` = 0 on the dec... |
| [sampling_nature](timeseries/sampling_nature) | `enum` | required | Whether samples are event-driven (irregular) or taken at a nominal fixed rate. |
| [nominal_rate_hz](timeseries/nominal_rate_hz) | `number` | optional | Nominal sampling rate in Hz. Required when `sampling_nature` is `sampled`; meani... |
| [runtime_id](timeseries/runtime_id) | `string` | optional | Identifies the activity run (one specific execution of an activity by one agent,... |
| [session_uuid](timeseries/session_uuid) | `string` | optional | UUID of the session this series was recorded in (see the trial schema's `session... |
| [attempt](timeseries/attempt) | `integer` | optional | 1-based ordinal of the activity run within the session (see `attempt` in the tri... |
| [channels](timeseries/channels) | `array` | required | Definitions of the payload's channels, in payload column order. For self-describ... |

## Usage

See the [examples](./timeseries/examples) for practical usage patterns.

## Version History

The current version of `timeseries` is `v26.0727`.

Older versions are available in the [`timeseries/versions/`](https://github.com/behaverse/schemas/tree/main/timeseries/versions) directory.
