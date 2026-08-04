# Behaverse Devices Schema

**Version:** v26.0810
**Namespace:** `https://behaverse.org/schemas/devices#`

## Overview

The devices schema specifies `devices.csv`, the device roster at the root of a BDM dataset:
one row per recording device, holding **device-lifetime** facts — platform and OS, display
geometry (size, resolution, refresh rate, pixel ratio), pixel-density calibration with its
method and provenance, and capabilities (camera, microphone, touch, input devices). Physical
lengths are centimetres.

Runs reference their device through the trial family's `StudyflowLog.device_id`.
**Run-lifetime** facts deliberately stay on the run log: the recording engine
(`engine_name`/`engine_version`) and the viewing distance (`screen_distance` — posture is a
property of the sitting, not the hardware). A calibration belongs to the device, which is
what lets a participant calibrate once rather than at every session; refusal to calibrate is
recorded (`declined`), distinct from absence.

## Files

- `schema.linkml.yaml`: The LinkML source of truth. Edit it, then run
  `python scripts/generate.py`.

## Artifacts

| File | Status | Purpose |
|------|--------|---------|
| [`schema.linkml.yaml`](schema.linkml.yaml) | ✅ | Source of truth (LinkML). |
| [`schema.json`](schema.json) | ✅ generated | JSON Schema validation contract for a devices document (tables as arrays of row objects). |
| [`field-definitions.json`](field-definitions.json) | ✅ generated | Render contract, so the documentation sites can generate this family's reference. |

## Validating a document

`schema.json` is a standard JSON Schema; any validator works (requires
`pip install jsonschema`):

```bash
python3 -c "import json, jsonschema; jsonschema.validate({'Device': [{'device_id': 'dev-01', 'platform': 'linux', 'screen_size_cm': [53.1, 29.9]}]}, json.load(open('devices/schema.json'))); print('valid')"
```

The published schema is at `https://behaverse.org/schemas/devices/schema.json` (pin a
`versions/v<VERSION>/` URL for production use — see [`../VERSIONING.md`](../VERSIONING.md)).
