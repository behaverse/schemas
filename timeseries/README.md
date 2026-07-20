# Behaverse Timeseries Schema

**Version:** v26.0721
**Namespace:** `https://behaverse.org/schemas/timeseries#`
**Source of truth:** [`schema.linkml.yaml`](schema.linkml.yaml) — edit it, then run `python scripts/generate.py`

## Overview

Sidecar metadata for **continuous sampled signals** — mouse trajectories, gaze, EEG, and other timeseries recorded alongside behavioral data. Per the Behaverse Data Model, continuous signals are *referenced, never inlined*: the raw samples live in a domain-appropriate payload file, and this schema validates the small JSON **sidecar** that describes it.

**Channels are the primitive.** A mouse trajectory (`t`, `x`, `y`), a gaze stream, and a 64-channel EEG are all the same shape — a payload plus a list of channel definitions (name, datatype, unit, optional coordinate frame). There is no class per modality; a "2-D position series" is just the profile below.

## The sidecar + payload model

| Piece | What it is | Validated? |
|---|---|---|
| **Payload** (`mouse_1.ndjson.gz`, `eeg_1.edf`, …) | The samples, in any declared format: NDJSON (objects keyed by channel name), CSV, EDF, Parquet, … | No — declared via `content_type` |
| **Sidecar** (`<payload-filename>.timeseries.json`) | This schema's document: payload location + encoding + hash, clock, sampling nature, channels | Yes — against [`schema.json`](schema.json) |

- **Naming:** the sidecar is named after the payload file *as it exists on disk*, with `.timeseries.json` appended (`mouse_1.ndjson.gz` → `mouse_1.ndjson.gz.timeseries.json`).
- **Placement:** both sit in the dataset's activity folder beside the trial tables, partitioned by attempt (`response_1.csv` ↔ `mouse_1.ndjson.gz`), per the dataset layout.
- **Linkage from events:** an event's `attachments` entry points at the **sidecar** (`type: "bdm:Timeseries"`, `contentType: "application/json"`); the sidecar's `content_url` points at the payload. One uniform reference chain — metadata is always discoverable.
- `content_url` follows the same addressing rule as event attachments: a relative path resolved against the referencing file's own location, or an absolute URL.

## Clocks

Every `t` value is on the sidecar's declared `clock` — by default the vocabulary term [`engine_seconds`](https://behaverse.org/schemas/vocabulary): a **monotonic** per-session clock counting seconds since engine start. `anchor_datetime` (RFC 9557) is the single per-session bridge to wall-clock time (`datetime = anchor + t`); it may be duplicated into the sidecar to make it standalone.

## Sampling

- `sampling_nature: event_driven` — a sample per occurrence (pointer move); the payload **must** contain a `t` channel.
- `sampling_nature: sampled` — nominal fixed rate; `nominal_rate_hz` **required**; a `t` channel is optional (times derive from index × rate).

## Profile: 2-D position series (mouse, gaze)

Channels `t` (float, `s`) + `x` + `y` (float, one `coordinate_frame` ∈ `screen_px` | `viewport_fraction` — mirroring the trial Input table's `x_screen`/`x_viewport` distinction). See [`examples/mouse_1.ndjson.gz.timeseries.json`](examples/mouse_1.ndjson.gz.timeseries.json); the EEG sidecar ([`examples/eeg_1.edf.timeseries.json`](examples/eeg_1.edf.timeseries.json)) shows the N-channel case over a self-describing container.

## Artifacts

| File | Status | Purpose |
|------|--------|---------|
| [`schema.linkml.yaml`](schema.linkml.yaml) | ✅ | Source of truth (LinkML). |
| [`schema.json`](schema.json) | ✅ generated | JSON Schema (validation contract for sidecars). |
| [`examples/`](examples/) | ✅ | Mouse (event-driven NDJSON) and EEG (sampled EDF) sidecars. |

## Versioning

CalVer `vYY.MMDD`. See the repo-wide [`VERSIONING.md`](../VERSIONING.md).
