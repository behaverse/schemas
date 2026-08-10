#!/usr/bin/env python3
"""The schema-family manifest — the single place that lists what this repo publishes.

Adding a family used to mean editing three lists that could silently disagree:
`scripts/generate.py`, `scripts/validate_schemas.py`, and `SCHEMA_DIRS` in
`.github/workflows/build-deploy-pages.yml`. The two Python scripts now import this
module, and `validate_schemas.py` checks the workflow's list against it, so a family
cannot be deployed-but-unvalidated (or validated-but-undeployed) by accident.

Per family:
  source                  'linkml' | 'json' | 'terms' — where the source of truth lives
  emits_context           publishes context.jsonld
  emits_field_definitions publishes field-definitions.json (the docs render artifact)
  has_schema_json         publishes schema.json (so it can be JSON-Schema-validated)
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent

FAMILIES: List[Dict[str, Any]] = [
    # name          source     context  field_defs  schema.json
    {"name": "agents", "source": "linkml", "emits_context": False,
     "emits_field_definitions": True, "has_schema_json": True},
    {"name": "devices", "source": "linkml", "emits_context": False,
     "emits_field_definitions": True, "has_schema_json": True},
    {"name": "bcsv", "source": "json", "emits_context": True,
     "emits_field_definitions": False, "has_schema_json": True},
    {"name": "catalog", "source": "linkml", "emits_context": True,
     "emits_field_definitions": False, "has_schema_json": True},
    {"name": "dataset", "source": "linkml", "emits_context": True,
     "emits_field_definitions": False, "has_schema_json": True},
    {"name": "studyflow", "source": "linkml", "emits_context": False,
     "emits_field_definitions": True, "has_schema_json": True},
    {"name": "trial", "source": "linkml", "emits_context": True,
     "emits_field_definitions": True, "has_schema_json": True},
    {"name": "event", "source": "linkml", "emits_context": True,
     "emits_field_definitions": True, "has_schema_json": True},
    {"name": "timeseries", "source": "linkml", "emits_context": False,
     "emits_field_definitions": True, "has_schema_json": True},
    {"name": "vocabulary", "source": "terms", "emits_context": False,
     "emits_field_definitions": False, "has_schema_json": False},
]

# `bcsv` is hand-maintained JSON and `vocabulary` is SKOS terms.yaml with its own generator,
# so neither is generated from LinkML here; both are still deployed, linted, and
# version-checked. Every LinkML family publishes a schema.json.
GENERATED = [f for f in FAMILIES if f["source"] == "linkml"]

NAMES = [f["name"] for f in FAMILIES]
SCHEMA_JSON = [f["name"] for f in FAMILIES if f["has_schema_json"]]
CONTEXTS = [f["name"] for f in FAMILIES if f["emits_context"]]
