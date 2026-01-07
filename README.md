# Behaverse Schemas (WIP)

**custom schemas for cognitive and behavioral sciences**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Overview

This repository hosts machine-readable schemas and vocabularies for organizing, documenting, and sharing cognitive science data. All schemas are publicly accessible via GitHub Pages and aim to follow semantic web best practices.

**Base URL**: `https://behaverse.org/schemas/`

## Schemas

### <img src="assets/img/schema_B.png" height="40" style="vertical-align: middle;"> bcsvw (Behaverse CSV for the Web)
Extension of W3C CSVW with support for R/Python data types including categorical and ordered factors, missing value codes, units of measurement, and file integrity verification.

- **Version**: v25.1201
- **Namespace**: `https://behaverse.org/schemas/bcsvw#`
- **Context**: [`bcsvw/context.jsonld`](bcsvw/context.jsonld)
- **JSON Schema**: [`bcsvw/schema.json`](bcsvw/schema.json)
- **Documentation**: [`bcsvw/README.md`](bcsvw/README.md)

**Example property reference**: `https://behaverse.org/schemas/bcsvw#ordered`

### <img src="assets/img/schema_C.png" height="40" style="vertical-align: middle;"> catalog 
Metadata schema for describing thematic catalogs of datasets that share specific characteristics or serve particular research applications. Extends schema.org/DataCatalog. Supports hierarchical organization through nested catalogs.

- **Version**: v26.0107
- **Namespace**: `https://behaverse.org/schemas/catalog#`
- **Context**: [`catalog/context.jsonld`](catalog/context.jsonld)
- **JSON Schema**: [`catalog/schema.json`](catalog/schema.json)
- **Documentation**: [`catalog/README.md`](catalog/README.md)

**Example property reference**: `https://behaverse.org/schemas/catalog#inclusion_criteria`

### <img src="assets/img/schema_D.png" height="40" style="vertical-align: middle;"> dataset
Metadata schema for describing cognitive science datasets with comprehensive coverage of participant demographics, measurement techniques, cognitive tasks, and data access information.

- **Version**: v25.1201
- **Namespace**: `https://behaverse.org/schemas/dataset#`
- **Context**: [`dataset/context.jsonld`](dataset/context.jsonld)
- **JSON Schema**: [`dataset/schema.json`](dataset/schema.json)
- **Documentation**: [`dataset/README.md`](dataset/README.md)

**Example property reference**: `https://behaverse.org/schemas/dataset#sample_size`

### <img src="assets/img/schema_S.png" height="40" style="vertical-align: middle;"> studyflow
Schema for defining the formal structure of studyflow diagrams - sequences of activities and resources designed to facilitate experimental research and data analysis. Used by the Studyflow Modeler app.

- **Version**: v25.0414
- **Namespace**: `https://behaverse.org/schemas/studyflow#`
- **LinkML Schema**: [`studyflow/schema.linkml.yaml`](studyflow/schema.linkml.yaml)
- **Documentation**: [`studyflow/README.md`](studyflow/README.md)

**Related**: [Studyflow Modeler Documentation](https://behaverse.org/studyflow-modeler/docs)

## Versioning

We use **Calendar Versioning (CalVer)** with the format: `vYY.MMDD[.dev#]`

- **Stable releases**: `v25.1201` (December 1, 2025)
- **Development versions**: `v25.1201.dev2` (second dev iteration on that date)

**Current versions** are in the root of each schema folder. **Historical versions** are archived in the `versions/` subfolder.

Example:
- Current: `dataset/context.jsonld`
- Archived: `dataset/versions/v25.1201/context.jsonld`

### Stability Promise

Property URIs remain stable across versions. For example, `https://behaverse.org/schemas/dataset#sample_size` will always refer to the same concept, even as the schema evolves.

## Repository Structure

```
behaverse/schemas/
├── bcsvw/               # bcsvw schema
│   ├── context.jsonld
│   ├── schema.json
│   ├── README.md
│   ├── examples/
│   └── versions/
├── catalog/             # catalog schema (DataCatalog)
│   ├── context.jsonld
│   ├── schema.json
│   ├── README.md
│   ├── examples/
│   └── versions/
├── dataset/             # dataset metadata schema
│   ├── context.jsonld
│   ├── schema.json
│   ├── README.md
│   ├── examples/
│   └── versions/
├── studyflow/           # studyflow schema
│   ├── schema.moddle.json
│   ├── schema.linkml.yaml
│   ├── templates.json
│   └── README.md
└── README.md
```

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
- [W3C DCAT](https://www.w3.org/TR/vocab-dcat-3/)
- [Dublin Core](https://www.dublincore.org/)
- [BIDS](https://bids-specification.readthedocs.io/)
- [DataCite](https://schema.datacite.org/)

## AI Usage Disclosure 

This document was created with assistance from AI tools.