---
id: index
title: dataset
sidebar_label: Overview
slug: /dataset
---

<!-- THIS FILE IS AUTO-GENERATED. DO NOT EDIT MANUALLY. -->

# <img src={require('@site/static/assets/img/schema_D.png').default} height="80" style={{verticalAlign: 'middle'}} /> dataset

**Version**: v25.1201  
**Namespace**: `https://behaverse.org/schemas/dataset`

A metadata schema for cognitive science and neuroscience datasets with mappings to Schema.org, DataCite, BIDS, and other standards

## Properties

This schema defines **44 properties** for describing dataset metadata.

### Core Metadata

Essential fields for dataset identification

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [name](dataset/name) | `string` | required | Short URL-friendly identifier |
| [pretty_name](dataset/pretty_name) | `string` | recommended | Human-readable display title |
| [description](dataset/description) | `string` | required | Comprehensive dataset description |
| [version](dataset/version) | `string` | recommended | Dataset version (semantic versioning) |
| [license](dataset/license) | `string` | required | License identifier in SPDX format |
| [url](dataset/url) | `string` | recommended | Dataset homepage or landing page |
| [doi](dataset/doi) | `string` | recommended | Digital Object Identifier |
| [keywords](dataset/keywords) | `array` | recommended | Keywords for discovery |
| [language](dataset/language) | `array` | optional | ISO 639-1 language codes |


### Dates

Temporal metadata

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [date_created](dataset/date_created) | `string` | recommended | Date dataset was originally created (ISO 8601) |
| [date_published](dataset/date_published) | `string` | recommended | Date first published (ISO 8601) |
| [date_modified](dataset/date_modified) | `string` | optional | Date of last modification (ISO 8601) |
| [date_added](dataset/date_added) | `string` | required | Date added to catalog (ISO 8601, internal) |
| [last_verified](dataset/last_verified) | `string` | optional | Date metadata was last verified (ISO 8601, internal) |


### People & Organizations

Creator and contributor information

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [creator](dataset/creator) | `array` | recommended | Primary dataset creators/authors |
| [curator](dataset/curator) | `array` | optional | Dataset curators responsible for maintenance and quality |

#### Creator Object

Each creator in the `creator` array is an object with the following properties:

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [name](dataset/creator/name) | `string` | required | Creator full name |
| [email](dataset/creator/email) | `string` | optional | Creator email address (format: email) |
| [orcid](dataset/creator/orcid) | `string` | optional | ORCID identifier (format: 0000-0000-0000-0000) |
| [affiliation](dataset/creator/affiliation) | `string` | optional | Institutional affiliation |

**Example:**
```json
{
  "creator": [
  {
    "name": "Jane Researcher",
    "email": "jane@university.edu",
    "orcid": "0000-0001-2345-6789",
    "affiliation": "University Psychology Department"
  }
]
}
```

#### Curator Object

Each curator in the `curator` array is an object with the following properties:

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [name](dataset/curator/name) | `string` | required | Curator full name |
| [email](dataset/curator/email) | `string` | optional | Curator email address (format: email) |
| [orcid](dataset/curator/orcid) | `string` | optional | ORCID identifier (format: 0000-0000-0000-0000) |
| [affiliation](dataset/curator/affiliation) | `string` | optional | Institutional affiliation |


### Citations & References

Published papers and references

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [citation](dataset/citation) | `array` | recommended | Published papers or references |

#### Citation Object

Each citation in the `citation` array is an object with the following properties:

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [type](dataset/citation/type) | `string` | optional | Citation type |
| [doi](dataset/citation/doi) | `string` | optional | DOI of cited paper |
| [url](dataset/citation/url) | `string` | optional | URL of cited resource |
| [text](dataset/citation/text) | `string` | optional | Full citation text |
| [arxiv_id](dataset/citation/arxiv_id) | `string` | optional | ArXiv preprint ID |


### Population & Sample

Aggregate-level population demographics and coverage

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [sample_size](dataset/sample_size) | `integer` | required | Total number of participants |
| [age_range](dataset/age_range) | `array` | recommended | [min, max] age in years |
| [age_mean](dataset/age_mean) | `number` | optional | Mean participant age |
| [age_std](dataset/age_std) | `number` | optional | Standard deviation of age |
| [sex_distribution](dataset/sex_distribution) | `object` | recommended | Participant counts by sex |
| [age_category](dataset/age_category) | `array` | optional | Age group classification |
| [population_category](dataset/population_category) | `string` | optional | Population type (clinical vs healthy) |
| [inclusion_criteria](dataset/inclusion_criteria) | `array` | optional | Participant inclusion criteria |
| [exclusion_criteria](dataset/exclusion_criteria) | `array` | optional | Participant exclusion criteria |
| [spatial_coverage](dataset/spatial_coverage) | `string` | optional | Geographic location/region |
| [temporal_coverage](dataset/temporal_coverage) | `string` | optional | Time period data covers |

#### Sex Distribution Object

Each sex_distribution in the `sex_distribution` array is an object with the following properties:

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [female](dataset/sex_distribution/female) | `integer` | optional | Number of female participants |
| [male](dataset/sex_distribution/male) | `integer` | optional | Number of male participants |
| [other](dataset/sex_distribution/other) | `integer` | optional | Number of participants with other gender identity |
| [not_reported](dataset/sex_distribution/not_reported) | `integer` | optional | Number of participants who did not report gender |

**Example:**
```json
{
  "sex_distribution": {
  "female": 52,
  "male": 45,
  "other": 2,
  "not_reported": 1
}
}
```


### Data Modalities & Measurement

Types of data collected and measurement techniques

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [measurement_technique](dataset/measurement_technique) | `array` | recommended | Measurement techniques used with optional detailed specifications |
| [constructs_measured](dataset/constructs_measured) | `array` | optional | Cognitive or psychological constructs measured in the dataset |

#### Measurement Technique Object

Each measurement_technique in the `measurement_technique` array is an object with the following properties:

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [type](dataset/measurement_technique/type) | `string` | optional | High-level category of measurement |
| [technique](dataset/measurement_technique/technique) | `string` | required | Specific measurement technique |
| [channels](dataset/measurement_technique/channels) | `integer` | optional | Number of channels/electrodes (for EEG, MEG) |
| [sampling_rate](dataset/measurement_technique/sampling_rate) | `number` | optional | Sampling rate in Hz (for EEG, MEG, physiological) |
| [reference](dataset/measurement_technique/reference) | `string` | optional | Reference type (for EEG, MEG) |
| [manufacturer](dataset/measurement_technique/manufacturer) | `string` | optional | Equipment manufacturer/system |
| [field_strength](dataset/measurement_technique/field_strength) | `number` | optional | Magnetic field strength in Tesla (for MRI) |
| [tr](dataset/measurement_technique/tr) | `number` | optional | Repetition time in ms (for fMRI) |
| [te](dataset/measurement_technique/te) | `number` | optional | Echo time in ms (for MRI) |
| [details](dataset/measurement_technique/details) | `string` | optional | Additional technique-specific details |
| [response_type](dataset/measurement_technique/response_type) | `array` | optional | Types of behavior responses (applies when technique is behavior) |
| [format](dataset/measurement_technique/format) | `string` | optional | File format for this specific measurement (e.g., edf, bdf, nii, csv) |
| [granularity](dataset/measurement_technique/granularity) | `string` | optional | Granularity of the measurement (e.g., per trial, per subject, per session) |

**Example:**
```json
{
  "measurement_technique": [
  {
    "type": "electrophysiology",
    "technique": "EEG",
    "channels": 64,
    "sampling_rate": 512,
    "reference": "average",
    "manufacturer": "BioSemi",
    "granularity": "event-data"
  }
]
}
```


### Activities & Paradigms

Cognitive tasks and experimental paradigms

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [activity](dataset/activity) | `array` | recommended | Activities or tasks performed by participants with associated measurements |

#### Activity Object

Each activity in the `activity` array is an object with the following properties:

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [name](dataset/activity/name) | `string` | required | Activity/task name |
| [type](dataset/activity/type) | `string` | optional | Activity type/category |
| [measurements](dataset/activity/measurements) | `array` | optional | List of measurement techniques collected during this activity (reference by technique name) |
| [trials](dataset/activity/trials) | `integer` | optional | Number of trials |
| [duration](dataset/activity/duration) | `number` | optional | Typical duration in minutes |
| [conditions](dataset/activity/conditions) | `array` | optional | Experimental conditions |
| [measures](dataset/activity/measures) | `array` | optional | Primary dependent variables |
| [constructs](dataset/activity/constructs) | `array` | optional | Constructs measured |

**Example:**
```json
{
  "activity": [
  {
    "name": "N-Back",
    "type": "task",
    "measurements": [
      "EEG",
      "eye-tracking",
      "response-device"
    ],
    "trials": 150,
    "duration": 20,
    "conditions": [
      "0-back",
      "2-back"
    ],
    "measures": [
      "d_prime",
      "reaction_time"
    ],
    "constructs": [
      "working memory"
    ]
  }
]
}
```


### Study Design

Study design and methodology

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [study_design_type](dataset/study_design_type) | `string` | recommended | Study design category |
| [intervention_type](dataset/intervention_type) | `array` | optional | Type(s) of intervention (applies when study_design_type is intervention) |
| [session_count](dataset/session_count) | `integer` | optional | Number of experimental sessions per participant |
| [session_description](dataset/session_description) | `string` | optional | Brief description of session structure (if multi-session) |


### Data Files & Distribution

File formats and access information

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [data_formats](dataset/data_formats) | `array` | recommended | File formats (csv, json, edf, etc.) |
| [data_size_gb](dataset/data_size_gb) | `number` | optional | Total dataset size (GB) |
| [data_structure](dataset/data_structure) | `string` | optional | Organization of data files |
| [download_url](dataset/download_url) | `string` | optional | Direct URL to download dataset files (e.g., .zip archive or direct file download... |
| [access_url](dataset/access_url) | `string` | optional | URL to dataset landing page with documentation, access instructions, and metadat... |
| [access_conditions](dataset/access_conditions) | `object` | optional | Access requirements and restrictions for the dataset |

#### Access Conditions Object

Each access_conditions in the `access_conditions` array is an object with the following properties:

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [is_free](dataset/access_conditions/is_free) | `boolean` | optional | Whether the dataset is freely accessible without cost |
| [requirements](dataset/access_conditions/requirements) | `string` | optional | Access restrictions or requirements (e.g., registration, data use agreement) |

**Example:**
```json
{
  "access_conditions": {
  "is_free": true,
  "requirements": "Publicly available"
}
}
```


### Ethics

Ethical approval and data quality

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [ethical_approval](dataset/ethical_approval) | `object` | optional | Ethical approval and IRB information |

#### Ethical Approval Object

Each ethical_approval in the `ethical_approval` array is an object with the following properties:

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [obtained](dataset/ethical_approval/obtained) | `boolean` | optional | Whether ethics approval was obtained |
| [institution](dataset/ethical_approval/institution) | `string` | optional | IRB or ethics board institution |
| [protocol](dataset/ethical_approval/protocol) | `string` | optional | Protocol or approval number |

**Example:**
```json
{
  "ethical_approval": {
  "obtained": true,
  "institution": "University IRB",
  "protocol": "IRB-2024-001"
}
}
```


### HuggingFace-Specific

ML dataset metadata

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [size_category](dataset/size_category) | `string` | optional | HF size bucket |
| [task_categories](dataset/task_categories) | `array` | optional | ML task types |



## Usage

See the [examples](dataset/examples) for practical usage patterns.

## Version History

The current version of `dataset` is `v25.1201`.

Older versions are available in the [`dataset/versions/`](https://github.com/behaverse/schemas/tree/main/dataset/versions) directory.
