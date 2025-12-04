---
id: examples
title: Examples
sidebar_label: Examples
---

<!-- THIS FILE IS MANUALLY EDITABLE -->

# Examples

This page provides practical examples of using the Behaverse Dataset Schema to document cognitive science datasets.

## Minimal Example

A minimal dataset description with only required fields:

```json
{
  "@context": "https://behaverse.org/schemas/dataset/context.jsonld",
  "name": "simple-stroop",
  "description": "Basic Stroop task dataset with 20 participants",
  "license": "CC-BY-4.0"
}
```

## Basic fMRI Dataset

A typical neuroimaging dataset with essential metadata:

```json
{
  "@context": "https://behaverse.org/schemas/dataset/context.jsonld",
  "name": "stroop-task-fmri",
  "pretty_name": "Stroop Task fMRI Dataset",
  "description": "fMRI data from 30 participants performing a classic Stroop color-word interference task. Participants viewed color words displayed in either matching or mismatching ink colors and indicated the ink color via button press.",
  "version": "1.0.0",
  "license": "CC-BY-4.0",
  "doi": "10.5555/example.stroop",
  "url": "https://example.org/datasets/stroop-fmri",
  "keywords": ["fMRI", "Stroop", "executive function", "attention", "cognitive control"],
  
  "date_published": "2024-03-15",
  "date_added": "2025-01-15",
  
  "sample_size": 30,
  "age_range": [18, 35],
  "age_mean": 24.5,
  "sex_distribution": {
    "female": 15,
    "male": 15
  },
  
  "constructs_measured": ["executive_function", "attention", "response_inhibition"],
  
  "measurement_technique": [
    {
      "type": "neuroimaging",
      "technique": "fMRI",
      "field_strength": 3.0,
      "tr": 2000,
      "te": 30
    }
  ],
  
  "activity": [
    {
      "name": "Stroop Task",
      "type": "task",
      "trials": 120,
      "duration": 6,
      "conditions": ["congruent", "incongruent", "neutral"]
    }
  ],
  
  "data_formats": ["NIfTI", "TSV", "JSON"],
  "download_url": "https://example.org/downloads/stroop-fmri.zip"
}
```

## Comprehensive Multimodal Dataset

A detailed example showing rich metadata for a complex multimodal study:

```json
{
  "@context": "https://behaverse.org/schemas/dataset/context.jsonld",
  "name": "multimodal-cognitive-battery",
  "pretty_name": "Multimodal Cognitive Battery Dataset",
  "description": "A comprehensive dataset combining EEG, eye tracking, and behavioral measures from 120 participants completing a battery of six cognitive tasks assessing attention, memory, and executive function. Data was collected in three sessions over two weeks.",
  "version": "2.1.0",
  "license": "CC-BY-4.0",
  "doi": "10.5555/example.multimodal",
  "url": "https://example.org/datasets/multimodal-battery",
  "keywords": [
    "EEG",
    "eye tracking",
    "cognitive battery",
    "attention",
    "working memory",
    "executive function",
    "multimodal"
  ],
  "language": ["en"],
  
  "date_created": "2023-01-10",
  "date_published": "2024-06-01",
  "date_modified": "2024-11-15",
  "date_added": "2025-01-20",
  
  "creator": [
    {
      "name": "Dr. Jane Smith",
      "email": "jane.smith@university.edu",
      "orcid": "0000-0001-2345-6789",
      "affiliation": "Department of Psychology, Example University"
    },
    {
      "name": "Dr. John Doe",
      "email": "john.doe@university.edu",
      "orcid": "0000-0002-3456-7890",
      "affiliation": "Department of Neuroscience, Example University"
    }
  ],
  
  "curator": [
    {
      "name": "Dr. Jane Smith",
      "email": "jane.smith@university.edu",
      "orcid": "0000-0001-2345-6789",
      "affiliation": "Department of Psychology, Example University"
    }
  ],
  
  "citation": [
    {
      "type": "article",
      "doi": "10.5555/example.paper1",
      "text": "Smith, J., & Doe, J. (2024). A multimodal investigation of cognitive control. Journal of Cognitive Neuroscience, 36(5), 789-812.",
      "url": "https://doi.org/10.5555/example.paper1"
    },
    {
      "type": "preprint",
      "doi": "10.5555/example.preprint",
      "text": "Smith, J., et al. (2024). Dataset descriptor: Multimodal Cognitive Battery. bioRxiv.",
      "url": "https://doi.org/10.5555/example.preprint"
    }
  ],
  
  "sample_size": 120,
  "age_range": [18, 65],
  "age_mean": 32.4,
  "age_std": 12.8,
  "sex_distribution": {
    "female": 65,
    "male": 52,
    "non_binary": 3
  },
  "age_category": ["adult", "young-adult", "middle-aged", "older-adult"],
  "population_category": ["healthy", "neurotypical"],
  
  "inclusion_criteria": [
    "Age 18-65 years",
    "Native English speaker or fluent (self-reported)",
    "Normal or corrected-to-normal vision",
    "No current psychiatric medication",
    "Able to complete 3 sessions over 2 weeks"
  ],
  
  "exclusion_criteria": [
    "History of neurological disorder",
    "Current diagnosis of psychiatric disorder",
    "Substance abuse in past 6 months",
    "Uncorrected vision impairment"
  ],
  
  "spatial_coverage": "Seattle, Washington, United States",
  "temporal_coverage": "2023-03 to 2023-12",
  
  "constructs_measured": [
    "attention",
    "working_memory",
    "executive_function",
    "processing_speed",
    "inhibitory_control",
    "cognitive_flexibility"
  ],
  
  "measurement_technique": [
    {
      "type": "neurophysiology",
      "technique": "EEG",
      "channels": 64,
      "sampling_rate": 1000,
      "manufacturer": "BioSemi ActiveTwo",
      "details": "International 10-20 system, impedances <5kΩ"
    },
    {
      "type": "eye_tracking",
      "technique": "eye_tracking",
      "sampling_rate": 1000,
      "manufacturer": "EyeLink 1000 Plus",
      "details": "Binocular recording, desktop mount, 9-point calibration"
    },
    {
      "type": "behavior",
      "technique": "behavior",
      "response_type": ["button-press", "verbal"],
      "details": "Response pad for manual tasks, microphone for verbal tasks"
    }
  ],
  
  "activity": [
    {
      "name": "Flanker Task",
      "type": "task",
      "measurements": ["EEG", "eye_tracking", "behavior"],
      "trials": 200,
      "duration": 8,
      "conditions": ["congruent", "incongruent"],
      "measures": ["ERP", "reaction_time", "accuracy", "fixations"],
      "constructs": ["attention", "inhibitory_control"]
    },
    {
      "name": "N-Back Task",
      "type": "task",
      "measurements": ["EEG", "behavior"],
      "trials": 150,
      "duration": 10,
      "conditions": ["1-back", "2-back", "3-back"],
      "measures": ["ERP", "reaction_time", "accuracy", "d-prime"],
      "constructs": ["working_memory", "executive_function"]
    },
    {
      "name": "Visual Search",
      "type": "task",
      "measurements": ["EEG", "eye_tracking", "behavior"],
      "trials": 120,
      "duration": 12,
      "conditions": ["set_size_4", "set_size_8", "set_size_12"],
      "measures": ["ERP", "search_time", "accuracy", "scanpath", "fixations"],
      "constructs": ["attention", "processing_speed"]
    },
    {
      "name": "Stroop Task",
      "type": "task",
      "measurements": ["EEG", "behavior"],
      "trials": 180,
      "duration": 7,
      "conditions": ["congruent", "incongruent", "neutral"],
      "measures": ["ERP", "reaction_time", "accuracy"],
      "constructs": ["executive_function", "inhibitory_control"]
    },
    {
      "name": "Trail Making Test",
      "type": "task",
      "measurements": ["eye_tracking", "behavior"],
      "duration": 5,
      "conditions": ["part_A", "part_B"],
      "measures": ["completion_time", "errors", "scanpath"],
      "constructs": ["cognitive_flexibility", "processing_speed"]
    },
    {
      "name": "Digit Span",
      "type": "task",
      "measurements": ["behavior"],
      "duration": 10,
      "conditions": ["forward", "backward"],
      "measures": ["span_length", "accuracy"],
      "constructs": ["working_memory"]
    }
  ],
  
  "study_design_type": "cross-sectional",
  "session_count": 3,
  "session_description": "Session 1: Demographics, consent, Flanker, N-Back. Session 2: Visual Search, Stroop, Trail Making. Session 3: Digit Span, questionnaires, debriefing.",
  
  "data_formats": ["EDF", "BDF", "CSV", "TSV", "JSON"],
  "data_size_gb": 45.7,
  "data_structure": "BIDS-compatible organization with raw EEG, preprocessed eye tracking, behavioral data in TSV, and metadata in JSON",
  "download_url": "https://example.org/downloads/multimodal-battery.tar.gz",
  
  "ethical_approval": {
    "obtained": true,
    "institution": "Example University IRB",
    "protocol": "IRB-2022-12345"
  },
  
  "access_conditions": {
    "is_free": true,
    "requirements": "Data use agreement required, no commercial use"
  },
  
  "task_categories": ["attention", "working-memory", "cognitive-control"],
  "size_category": "10K<n<100K"
}
```

## Longitudinal Study

An example showing how to document a longitudinal dataset:

```json
{
  "@context": "https://behaverse.org/schemas/dataset/context.jsonld",
  "name": "cognitive-aging-longitudinal",
  "pretty_name": "Cognitive Aging Longitudinal Study",
  "description": "A 5-year longitudinal study tracking cognitive function in older adults, with annual assessments of memory, attention, and executive function. Includes 200 participants aged 60-80 at baseline.",
  "version": "1.0.0",
  "license": "CC-BY-NC-4.0",
  "doi": "10.5555/example.aging",
  
  "sample_size": 200,
  "age_range": [60, 80],
  "age_mean": 68.5,
  "age_category": ["older-adult"],
  "population_category": ["healthy"],
  
  "temporal_coverage": "2018-01 to 2023-12",
  
  "constructs_measured": [
    "episodic_memory",
    "working_memory",
    "processing_speed",
    "executive_function"
  ],
  
  "study_design_type": "longitudinal",
  "session_count": 5,
  "session_description": "Annual assessments over 5 years, each including cognitive battery, health questionnaires, and lifestyle measures",
  
  "activity": [
    {
      "name": "Cognitive Battery",
      "type": "task",
      "measurements": ["behavior"],
      "duration": 90,
      "measures": ["accuracy", "reaction_time", "standard_scores"],
      "constructs": ["episodic_memory", "working_memory", "processing_speed", "executive_function"]
    }
  ],
  
  "data_formats": ["CSV", "JSON"],
  "download_url": "https://example.org/downloads/aging-study.zip"
}
```

## Clinical Population Dataset

An example documenting a clinical population study:

```json
{
  "@context": "https://behaverse.org/schemas/dataset/context.jsonld",
  "name": "adhd-cognitive-profile",
  "pretty_name": "ADHD Cognitive Profile Dataset",
  "description": "Cognitive assessment data from 80 adults diagnosed with ADHD and 80 matched controls, including attention tasks, executive function measures, and questionnaires.",
  "version": "1.0.0",
  "license": "CC-BY-NC-SA-4.0",
  "doi": "10.5555/example.adhd",
  
  "sample_size": 160,
  "age_range": [18, 50],
  "sex_distribution": {
    "female": 80,
    "male": 78,
    "prefer_not_to_say": 2
  },
  "age_category": ["adult"],
  "population_category": ["clinical", "ADHD", "healthy_control"],
  
  "inclusion_criteria": [
    "ADHD group: DSM-5 diagnosis of ADHD confirmed by clinical interview",
    "Control group: No history of ADHD or other psychiatric disorders",
    "Age 18-50 years",
    "IQ > 85"
  ],
  
  "exclusion_criteria": [
    "Comorbid major psychiatric disorder (except anxiety/depression for ADHD group)",
    "Neurological disorder",
    "Substance dependence"
  ],
  
  "constructs_measured": [
    "sustained_attention",
    "selective_attention",
    "inhibitory_control",
    "working_memory",
    "cognitive_flexibility"
  ],
  
  "activity": [
    {
      "name": "Continuous Performance Test",
      "type": "task",
      "measurements": ["behavior"],
      "trials": 300,
      "duration": 15,
      "measures": ["hit_rate", "false_alarms", "reaction_time", "reaction_time_variability"],
      "constructs": ["sustained_attention", "inhibitory_control"]
    },
    {
      "name": "ADHD Rating Scale",
      "type": "questionnaire",
      "measurements": ["self_report"],
      "duration": 10,
      "measures": ["total_score", "inattention_subscale", "hyperactivity_subscale"],
      "constructs": ["ADHD_symptoms"]
    }
  ],
  
  "ethical_approval": {
    "obtained": true,
    "institution": "Clinical Research IRB",
    "protocol": "IRB-CLIN-2023-456"
  },
  
  "data_formats": ["CSV", "JSON"],
  "size_category": "100<n<1K"
}
```
