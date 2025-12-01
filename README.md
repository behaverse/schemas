# Behaverse Schemas

**custom schemas for cognitive and behavioral sciences**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Overview

This repository hosts machine-readable schemas and vocabularies for organizing, documenting, and sharing cognitive science data. All schemas are publicly accessible via GitHub Pages and aim to follow semantic web best practices.

**Base URL**: `https://behaverse.github.io/schemas/`

## Schemas

### dataset
Metadata schema for describing cognitive science related datasets.

- **Namespace**: `https://behaverse.github.io/schemas/dataset#`
- **Context**: [`dataset/context.jsonld`](dataset/context.jsonld)
- **JSON Schema**: [`dataset/schema.json`](dataset/schema.json)
- **Documentation**: [`dataset/README.md`](dataset/README.md)

**Example property reference**: `https://behaverse.github.io/schemas/dataset#sample_size`

### BCSVW (Behaverse CSV for the Web)
Extension of W3C CSVW with support for R/Python data types (factors, ordered factors, missing values, units).

- **Namespace**: `https://behaverse.github.io/schemas/bcsvw#`
- **Context**: [`bcsvw/context.jsonld`](bcsvw/context.jsonld)
- **JSON Schema**: [`bcsvw/schema.json`](bcsvw/schema.json)
- **Documentation**: [`bcsvw/README.md`](bcsvw/README.md)

**Example property reference**: `https://behaverse.github.io/schemas/bcsvw#ordered_factor`

### collection 
Schema for describing thematic collections of datasets.

- **Namespace**: `https://behaverse.github.io/schemas/collection#`
- **Context**: [`collection/context.jsonld`](collection/context.jsonld)
- **JSON Schema**: [`collection/schema.json`](collection/schema.json)
- **Documentation**: [`collection/README.md`](collection/README.md)

**Example property reference**: `https://behaverse.github.io/schemas/collection#inclusion_criteria`



## Using These Schemas

### In JSON-LD

Reference the context file to use short property names:

```json
{
  "@context": "https://behaverse.github.io/schemas/dataset/context.jsonld",
  "dataset_name": "my-cognitive-dataset",
  "description": "A study of working memory",
  "sample_size": 100,
  "cognitive_domains": ["working_memory", "attention"]
}
```

### In YAML (HuggingFace Dataset Cards)

Use simple field names--the JSON-LD context handles semantic mapping:

```yaml
dataset_name: my-cognitive-dataset
description: "A study of working memory"
sample_size: 100
cognitive_domains:
  - working_memory
  - attention
```

### For Validation

Validate your data against the JSON Schema:

```bash
# Using ajv-cli
ajv validate -s https://behaverse.github.io/schemas/dataset/schema.json -d your-dataset.json
```

### Referencing Individual Properties

Properties can be referenced like Schema.org terms:

```
https://behaverse.github.io/schemas/dataset#sample_size
https://behaverse.github.io/schemas/dataset#cognitive_domains
https://behaverse.github.io/schemas/bcsvw#ordered_factor
```

## Versioning

We use **Calendar Versioning (CalVer)** with the format: `vYY.MMDD[.dev#]`

- **Stable releases**: `v25.1201` (December 1, 2025)
- **Development versions**: `v25.1201.dev2` (second dev iteration on that date)

**Current versions** are in the root of each schema folder. **Historical versions** are archived in the `versions/` subfolder.

Example:
- Current: `dataset/context.jsonld`
- Archived: `dataset/versions/v25.1201/context.jsonld`

### Stability Promise

Property URIs remain stable across versions. For example, `https://behaverse.github.io/schemas/dataset#sample_size` will always refer to the same concept, even as the schema evolves.

## Repository Structure

```
behaverse/schemas/
├── dataset/              # Dataset metadata schema
│   ├── context.jsonld
│   ├── schema.json
│   ├── README.md
│   ├── examples/
│   └── versions/
├── bcsvw/               # BCSVW schema
│   ├── context.jsonld
│   ├── schema.json
│   ├── README.md
│   ├── examples/
│   └── versions/
├── collection/          # Collection schema
│   ├── context.jsonld
│   ├── schema.json
│   ├── README.md
│   ├── examples/
│   └── versions/
└── README.md
```



## Related Projects

- **[behaverse-data-catalog](https://github.com/behaverse/behaverse-data-catalog)**: Curated collection of cognitive science datasets using these schemas
- **[csvw](https://github.com/behaverse/csvw)**: Tools and examples for working with BCSVW


## License

These schemas are licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

You are free to:
- **Share**: Copy and redistribute the schemas
- **Adapt**: Remix, transform, and build upon the schemas

Under the following terms:
- **Attribution**: Give appropriate credit to Behaverse




## Contact

- **Issues**: [GitHub Issues](https://github.com/behaverse/schemas/issues)
- **Discussions**: [GitHub Discussions](https://github.com/behaverse/schemas/discussions)
- **Organization**: [Behaverse on GitHub](https://github.com/behaverse)

## Acknowledgments

These schemas build upon and reference established standards including:
- [Schema.org](https://schema.org/)
- [W3C CSVW](https://www.w3.org/TR/tabular-data-primer/)
- [Dublin Core](https://www.dublincore.org/)
- [BIDS](https://bids-specification.readthedocs.io/)
- [DataCite](https://schema.datacite.org/)
