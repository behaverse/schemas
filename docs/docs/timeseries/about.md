---
sidebar_position: 2
---

<!-- THIS FILE IS MANUALLY EDITABLE (hand-written About; the Overview and per-property pages are generated) -->

# About

## Motivation

Behavioral experiments increasingly record **continuous signals** alongside discrete responses: mouse trajectories, gaze position, EEG. The Behaverse Data Model's rule for such signals is *referenced, never inlined* — the raw samples are too dense and homogeneous to live inside event records or trial tables. That rule creates a need this schema fills: a standard, machine-readable way to describe the referenced file, so any consumer can interpret it without guessing at its clock, units, or layout.

## Features

**A sidecar, not a payload format.** The schema validates a small JSON *sidecar* document (`<payload-filename>.timeseries.json`) that sits beside the signal file. The payload itself may be NDJSON, CSV, EDF, Parquet — whatever suits the domain — declared via `content_type`. The sidecar carries what the payload cannot say for itself: which clock the sample times are on, whether sampling is event-driven or fixed-rate, what each channel means.

**Channels are the primitive.** A mouse trajectory (`t`, `x`, `y`), a gaze stream, and a 64-channel EEG all have the same shape: a payload plus a list of channel definitions (name, datatype, unit, optional coordinate frame). There is no class per modality — a "2-D position series" is simply the profile of channels `t` + `x` + `y` with a declared coordinate frame (`screen_px` or `viewport_fraction`, mirroring the trial Input table's `x_screen`/`x_viewport` distinction).

**One clock, one bridge.** Sample times are expressed on a declared monotonic clock — by default the vocabulary term `engine_seconds` (seconds since recording-engine start). A single per-session `anchor_datetime` bridges the monotonic clock to wall-clock time.

**Discoverable from events.** An event stream references a timeseries through its `attachments`: the attachment points at the sidecar, the sidecar's `content_url` points at the payload. Metadata is always one hop away.

## Relationship to standards

The sidecar borrows familiar ideas rather than inventing new ones: MIME `content_type` declarations, SHA-256 content hashing, and per-channel unit/datatype declarations in the spirit of bcsv's column metadata. Domain container formats (e.g. EDF for EEG) remain authoritative for their internal calibration details; the sidecar mirrors only what consumers need without parsing the container.

## Namespace

`https://behaverse.org/schemas/timeseries#`

## Next

- **[Overview](/timeseries)** — all sidecar properties.
- Worked examples (an event-driven NDJSON mouse trajectory and a fixed-rate EDF EEG) ship in the repository's [`examples/`](https://github.com/behaverse/schemas/tree/main/timeseries/examples) directory.
