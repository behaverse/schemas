# Behaverse Catalog Schema (WIP)

**Metadata schema for thematic catalogs of cognitive science datasets**

## Overview

The Behaverse Catalog Schema defines how to describe and organize **catalogs** of datasets that share specific characteristics or serve particular research applications. A catalog groups datasets by research focus, methodology, or population (e.g., "Multi-Task Studies", "Longitudinal Data", "Adolescent Mental Health").

The Behaverse `catalog` schema extends `https://schema.org/DataCatalog`. Furthermore, `catalog` is linked to `behaverse.org/schemas/dataset` in the sense that the properties required to define a catalog (e.g., "mental health", "adolescents") must be available as descriptors of a datasets.

Catalogs can be nested hierarchically—a catalog can contain child catalogs using the `catalogs` property, enabling multi-level organization (e.g., a "Mental Health" catalog containing "Pediatric Mental Health" and "Adult Mental Health" sub-catalogs).

- **Version**: v26.0107
- **Namespace**: `https://behaverse.org/schemas/catalog#`
- **Format**: JSON or JSON-LD
- **Status**: Active

## Quick Start

### Basic Example

```json
{
  "@context": "https://behaverse.org/schemas/catalog/context.jsonld",
  "name": "demo-multi-task",
  "pretty_name": "Demo: Multi-Task Cognitive Assessments",
  "description": "This is a demonstration example - datasets where participants completed multiple distinct cognitive tasks...",
  "inclusion_criteria": [
    "Participants must have completed 2 or more distinct cognitive tasks",
    "Tasks must measure different cognitive constructs"
  ],
  "datasets": [
    "https://example.org/datasets/demo-dataset-1",
    "https://doi.org/10.5555/example.12345"
  ]
}
```

### Nested Catalogs Example

```json
{
  "@context": "https://behaverse.org/schemas/catalog/context.jsonld",
  "name": "mental-health-data",
  "pretty_name": "Mental Health Research Data Catalog",
  "description": "A collection of datasets related to mental health research across populations.",
  "inclusion_criteria": [
    "Dataset must include mental health-related measures or diagnoses"
  ],
  "catalogs": [
    "https://behaverse.org/catalogs/pediatric-mental-health",
    "https://behaverse.org/catalogs/adult-mental-health"
  ]
}
```

## Core Fields

### Identity Fields

| Field | Type | Status | Description |
|-------|------|--------|-------------|
| `name` | string | **Required** | Short URL-friendly identifier (e.g., `demo-multi-task`, `demo-longitudinal`) |
| `pretty_name` | string | **Required** | Human-readable title (e.g., "Demo: Multi-Task Cognitive Assessments") |
| `description` | string | **Required** | Comprehensive description of the catalog's purpose and scope |
| `keywords` | array[string] | Recommended | Keywords describing the catalog's focus areas |

### Catalog Definition

| Field | Type | Status | Description |
|-------|------|--------|-------------|
| `inclusion_criteria` | array[string] | **Required** | Rules that datasets must meet to be included (ALL must be satisfied) |
| `exclusion_criteria` | array[string] | Optional | Criteria that would exclude a dataset from this catalog |

### Catalog Contents

| Field | Type | Status | Description |
|-------|------|--------|-------------|
| `datasets` | array[string] | Optional | List of dataset URLs or DOIs that belong to this catalog |
| `catalogs` | array[string] | Optional | List of child catalog URLs for hierarchical organization |
| `dataset_count` | integer | Optional | Number of datasets currently in this catalog |
| `related_catalogs` | array[string] | Optional | Names of other catalogs that frequently overlap |

### Metadata & Curation

| Field | Type | Status | Description |
|-------|------|--------|-------------|
| `date_created` | string | Recommended | Date catalog was created (ISO 8601: YYYY-MM-DD) |
| `date_modified` | string | Optional | Date catalog definition was last modified |
| `curator` | array[object] | Recommended | People or organizations that curate this catalog |

### Curator Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Curator full name or organization |
| `email` | string | No | Contact email |
| `orcid` | string | No | ORCID identifier (format: 0000-0000-0000-0000) |
| `affiliation` | string | No | Institutional affiliation |

## Detailed Property Reference

### name

**Type**: string  
**Status**: Required  
**Pattern**: `^[a-z0-9-_]+$` (lowercase, numbers, hyphens, underscores)  
**Description**: Short, unique identifier used in URLs and file names  
**Mapped to**: `schema:name`

**Examples**:
- `demo-multi-task`
- `demo-longitudinal`
- `demo-multimodal`
- `demo-adolescent-mental-health`

---

### pretty_name

**Type**: string  
**Status**: Required  
**Description**: Human-readable display title for the catalog  
**Mapped to**: `schema:name`

**Example**:
- "Demo: Multi-Task Cognitive Assessments"
- "Demo: Longitudinal & Test-Retest Studies"
- "Adolescent Mental Health"

---

### description

**Type**: string  
**Status**: Required  
**Description**: Comprehensive description of what the catalog represents and why it is useful  
**Mapped to**: `schema:description`, `dc:description`

**Example**:
```json
{
  "description": "Datasets where participants completed multiple distinct cognitive tasks or assessments within the same study, enabling cross-task analysis and cognitive profiling."
}
```

---

### keywords

**Type**: array of strings  
**Status**: Recommended  
**Description**: Keywords or tags that describe the catalog's focus areas  
**Mapped to**: `schema:keywords`

**Example**:
```json
{
  "keywords": [
    "demo-multi-task",
    "cognitive assessment",
    "battery",
    "neuropsychology",
    "cognitive profiling",
    "example",
    "demonstration"
  ]
}
```

---

### inclusion_criteria

**Type**: array of strings  
**Status**: Required  
**Description**: Specific rules that datasets must meet to be included. A dataset must satisfy ALL criteria to be included in the catalog.  
**Mapped to**: `behaverse:inclusionCriteria`

**Example**:
```json
{
  "inclusion_criteria": [
    "(Demo criteria) Participants must have completed 2 or more distinct cognitive tasks or assessments",
    "(Demo criteria) Tasks must measure different cognitive constructs (e.g., memory, attention, executive function)",
    "(Demo criteria) All tasks must be from the same participants (within-subject design)",
    "(Demo criteria) Both behavioral and neuroimaging multi-task datasets are eligible"
  ]
}
```

**Guidelines**:
- Be specific and measurable
- Use clear, objective criteria
- Avoid ambiguous terms
- Each criterion should be independently verifiable

---

### exclusion_criteria

**Type**: array of strings  
**Status**: Optional  
**Description**: Criteria that would explicitly exclude a dataset from this catalog  
**Mapped to**: `behaverse:exclusionCriteria`

**Example**:
```json
{
  "exclusion_criteria": [
    "Single-task studies",
    "Between-subject designs with no within-subject component",
    "Non-human animal studies"
  ]
}
```

---

### datasets

**Type**: array of strings (URLs)  
**Status**: Optional  
**Format**: URI (URLs or DOIs)  
**Description**: List of dataset URLs or DOIs that belong to this catalog. Use stable, resolvable identifiers like DOIs or canonical dataset URLs. This provides explicit membership rather than relying only on inclusion criteria.  
**Mapped to**: `schema:dataset`

**Example**:
```json
{
  "datasets": [
    "https://example.org/datasets/demo-dataset-1",
    "https://doi.org/10.5555/example.12345",
    "https://example.org/datasets/demo-dataset-2"
  ]
}
```

**Best Practices**:
- Use DOIs when available (most stable)
- Use canonical dataset URLs for datasets without DOIs
- Keep URLs resolvable (don't use local file paths)
- Update when datasets are added/removed from catalog

---

### catalogs

**Type**: array of strings (URLs)  
**Status**: Optional  
**Format**: URI  
**Description**: List of child catalog URLs for hierarchical organization. Enables nesting catalogs within catalogs.  
**Mapped to**: `schema:hasPart`, `dcat:catalog`

**Example**:
```json
{
  "catalogs": [
    "https://behaverse.org/catalogs/pediatric-mental-health",
    "https://behaverse.org/catalogs/adult-mental-health"
  ]
}
```

**Use Cases**:
- Organizing thematic sub-collections (e.g., "Neuroimaging in Pediatric Mental Health")
- Creating hierarchical data portals
- Federating multiple research group catalogs

---

### related_catalogs

**Type**: array of strings  
**Status**: Optional  
**Description**: Names (using `name` field) of other catalogs that frequently overlap or are related  
**Mapped to**: `behaverse:relatedCatalogs`

**Example**:
```json
{
  "related_catalogs": [
    "demo-multimodal",
    "demo-longitudinal",
    "demo-adult-mental-health"
  ]
}
```

---

### dataset_count

**Type**: integer  
**Status**: Optional  
**Description**: Number of datasets currently included in this catalog (may change over time)  
**Mapped to**: `behaverse:datasetCount`

**Example**:
```json
{
  "dataset_count": 15
}
```

---

### date_created

**Type**: string (ISO 8601 date)  
**Status**: Recommended  
**Format**: `YYYY-MM-DD`  
**Description**: Date when this catalog was first created  
**Mapped to**: `schema:dateCreated`

**Example**:
```json
{
  "date_created": "2025-12-02"
}
```

---

### date_modified

**Type**: string (ISO 8601 date)  
**Status**: Optional  
**Format**: `YYYY-MM-DD`  
**Description**: Date when the catalog definition was last modified  
**Mapped to**: `schema:dateModified`

**Example**:
```json
{
  "date_modified": "2025-12-15"
}
```

---

### curator

**Type**: array of objects  
**Status**: Recommended  
**Description**: People or organizations responsible for curating this catalog  
**Mapped to**: `schema:curator`

**Object Properties**:
- `name` (string, required): Curator's full name or organization name
- `email` (string, optional): Contact email address
- `orcid` (string, optional): ORCID identifier (format: `0000-0000-0000-0000`)
- `affiliation` (string, optional): Institutional affiliation

**Example**:
```json
{
  "curator": [
    {
      "name": "Jane Doe",
      "email": "jane.doe@example.edu",
      "orcid": "0000-0002-1234-5678",
      "affiliation": "Department of Psychology, Example University"
    },
    {
      "name": "Example Curator Team",
      "email": "curator@example.org"
    }
  ]
}
```

## Complete Example

```json
{
  "@context": "https://behaverse.org/schemas/catalog/context.jsonld",
  "name": "demo-longitudinal",
  "pretty_name": "Demo: Longitudinal & Test-Retest Studies",
  "description": "This is a demonstration - datasets where participants completed the same assessment(s) at multiple time points, enabling analysis of temporal dynamics, reliability, and developmental or intervention effects.",
  "keywords": [
    "demo-longitudinal",
    "test-retest",
    "reliability",
    "development",
    "intervention",
    "example",
    "demonstration"
  ],
  "inclusion_criteria": [
    "Participants must have data from 2 or more time points",
    "Same or equivalent measures collected at each time point",
    "Time between measurements can range from minutes (test-retest) to years (longitudinal)",
    "Must include sufficient sample overlap across time points (>50% retention recommended)"
  ],
  "exclusion_criteria": [
    "Cross-sectional studies with no repeated measures"
  ],
  "datasets": [
    "https://example.org/datasets/demo-dataset-1",
    "https://doi.org/10.5555/example.12345",
    "https://example.org/datasets/demo-dataset-2"
  ],
  "related_catalogs": [
    "demo-multi-task",
    "demo-adolescent-mental-health"
  ],
  "dataset_count": 3,
  "date_created": "2025-12-02",
  "curator": [
    {
      "name": "Example Curator",
      "email": "curator@example.org"
    }
  ]
}
```

## Validation

Validate your catalog metadata against the JSON Schema:

```bash
# Using ajv-cli
ajv validate -s https://behaverse.org/schemas/catalog/schema.json -d your-catalog.json

# Using Python
import json
import jsonschema
import requests

schema = requests.get('https://behaverse.org/schemas/catalog/schema.json').json()
with open('your-catalog.json') as f:
    data = json.load(f)
jsonschema.validate(data, schema)
```

## Best Practices

### Defining Inclusion Criteria

1. **Be Specific**: Criteria should be objective and measurable
   - ✅ "Participants must have completed 2 or more distinct cognitive tasks"
   - ❌ "Multiple tasks" (too vague)

2. **Be Independent**: Each criterion should stand alone
   - ✅ List each requirement separately
   - ❌ Combine multiple requirements in one criterion

3. **Be Comprehensive**: Cover all necessary aspects
   - Sample characteristics (if relevant)
   - Methodology requirements
   - Data type requirements
   - Design requirements

4. **Think AND Logic**: Datasets must meet ALL inclusion criteria
   - If you need OR logic, consider creating multiple catalogs

### Catalog Naming

- Use descriptive, memorable names
- Keep `name` field short and URL-friendly
- Make `pretty_name` clear and professional
- Be consistent with existing catalog names

### Organizing Catalogs

- Catalogs can overlap—datasets may belong to multiple catalogs
- Use `related_catalogs` to indicate frequent overlaps
- Use `catalogs` property for hierarchical nesting
- Consider both methodology (e.g., "multimodal") and domain (e.g., "adolescent-mental-health")

## Semantic Web & JSON-LD

This schema uses JSON-LD for semantic web integration. Properties are mapped to standard vocabularies:

- **Schema.org**: Core metadata properties (DataCatalog, Dataset)
- **DCAT**: W3C Data Catalog Vocabulary
- **Dublin Core**: Descriptive metadata
- **Behaverse**: Custom cognitive science properties

### Property URIs

Properties can be referenced using full URIs:

```
https://behaverse.org/schemas/catalog#name
https://behaverse.org/schemas/catalog#inclusion_criteria
https://behaverse.org/schemas/catalog#catalogs
```

### Using the Context

The `@context` provides short names for full URIs:

```json
{
  "@context": "https://behaverse.org/schemas/catalog/context.jsonld",
  "name": "demo-multi-task"
}
```

Expands to:

```json
{
  "https://schema.org/name": "demo-multi-task"
}
```

## Files in This Schema

- **field-definitions.yaml**: Source of truth for all field definitions
- **schema.json**: JSON Schema for validation
- **context.jsonld**: JSON-LD context for semantic web
- **README.md**: This documentation
- **examples/**: Example catalog files
- **scripts/**: Schema generation scripts

## Related Schemas

- **[Dataset Schema](../dataset/)**: For describing individual datasets
- **[bcsvw Schema](../bcsvw/)**: For describing CSV data files

## Version History

- **v26.0107** (2026-01-07): Renamed to Catalog, aligned with Schema.org DataCatalog
  - Renamed from "collection" to "catalog"
  - Changed base type from `schema:Collection` to `schema:DataCatalog`
  - Added `catalogs` property for hierarchical nesting
  - Renamed `related_collections` to `related_catalogs`
  - Updated `datasets` to use `schema:dataset` mapping

- **v25.1202** (2025-12-02): Initial release (as "collection")
  - Core identity and definition fields
  - Curator support
  - Examples and documentation

## AI Usage Disclosure

This document was created with assistance from AI tools.
