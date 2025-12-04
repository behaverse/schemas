---
id: examples
title: Examples
sidebar_label: Examples
---

<!-- THIS FILE IS MANUALLY EDITABLE -->

## Example



### CSV File

**experiment_data.csv:**
```csv
subject_id,name,age,treatment,severity,temperature,response_time
1,Alice,25,control,mild,36.5,1.2
2,Bob,30,treatment_a,moderate,37.2,1.5
3,Charlie,28,treatment_b,severe,37.8,2.1
4,Diana,35,control,moderate,36.8,1.3
5,Eve,32,treatment_a,critical,38.1,NA
```

### Metadata File

**experiment_data.json:**
```json
{
  "@context": "https://behaverse.org/schemas/bcsvw/context.jsonld",
  "name": "experiment-data",
  "pretty_name": "Experiment Data",
  "description": "Experimental data with treatment groups and measurements",
  "date_created": "2025-12-01",
  "creator": "Research Lab",
  "url": "experiment_data.csv",
  "table_schema": {
    "columns": [
      {
        "name": "subject_id",
        "datatype": "integer",
        "description": "Unique subject identifier"
      },
      {
        "name": "name",
        "datatype": "string",
        "min_length": 2,
        "max_length": 50,
        "description": "Participant name"
      },
      {
        "name": "age",
        "datatype": "integer",
        "unit": "years",
        "minimum": 18,
        "maximum": 100,
        "description": "Age in years"
      },
      {
        "name": "treatment",
        "datatype": "categorical",
        "levels": ["control", "treatment_a", "treatment_b"],
        "description": "Experimental treatment group (unordered)"
      },
      {
        "name": "severity",
        "datatype": "ordered",
        "levels": ["mild", "moderate", "severe", "critical"],
        "description": "Symptom severity level (ordered)"
      },
      {
        "name": "temperature",
        "datatype": "number",
        "unit": "°C",
        "minimum": 35.0,
        "maximum": 42.0,
        "null": [""],
        "description": "Body temperature in Celsius"
      },
      {
        "name": "response_time",
        "datatype": "number",
        "unit": "s",
        "null": ["", "NA"],
        "na_strings": ["N/A", "missing", "timeout"],
        "description": "Response time in seconds (NA if timeout)"
      }
    ]
  }
}
```
