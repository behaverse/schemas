---
id: examples
title: Examples
sidebar_label: Examples
---

<!-- THIS FILE IS MANUALLY EDITABLE -->

# Examples

## Multi-Task Cognitive Assessments

A collection of datasets where participants completed multiple distinct cognitive tasks.

```json
{
  "@context": "https://behaverse.org/schemas/collection/context.jsonld",
  "name": "demo-multi-task",
  "pretty_name": "Demo: Multi-Task Cognitive Assessments",
  "description": "Example collection demonstrating how to define multi-task dataset collections. This is a demonstration - the criteria and datasets listed are for illustrative purposes only.",
  "keywords": [
    "demo-multi-task",
    "cognitive assessment",
    "battery",
    "example",
    "demonstration"
  ],
  "inclusion_criteria": [
    "Participants must have completed 2 or more distinct cognitive tasks or assessments",
    "Tasks must measure different cognitive constructs (e.g., memory, attention, executive function, language)",
    "All tasks must be from the same participants (within-subject design)",
    "Both behavioral and neuroimaging multi-task datasets are eligible",
    "Tasks can be completed in single or multiple sessions"
  ],
  "exclusion_criteria": [
    "Single-task studies",
    "Between-subject designs with no within-subject component"
  ],
  "datasets": [
    "https://example.org/datasets/demo-dataset-1",
    "https://example.org/datasets/demo-dataset-2",
    "https://doi.org/10.5555/example.12345"
  ],
  "related_collections": [
    "demo-multimodal",
    "demo-longitudinal"
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

## Longitudinal Studies

A collection of datasets with repeated measurements over time.

```json
{
  "@context": "https://behaverse.org/schemas/collection/context.jsonld",
  "name": "demo-longitudinal",
  "pretty_name": "Demo: Longitudinal & Test-Retest Studies",
  "description": "Example collection demonstrating how to define longitudinal dataset collections. This is a demonstration - the criteria and datasets listed are for illustrative purposes only.",
  "keywords": [
    "demo-longitudinal",
    "test-retest",
    "example",
    "demonstration"
  ],
  "inclusion_criteria": [
    "Participants must have data from 2 or more time points",
    "Same or equivalent measures collected at each time point",
    "Time between measurements can range from minutes (test-retest) to years (longitudinal development)",
    "Must include sufficient sample overlap across time points (>50% retention recommended)",
    "Includes developmental studies, intervention studies, and reliability assessments"
  ],
  "exclusion_criteria": [
    "Cross-sectional studies with no repeated measures",
    "Studies with less than 50% participant retention"
  ],
  "datasets": [
    "https://example.org/datasets/demo-longitudinal-1",
    "https://example.org/datasets/demo-longitudinal-2",
    "https://doi.org/10.5555/example.67890"
  ],
  "related_collections": [
    "demo-multi-task",
    "demo-adolescent-mental-health",
    "demo-adult-mental-health"
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

## Minimal Collection

A minimal collection definition with only required fields.

```json
{
  "@context": "https://behaverse.org/schemas/collection/context.jsonld",
  "name": "minimal-example",
  "pretty_name": "Minimal Collection Example",
  "description": "This minimal example shows the required fields for a valid collection definition.",
  "inclusion_criteria": [
    "Datasets must meet at least one inclusion criterion"
  ]
}
```
