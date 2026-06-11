# Behaverse Vocabulary

Cross-cutting controlled terminology for behaverse data: general terms (e.g. `accuracy`,
`response_time`), demographics, and the suffix conventions used in variable names
(generic, aggregation, transformation, and referencing suffixes).

This is a **terminology resource** (SKOS concept schemes + concepts), not a JSON Schema.
Terms that one schema owns — e.g. the trial table fields or the event envelope — live in
that schema's `field-definitions.yaml`; this resource holds only the terms no single
schema owns.

## Files

| File | Role |
|---|---|
| `terms.yaml` | **Source of truth.** Concept schemes + concepts. Edit this. |
| `terms.jsonld` | Generated SKOS JSON-LD serialization. Readable as plain JSON. |
| `scripts/generate.py` | `terms.yaml` → `terms.jsonld`. CI checks it is in sync (`--check`). |

Published at `https://behaverse.org/schemas/vocabulary/terms.jsonld`.

## Structure

- **Schemes** group concepts (General, Demographics, Generic Suffixes, …). Schemes or
  concepts marked `status: internal` are kept for reference but excluded from the public
  BDM glossary.
- **Concepts** carry `label`, `definition`, and optionally `data_type`, `range`, and
  `notes`.

## Consumers

The BDM glossary page ([behaverse.org/data-model/glossary](https://behaverse.org/data-model/glossary/))
is a generated merge-view: it renders these concepts together with field terms harvested
from each schema's `field-definitions.json`.

## Editing

```bash
# edit terms.yaml, then:
uv run scripts/generate.py
```

Seeded from behaverse/data-model's pre-redesign `glossary.yml` (the old Google-Sheet
export), restructured into schemes + concepts.
