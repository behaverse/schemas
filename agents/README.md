# Behaverse Agents Schema

**Version:** v26.0804
**Namespace:** `https://behaverse.org/schemas/agents#`

## Overview

The agents schema specifies `agents.csv`, the agent roster at the root of every BDM
dataset: one row per agent, mapping the dataset-local `agent_index` (which names the
agent's data folder, e.g. `agent_015`) to the global `agent_id` (which identifies the
agent across studies), plus a small core of optional per-agent attributes (`agent_type`,
`age`, `sex`, `language`). Datasets may add custom columns; the schema defines the shared
core.

Every table that carries an `agent_id` — such as `Response` and `StudyflowLog` in the
[`trial`](../trial/) schema — resolves it against this roster. Per-agent data
availability is deliberately not recorded here: it is derivable from each agent's
`studyflow_log.csv`.

## Files

- `schema.linkml.yaml`: The LinkML source of truth. Edit it, then run
  `python scripts/generate.py`.

## Artifacts

| File | Status | Purpose |
|------|--------|---------|
| [`schema.linkml.yaml`](schema.linkml.yaml) | ✅ | Source of truth (LinkML). |
| [`schema.json`](schema.json) | ✅ generated | JSON Schema validation contract for an agents document (tables as arrays of row objects). |
| [`field-definitions.json`](field-definitions.json) | ✅ generated | Render contract, so the documentation sites can generate this family's reference. |

## Validating a document

`schema.json` validates the JSON representation of the roster (rows as objects under the
`Agent` key):

```bash
.venv/bin/python - <<'EOF'
import json, jsonschema
doc = {"Agent": [{"agent_id": "20025fe6-6868-47c6-a222-a5c06b49c8db",
                  "agent_index": "agent_001", "agent_type": "human"}]}
jsonschema.validate(doc, json.load(open("agents/schema.json")))
print("valid")
EOF
```
