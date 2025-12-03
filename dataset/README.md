# Behaverse Dataset Schema (WIP)

**Version:** v25.1201  
**Namespace:** `https://behaverse.org/schemas/dataset#`

## Overview

The Behaverse Dataset Schema provides a standardized metadata format for describing cognitive science datasets. It enables rich documentation of experimental data including participant demographics, measurement techniques, cognitive tasks, data access information, and ethical considerations.

This schema maps to established standards including Schema.org, DataCite, BIDS (Brain Imaging Data Structure), DDI (Data Documentation Initiative), and HuggingFace dataset cards, ensuring interoperability with existing data infrastructure.

## Key Features

| Feature | Description |
|---------|-------------|
| **Comprehensive Coverage** | 40+ properties covering all aspects of cognitive science datasets |
| **Standard Mappings** | Maps to Schema.org, DataCite, BIDS, DDI, HuggingFace |
| **Flexible Structure** | Supports simple to complex metadata with nested objects |
| **Population Demographics** | Detailed age, sex, and population characteristics |
| **Measurement Techniques** | Structured descriptions of EEG, fMRI, eye tracking, etc. |
| **Activities** | Information about the activities (tasks, questionnaires, games)completed by the agent |
| **Data Access** | Clear licensing, download URLs, and file format information |
| **Ethics** | IRB approval tracking and data quality assessments |

## Field Groups

The schema organizes fields into logical groups:

- **Core Metadata**: Essential identification (name, description, license, version)
- **Dates**: Temporal metadata (created, published, modified, added)
- **People & Organizations**: Creators, curators, affiliations, citations
- **Population & Sample**: Demographics, inclusion/exclusion criteria, coverage
- **Measurement Techniques**: Neuroimaging, physiological, behavioral modalities
- **Activities & Paradigms**: Cognitive tasks, experimental procedures
- **Study Design**: Methodology, conditions, variables
- **Data Files & Distribution**: Formats, access, downloads
- **Ethics**: IRB approval, data quality
- **HuggingFace-Specific**: ML dataset metadata

## Basic Example

```json
{
  "@context": "https://behaverse.org/schemas/dataset/context.jsonld",
  "name": "stroop-task-fmri",
  "pretty_name": "Stroop Task fMRI Dataset",
  "description": "fMRI data from 30 participants performing a classic Stroop color-word interference task",
  "version": "1.0.0",
  "license": "CC-BY-4.0",
  "date_added": "2025-01-15",
  "sample_size": 30,
  "age_range": [18, 35],
  "sex_distribution": {
    "female": 15,
    "male": 15
  },
  "constructs_measured": ["executive_function", "attention"],
  "measurement_technique": [
    {
      "type": "neuroimaging",
      "technique": "fMRI",
      "tr": 2000,
      "te": 30,
      "field_strength": 3.0
    }
  ],
  "activity": [
    {
      "name": "Stroop Task",
      "type": "task",
      "measurements": ["behavior", "fMRI"],
      "trials": 120,
      "duration": 6,
      "conditions": ["congruent", "incongruent"],
      "constructs": ["executive_function", "attention"]
    }
  ]
}
```

## Property Reference

### Core Metadata

| Property | Type | Status | Description | Maps To |
|----------|------|--------|-------------|---------|
| `name` | string | **required** | Short URL-friendly identifier (e.g., "stroop-task-fmri") | schema:name, dc:identifier |
| `pretty_name` | string | recommended | Human-readable display title | HuggingFace pretty_name |
| `description` | string | **required** | Detailed dataset description | schema:description, dc:description |
| `version` | string | recommended | Dataset version number | schema:version |
| `license` | string | **required** | License identifier (e.g., "CC-BY-4.0") | schema:license, datacite:Rights |
| `url` | string (URI) | recommended | Main dataset homepage URL | schema:url |
| `doi` | string | recommended | Digital Object Identifier | datacite:Identifier, schema:identifier |
| `keywords` | array[string] | recommended | Search keywords or tags | schema:keywords |
| `language` | array[string] | optional | Languages used (ISO 639-1 codes) | schema:inLanguage, dc:language |

### Dates

| Property | Type | Status | Description | Maps To |
|----------|------|--------|-------------|---------|
| `date_created` | string (date) | recommended | Original data collection date | schema:dateCreated, datacite:Created |
| `date_published` | string (date) | recommended | Public release date | schema:datePublished, datacite:Issued |
| `date_modified` | string (date) | optional | Last modification date | schema:dateModified, datacite:Updated |
| `date_added` | string (date) | **required** | Date added to catalog | — |
| `last_verified` | string (date) | optional | Last verification/validation date | — |

### People & Organizations

| Property | Type | Status | Description | Maps To |
|----------|------|--------|-------------|---------|
| `creator` | array[object] | recommended | Dataset creators/authors | schema:creator, datacite:Creator |
| `creator[].name` | string | required | Person's full name | schema:name |
| `creator[].email` | string | optional | Contact email | schema:email |
| `creator[].orcid` | string | optional | ORCID identifier | schema:identifier |
| `creator[].affiliation` | string | optional | Institutional affiliation | schema:affiliation |
| `curator` | array[object] | optional | Dataset curators/maintainers | schema:contributor |
| `curator[].name` | string | required | Curator's name | schema:name |
| `curator[].email` | string | optional | Contact email | schema:email |
| `curator[].orcid` | string | optional | ORCID identifier | schema:identifier |
| `curator[].affiliation` | string | optional | Institution | schema:affiliation |
| `citation` | array[object] | recommended | Related publications | schema:citation |
| `citation[].type` | string | optional | Citation type (e.g., "article", "preprint") | — |
| `citation[].doi` | string | optional | Publication DOI | schema:identifier |
| `citation[].url` | string | optional | Publication URL | schema:url |
| `citation[].text` | string | optional | Full citation text | schema:citation |
| `citation[].arxiv_id` | string | optional | arXiv identifier | — |

### Population & Sample

| Property | Type | Status | Description | Maps To |
|----------|------|--------|-------------|---------|
| `sample_size` | integer | **required** | Total number of participants | behaverse:sample_size |
| `age_range` | array[number] | recommended | Age range [min, max] in years | — |
| `age_mean` | number | optional | Mean participant age | — |
| `age_std` | number | optional | Standard deviation of age | — |
| `sex_distribution` | object | recommended | Sex breakdown | — |
| `sex_distribution.female` | integer | optional | Female participants | — |
| `sex_distribution.male` | integer | optional | Male participants | — |
| `sex_distribution.non_binary` | integer | optional | Non-binary participants | — |
| `sex_distribution.other` | integer | optional | Other sex identities | — |
| `sex_distribution.not_reported` | integer | optional | Not reported | — |
| `age_category` | array[string] | optional | Age categories: `children`, `adolescent`, `adult`, `elderly` | schema:audience |
| `population_category` | string | optional | Population type: `healthy`, `clinical`, `patient`, `mixed` | — |
| `inclusion_criteria` | array[string] | optional | Participant inclusion criteria | — |
| `exclusion_criteria` | array[string] | optional | Participant exclusion criteria | — |
| `spatial_coverage` | string | optional | Geographic location/coverage | schema:spatialCoverage |
| `temporal_coverage` | string | optional | Time period covered | schema:temporalCoverage |

### Measurement Techniques

| Property | Type | Status | Description | Maps To |
|----------|------|--------|-------------|---------|
| `measurement_technique` | array[object] | recommended | Measurement modalities used | schema:measurementTechnique |
| `measurement_technique[].type` | string | optional | High-level category: `behavior`, `neuroimaging`, `electrophysiology`, `physiological`, `video`, `audio`, `other` | — |
| `measurement_technique[].technique` | string | **required** | Specific technique: `EEG`, `MEG`, `iEEG`, `fMRI`, `T1w`, `T2w`, `DWI`, `ASL`, `PET`, `NIRS`, `behavior`, `voice`, `eye-tracking`, `key-presses`, `mouse-tracking`, `motion-capture`, `video`, `audio`, `heart-rate`, `GSR`, `EDA`, `ECG`, `EMG`, `other` | — |
| `measurement_technique[].channels` | integer | optional | Number of channels/electrodes (for EEG, MEG) | — |
| `measurement_technique[].sampling_rate` | number | optional | Sampling rate in Hz (for EEG, MEG, physiological) | — |
| `measurement_technique[].reference` | string | optional | Reference type (for EEG, MEG) | — |
| `measurement_technique[].manufacturer` | string | optional | Equipment manufacturer/system | — |
| `measurement_technique[].field_strength` | number | optional | Magnetic field strength in Tesla (for MRI) | — |
| `measurement_technique[].tr` | number | optional | Repetition time in ms (for fMRI) | — |
| `measurement_technique[].te` | number | optional | Echo time in ms (for MRI) | — |
| `measurement_technique[].details` | string | optional | Additional technique-specific details | — |
| `measurement_technique[].response_type` | array[string] | optional | Response types: `button-press`, `key-press`, `mouse`, `voice`, `eye-gaze`, `touchscreen` | — |
| `measurement_technique[].format` | string | optional | File format (e.g., edf, bdf, nii, csv) | — |
| `measurement_technique[].granularity` | string | optional | Data granularity: `event-data`, `timecourse-data`, `trial-data`, `construct-data`, `aggregate-data` | — |
| `constructs_measured` | array[string] | optional | Cognitive or psychological constructs measured | schema:variableMeasured |

### Activities & Paradigms

| Property | Type | Status | Description | Maps To |
|----------|------|--------|-------------|---------|
| `tasks` | array[object] | recommended | Cognitive/behavioral tasks | behaverse:tasks |
| `tasks[].name` | string | required | Task name | schema:name |
| `tasks[].type` | string | optional | Task type (e.g., "cognitive", "motor") | — |
| `tasks[].description` | string | optional | Task description | schema:description |
| `tasks[].stimulus_type` | array[string] | optional | Stimulus types (e.g., "visual", "auditory") | — |
| `tasks[].response_type` | string | optional | Response mode (e.g., "button_press", "verbal") | — |
| `tasks[].trial_count` | integer | optional | Number of trials | — |
| `tasks[].duration` | number | optional | Task duration (seconds) | — |
| `tasks[].url` | string | optional | Task documentation URL | schema:url |
| `paradigm` | array[string] | optional | Experimental paradigms | — |
| `intervention` | array[string] | optional | Interventions applied | — |

### Study Design

| Property | Type | Status | Description | Maps To |
|----------|------|--------|-------------|---------|
| `study_design` | string | optional | Study design type (e.g., "cross-sectional", "longitudinal") | — |
| `experimental_conditions` | array[string] | optional | Experimental conditions/groups | — |
| `variables_measured` | array[string] | optional | Dependent/measured variables | schema:variableMeasured |
| `control_variables` | array[string] | optional | Controlled variables | — |

### Data Files & Distribution

| Property | Type | Status | Description | Maps To |
|----------|------|--------|-------------|---------|
| `file_format` | array[string] | recommended | Data file formats (e.g., "NIfTI", "EDF", "CSV") | schema:encodingFormat, datacite:Format |
| `file_size` | string | optional | Total dataset size (e.g., "2.5 GB") | schema:contentSize |
| `download_url` | string (URI) | optional | Direct download URL | schema:downloadUrl |
| `homepage` | string (URI) | optional | Dataset homepage | schema:url |
| `repository` | string | optional | Repository name (e.g., "OpenNeuro", "Zenodo") | — |
| `bids_compliant` | boolean | optional | BIDS format compliance | — |

### Ethics

| Property | Type | Status | Description | Maps To |
|----------|------|--------|-------------|---------|
| `ethics_approval` | string | optional | IRB/ethics approval status | — |
| `consent_type` | string | optional | Consent type obtained | — |
| `data_quality` | string | optional | Quality assessment summary | — |
| `preprocessing_applied` | array[string] | optional | Preprocessing steps applied | — |

### HuggingFace-Specific

| Property | Type | Status | Description | Maps To |
|----------|------|--------|-------------|---------|
| `task_categories` | array[string] | optional | ML task categories | HuggingFace task_categories |
| `size_categories` | array[string] | optional | Dataset size categories | HuggingFace size_categories |

## Validation

The schema includes JSON Schema validation with constraints:

- **Required fields**: name, description, license, date_added, sample_size
- **Format validation**: Dates (ISO 8601), URIs, email addresses
- **Pattern constraints**: name must be lowercase alphanumeric with hyphens/underscores
- **Type validation**: Strings, integers, numbers, booleans, arrays, objects
- **Enum validation**: Predefined value lists for categorical fields

## Usage in JSON-LD

Link to the context in your JSON-LD documents:

```json
{
  "@context": "https://behaverse.org/schemas/dataset/context.jsonld",
  "name": "my-dataset",
  "description": "Dataset description",
  ...
}
```

Or embed the context:

```json
{
  "@context": {
    "@vocab": "https://behaverse.org/schemas/dataset#",
    "schema": "https://schema.org/",
    ...
  },
  "name": "my-dataset",
  ...
}
```

## Standard Mappings

This schema maps to widely-used standards:

| Standard | Coverage | Purpose |
|----------|----------|---------|
| **Schema.org** | Core metadata, people, dates | Web discoverability, Google Dataset Search |
| **DataCite** | Citations, identifiers, creators | DOI registration, research data citation |
| **BIDS** | Neuroimaging modalities | Brain imaging data organization |
| **DDI** | Variables, study design | Social science data documentation |
| **HuggingFace** | ML metadata | Machine learning dataset cards |
| **Dublin Core** | Basic metadata | Library/archive interoperability |

## Generating Schema Files

The schema files (`schema.json` and `context.jsonld`) are generated from `field-definitions.yaml`:

```bash
cd dataset
python scripts/generate_schema_files.py
```

This ensures consistency between the source YAML, JSON Schema validation, and JSON-LD context.

## Files in this Directory

- **field-definitions.yaml**: Source of truth with all field specifications
- **schema.json**: JSON Schema for validation
- **context.jsonld**: JSON-LD context for semantic web
- **README.md**: This documentation
- **examples/**: Example dataset metadata files
- **scripts/generate_schema_files.py**: Schema generation script

## Related Resources

- [Schema.org Dataset](https://schema.org/Dataset)
- [DataCite Metadata Schema](https://schema.datacite.org/)
- [BIDS Specification](https://bids-specification.readthedocs.io/)
- [DDI Documentation](https://ddialliance.org/)
- [HuggingFace Dataset Cards](https://huggingface.co/docs/hub/datasets-cards)

## AI Usage Disclosure

This schema and documentation were developed with the assistance of AI tools (GitHub Copilot and Claude) to ensure comprehensive coverage of metadata standards and best practices in data documentation.

---

**Version**: v25.1201  
**License**: CC-BY-4.0  
**Maintainer**: Behaverse Project  
**Repository**: https://github.com/behaverse/schemas
