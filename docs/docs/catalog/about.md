---
id: about
title: About
sidebar_label: About
---

<!-- THIS FILE IS MANUALLY EDITABLE -->

# <img src={require('@site/static/assets/img/schema_C.png').default} height="80" style={{verticalAlign: 'middle'}} /> About catalog

The Behaverse catalog Schema provides a standardized way to describe and organize thematic catalogs of cognitive science and neuroscience datasets.

## Motivation

Research datasets are often more valuable when organized into meaningful catalogs that share characteristics or serve particular research applications. This schema aims to offer a standardized way to describe catalogs of datasets.


## Features

### 1. Explicit Inclusion Criteria

The schema requires explicit `inclusion_criteria` - a list of rules that datasets must meet to be part of the catalog. This ensures transparent, reproducible catalog membership.

**Example**: A "Multi-Task Studies" catalog might require:
- Participants completed 2 or more distinct cognitive tasks
- Tasks measure different cognitive constructs

### 2. Standards Compatibility with Consistent Naming

The schema provides consistent `snake_case` property naming conventions while maintaining compatibility with existing standards like [schema.org](https://schema.org) and [Dublin Core](https://www.dublincore.org/). Properties such as [`description`](../catalog/description), [`keywords`](../catalog/keywords), and [`curator`](../catalog/curator) map to their schema.org equivalents, while using developer-friendly naming that aligns with common programming conventions.

### 3. Rich Catalog Metadata

Catalogs can be described with standard metadata fields:
- `name`: URL-friendly identifier
- `pretty_name`: Human-readable title
- `description`: Comprehensive purpose and scope
- `keywords`: Focus areas for discovery
- `curator`: People or organizations maintaining the catalog

### 4. Dataset Membership Tracking

Catalogs can list their member datasets via:
- `datasets`: Array of dataset URLs or DOIs
- `dataset_count`: Number of datasets in the catalog

### 5. Catalog Relationships

The `related_catalogs` property enables listing related catalogs to facilitate dataset discovery.






## Use Cases

### Research Applications

- **"Longitudinal Studies"** - Datasets with repeated measurements over time
- **"Multi-Task Assessments"** - Studies with diverse cognitive tasks
- **"Multimodal Data"** - Datasets combining behavioral and neural measures
- **"Developmental Research"** - Studies spanning multiple age groups

### Population-Focused Catalogs

- **"Adolescent Mental Health"** - Datasets from adolescent populations with mental health measures
- **"Aging and Cognition"** - Studies of cognitive aging in older adults
- **"Clinical Populations"** - Datasets from specific clinical groups

### Methodology-Based Catalogs

- **"fMRI Studies"** - Datasets using functional magnetic resonance imaging
- **"Ecological Momentary Assessment"** - Studies using real-time data catalog
- **"Large-Scale Surveys"** - Population-level survey datasets

## Benefits

### For Data Curators

- **Transparent criteria**: Explicit rules for catalog membership
- **Standardized metadata**: Consistent structure across catalogs
- **Relationship tracking**: Document connections between catalogs

### For Researchers

- **Improved discovery**: Find relevant datasets through thematic catalogs
- **Research context**: Understand how datasets relate to each other
- **Quality signals**: Curated catalogs provide research validation

### For the Ecosystem

- **Interoperability**: Machine-readable catalog definitions
- **Semantic web ready**: JSON-LD support for linked data
- **Standards-based**: Built on Schema.org DataCatalog vocabulary

## Relationship to Standards

The Catalog Schema builds on:

- **[Schema.org DataCatalog](https://schema.org/DataCatalog)**: Base vocabulary for catalogs
- **[Dublin Core](https://www.dublincore.org/)**: Metadata properties (`description`, `creator`)
- **[Dataset Schema](https://behaverse.org/schemas/dataset)**: Properties used in inclusion criteria must align with dataset descriptors


## Namespace

- **Base namespace**: `https://behaverse.org/schemas/catalog#`
- **Context file**: `https://behaverse.org/schemas/catalog/context.jsonld`
