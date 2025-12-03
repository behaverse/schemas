---
id: about
title: About
sidebar_label: About
---

<!-- THIS FILE IS MANUALLY EDITABLE -->

# About dataset

The Behaverse `dataset` Schema provides a comprehensive, standardized metadata format for describing cognitive science and neuroscience datasets. It enables rich documentation of experimental data including participant demographics, measurement techniques, cognitive tasks, data access information, and ethical considerations.

## Motivation

High-quality metadata is essential for dataset discovery, evaluation, and reuse in cognitive science research. Researchers need to understand what data was collected, from whom, using what methods, and under what conditions. 

However, metadata practices vary widely across labs and repositories, making it difficult to find relevant datasets or assess their suitability for secondary analyses.

The `dataset` schema aims to facilitate discovery of relevant datasets by providing a structured, comprehensive format that captures all essential aspects of cognitive science datasets while maintaining compatibility with established metadata standards.


## Features

### 1. Comprehensive Coverage

The schema includes 44 properties organized into logical field groups covering:
- Core identification and licensing
- Participant demographics and population characteristics
- Measurement modalities (neuroimaging, behavioral, physiological)
- Cognitive tasks and experimental paradigms
- Study design and methodology
- Data access and file formats
- Ethics

This comprehensive coverage enables detailed dataset documentation without requiring multiple disparate metadata systems.

### 2. Standards Compatibility with Consistent Naming

The schema provides consistent `snake_case` property naming conventions while maintaining compatibility with existing standards including [Schema.org](https://schema.org), [DataCite](https://datacite.org), [BIDS](https://bids.neuroimaging.io), [DDI](https://ddialliance.org), and [HuggingFace](https://huggingface.co/docs/hub/datasets-cards). Properties such as [`description`](../dataset/description), [`license`](../dataset/license), and [`creator`](../dataset/creator) map to their equivalents in these standards, while using developer-friendly naming that aligns with common programming conventions.

### 3. Flexible Nested Structures

The schema supports both simple and complex metadata through nested object structures. Properties like [`measurement_technique`](../dataset/measurement_technique), [`activity`](../dataset/activity), and [`citation`](../dataset/citation) can contain rich structured information while simpler datasets can use minimal required fields.

**Example nested structure:**
```json
{
  "measurement_technique": [
    {
      "type": "neuroimaging",
      "technique": "fMRI",
      "field_strength": 3.0,
      "tr": 2000,
      "manufacturer": "Siemens Prisma"
    }
  ]
}
```

### 4. Population and Sample Documentation

Detailed fields for documenting participant characteristics including:
- Age distribution ([`age_range`](../dataset/age_range), [`age_mean`](../dataset/age_mean), [`age_std`](../dataset/age_std))
- Sex distribution ([`sex_distribution`](../dataset/sex_distribution) with support for non-binary categories)
- Population categories ([`population_category`](../dataset/population_category), [`age_category`](../dataset/age_category))
- Inclusion and exclusion criteria
- Geographic and temporal coverage

### 5. Multi-Modal Measurement Support

Structured documentation of diverse measurement techniques through the [`measurement_technique`](../dataset/measurement_technique) property, with specialized fields for:
- **Neuroimaging**: fMRI, EEG, MEG (field strength, timing parameters, manufacturer)
- **Behavioral**: Response types, timing accuracy, apparatus details
- **Physiological**: ECG, GSR, eye tracking (sampling rates, equipment)

### 6. Activity and Paradigm Description

The [`activity`](../dataset/activity) property enables detailed documentation of:
- Cognitive tasks with trial counts, conditions, and constructs measured
- Questionnaires and assessments
- Training or intervention protocols
- Duration, measurements collected, and experimental conditions

### 7. Citation and Reference Tracking

Multiple citation objects can document:
- Published papers describing the dataset
- Methodological references
- Related datasets
- Software and analysis tools used




## Relationship to Standards

The dataset schema builds on and maps to:

- **[Schema.org Dataset](https://schema.org/Dataset)**: Core vocabulary for dataset descriptions
- **[DataCite](https://datacite.org)**: Citation metadata and DOI registration
- **[BIDS](https://bids.neuroimaging.io)**: Brain imaging data structure for neuroimaging datasets
- **[DDI](https://ddialliance.org)**: Data Documentation Initiative for social science data
- **[HuggingFace](https://huggingface.co/docs/hub/datasets-cards)**: Machine learning dataset cards
- **[Dublin Core](https://www.dublincore.org/)**: Basic metadata elements (`description`, `creator`, `date`)

## Namespace

- **Base namespace**: `https://behaverse.org/schemas/dataset#`
- **Context file**: `https://behaverse.org/schemas/dataset/context.jsonld`
