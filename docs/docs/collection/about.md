---
id: about
title: About
sidebar_label: About
---

<!-- THIS FILE IS MANUALLY EDITABLE -->

# About collection

The Behaverse collection Schema provides a standardized way to describe and organize thematic collections of cognitive science and neuroscience datasets.

## Motivation

Research datasets are often more valuable when organized into meaningful collections that share characteristics or serve particular research applications. This schema aims to offer a standardized way to describe collections of datasets.


## Features

### 1. Explicit Inclusion Criteria

The schema requires explicit `inclusion_criteria` - a list of rules that datasets must meet to be part of the collection. This ensures transparent, reproducible collection membership.

**Example**: A "Multi-Task Studies" collection might require:
- Participants completed 2 or more distinct cognitive tasks
- Tasks measure different cognitive constructs

### 2. Standards Compatibility with Consistent Naming

The schema provides consistent `snake_case` property naming conventions while maintaining compatibility with existing standards like [schema.org](https://schema.org) and [Dublin Core](https://www.dublincore.org/). Properties such as [`description`](../collection/description), [`keywords`](../collection/keywords), and [`curator`](../collection/curator) map to their schema.org equivalents, while using developer-friendly naming that aligns with common programming conventions.

### 3. Rich Collection Metadata

Collections can be described with standard metadata fields:
- `name`: URL-friendly identifier
- `pretty_name`: Human-readable title
- `description`: Comprehensive purpose and scope
- `keywords`: Focus areas for discovery
- `curator`: People or organizations maintaining the collection

### 4. Dataset Membership Tracking

Collections can list their member datasets via:
- `datasets`: Array of dataset URLs or DOIs
- `dataset_count`: Number of datasets in the collection

### 5. Collection Relationships

The `related_collections` property enables listing related collections to facilitate dataset discovery.






## Use Cases

### Research Applications

- **"Longitudinal Studies"** - Datasets with repeated measurements over time
- **"Multi-Task Assessments"** - Studies with diverse cognitive tasks
- **"Multimodal Data"** - Datasets combining behavioral and neural measures
- **"Developmental Research"** - Studies spanning multiple age groups

### Population-Focused Collections

- **"Adolescent Mental Health"** - Datasets from adolescent populations with mental health measures
- **"Aging and Cognition"** - Studies of cognitive aging in older adults
- **"Clinical Populations"** - Datasets from specific clinical groups

### Methodology-Based Collections

- **"fMRI Studies"** - Datasets using functional magnetic resonance imaging
- **"Ecological Momentary Assessment"** - Studies using real-time data collection
- **"Large-Scale Surveys"** - Population-level survey datasets

## Benefits

### For Data Curators

- **Transparent criteria**: Explicit rules for collection membership
- **Standardized metadata**: Consistent structure across collections
- **Relationship tracking**: Document connections between collections

### For Researchers

- **Improved discovery**: Find relevant datasets through thematic collections
- **Research context**: Understand how datasets relate to each other
- **Quality signals**: Curated collections provide research validation

### For the Ecosystem

- **Interoperability**: Machine-readable collection definitions
- **Semantic web ready**: JSON-LD support for linked data
- **Standards-based**: Built on Schema.org Collection vocabulary

## Relationship to Standards

The Collection Schema builds on:

- **[Schema.org Collection](https://schema.org/Collection)**: Base vocabulary for collections
- **[Dublin Core](https://www.dublincore.org/)**: Metadata properties (`description`, `creator`)
- **[Dataset Schema](https://behaverse.org/schemas/dataset)**: Properties used in inclusion criteria must align with dataset descriptors


## Namespace

- **Base namespace**: `https://behaverse.org/schemas/collection#`
- **Context file**: `https://behaverse.org/schemas/collection/context.jsonld`
