---
id: about
title: About
sidebar_label: About
---

<!-- THIS FILE IS MANUALLY EDITABLE -->

# <img src={require('@site/static/assets/img/schema_B.png').default} height="80" style={{verticalAlign: 'middle'}} /> About bcsvw

bcsvw stands for **Behaverse CSV for the Web**; it is an extension of the [W3C CSV on the Web (CSVW)](https://www.w3.org/TR/tabular-data-primer/) standard designed to enhance CSV metadata for use in R and Python data analysis workflows.



## Motivation

CSV files are ubiquitous in data science, but they often lack the metadata needed to correctly interpret their contents. The [W3C CSV on the Web (CSVW)](https://www.w3.org/TR/tabular-data-primer/) standard provides a foundation for describing tabular data, but it was designed primarily for web publishing and lacks several features essential for modern data analysis workflows. bcsvw aims to bridge this gap.



## Extensions

### 1. Categorical Variables

CSVW defines many data types (`string`, `integer`, `number`, `boolean`, `date`, etc.), but lacks native support for **categorical variables** (factors) — one of the most fundamental data types in statistics and data science.

**bcsvw** adds `categorical` and `ordered` data types that map directly to:
- **R**: `factor()` and `ordered()` functions
- **Python**: `pd.Categorical()` with the `ordered` parameter

| Data Type | Description | Example Use |
|-----------|-------------|-------------|
| `categorical` | Unordered categorical variable (factor) | Gender, color, treatment group |
| `ordered` | Ordered categorical variable | Education level, Likert scale, size (S/M/L) |

### 2. Rich Metadata via Dublin Core

CSVW lacks properties for common metadata fields that are essential for data documentation and discovery.

**bcsvw** incorporates properties from Dublin Core (DC) and other vocabularies, including:
- `description` (from DC): Detailed descriptions for tables and columns
- `creator`: Person or organization that created the dataset
- `date_created`: When the dataset was created
- `pretty_name`: Human-readable titles

These properties make datasets more discoverable and self-documenting.

### 3. Units of Measurement

CSVW lacks a standardized way to specify units of measurement for numeric columns, making it difficult to ensure correct interpretation of scientific data.

**bcsvw** adds `unit` property for SI units and custom units (e.g., `"kg"`, `"°C"`, `"mol/L"`, `"years"`).

### 4. Missing Value Semantics

CSVW's `null` property only allows a single missing value representation. Real-world data often uses multiple codes (`NA`, `N/A`, `missing`, `BDL` for "Below Detection Limit", etc.) with different semantic meanings.

**bcsvw** adds `na_strings` property to specify additional missing value codes beyond the standard `null`, enabling domain-specific missing value handling.

### 5. Data Integrity

Metadata and data files can become desynchronized, leading to incorrect interpretations.

**bcsvw** adds `file_hash` property (SHA-256) to cryptographically ensure metadata corresponds to the correct data file.

### 6. Consistent Naming

CSVW uses camelCase naming (e.g., `minLength`, `maxLength`) which is inconsistent with common data science conventions.

**bcsvw** consistently uses snake_case and provides snake_case aliases (`min_length`, `max_length`) while maintaining backward compatibility with CSVW.



## Benefits

### For Data Producers

- **Self-documenting data**: Metadata travels with the data
- **Type safety**: Explicit data types catch errors early
- **Reproducibility**: Cryptographic hashing ensures data integrity
- **Standards-based**: Built on W3C recommendations

### For Data Consumers

- **Immediate usability**: Load CSV with correct types in one line of code
- **Rich metadata**: Labels, descriptions, and units embedded in the data structure
- **Cross-platform**: Works seamlessly in R, Python, and other tools
- **Validation**: Constraints (min/max, string length) enable automatic data quality checks

### For the Ecosystem

- **CSVW compatible**: Valid bcsvw files are valid CSVW files
- **Semantic web ready**: JSON-LD context enables linked data integration
- **Tool-agnostic**: Any tool that reads CSVW can read bcsvw

## Namespace

- **Base namespace**: `https://behaverse.org/schemas/bcsvw#`
- **Context file**: `https://behaverse.org/schemas/bcsvw/context.jsonld`

## Extension Properties

bcsvw adds the following properties to CSVW:

### Column-Level Properties

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `levels` | array | Factor levels (in order for `ordered` type) | `["low", "medium", "high"]` |
| `na_strings` | array | Additional missing value codes | `["NA", "N/A", "missing"]` |
| `unit` | string | Unit of measurement | `"kg"`, `"°C"`, `"mol/L"` |
| `min_length` | integer | Minimum string length | `2` |
| `max_length` | integer | Maximum string length | `50` |

### Table-Level Properties

| Property | Type | Description |
|----------|------|-------------|
| `file_hash` | string | SHA-256 hash of CSV file for integrity verification |
| `name` | string | Short URL-friendly identifier |
| `pretty_name` | string | Human-readable title for the table |
| `description` | string | Detailed description of the table contents (from Dublin Core) |
| `creator` | string/array | Person or organization that created the table (from Dublin Core) |
| `date_created` | string | Date the table was created (ISO 8601 format) |

## Type Mapping

bcsvw data types map directly to native types in R and Python:

| bcsvw Specification | R Type | Python Type |
|---------------------|--------|-------------|
| `datatype: "string"` | `character` | `str` |
| `datatype: "integer"` | `integer` | `int64` |
| `datatype: "number"` | `numeric` | `float64` |
| `datatype: "boolean"` | `logical` | `bool` |
| `datatype: "date"` | `Date` | `datetime64[ns]` |
| `datatype: "datetime"` | `POSIXct` | `datetime64[ns]` |
| `datatype: "categorical"` + `levels` | `factor()` | `pd.Categorical(ordered=False)` |
| `datatype: "ordered"` + `levels` | `ordered()` | `pd.Categorical(ordered=True)` |



## Relationship to Standards

bcsvw builds on and references:

- **[W3C CSVW](https://www.w3.org/TR/tabular-data-primer/)**: Core table and column definitions
- **[Dublin Core](https://www.dublincore.org/)**: Metadata properties (`description`, `creator`, `date_created`)
- **[RDFS](https://www.w3.org/TR/rdf-schema/)**: `label` property
- **[Schema.org](https://schema.org/)**: General vocabulary alignment
- **[XSD](https://www.w3.org/TR/xmlschema-2/)**: Data type definitions





## Using bcsvw for data processing

**Currently not implemented.** 


The goal is to provide two small packages/libraries to support the following functions in R and Python (same API):

### `read_bcsvw(data_file, metadata_file = NULL)`

Reads a CSV file and applies data types defined in the bcsvw metadata.

**Inputs:**
- `data_file`: Path to CSV file
- `metadata_file`: Path to JSON metadata file (optional, defaults to same name with `.json` extension)

**Output:** Data frame with proper types applied (factors, ordered factors, dates, missing values handled)

### `document_bcsvw(csv_filename, data, column_descriptions, pretty_name, description)`

Documents a data frame by generating bcsvw metadata and inferring types from the R data frame.

**Inputs:**
- `csv_filename`: Name of the CSV file this metadata describes
- `data`: Data frame with properly typed columns (factors, ordered, dates, etc.)
- `column_descriptions`: Named list with metadata for each column (description, unit, constraints)
- `pretty_name`: Human-readable dataset title
- `description`: Dataset description

**Output:** Metadata object (JSON structure) ready for writing

### `write_bcsvw(data, file, metadata_obj, metadata_file = NULL)`

Saves a data frame as CSV and generates its bcsvw metadata file with automatic file hash.

**Inputs:**
- `data`: Data frame to save
- `file`: Path for output CSV file
- `metadata_obj`: Metadata object (from `document_bcsvw()`)
- `metadata_file`: Path for output JSON metadata file (optional, defaults to same name with `.json` extension)

**Output:** Saves both CSV and JSON files, returns paths to saved files

### `validate_bcsvw(data_file, metadata_file = NULL)`

Validates that a CSV file conforms to its bcsvw metadata specification.

**Inputs:**
- `data_file`: Path to CSV file
- `metadata_file`: Path to JSON metadata file (optional, defaults to same name with `.json` extension)

**Output:** Validation result object with pass/fail status and detailed error messages for any violations




### Example in R

```r
# Source the bcsvw functions
library("bcsvw")

# Reading CSV with metadata
df <- read_bcsvw(data_file = "experiment_data.csv",
                 metadata_file = "experiment_data.json")

# The data frame now has proper R types:
# - categorical -> factor()
# - ordered -> ordered()
# - missing values handled according to na_strings

# Creating metadata from a data frame
sample_data <- data.frame(
  subject_id = 1:5,
  name = c("Alice", "Bob", "Carol", "David", "Eve"),
  age = c(25, 30, 35, 28, 32),
  treatment = factor(c("control", "treatment_a", "treatment_b", "control", "treatment_a"),
                     levels = c("control", "treatment_a", "treatment_b")),
  severity = ordered(c("mild", "moderate", "severe", "mild", "critical"),
                     levels = c("mild", "moderate", "severe", "critical")),
  temperature = c(36.5, 37.2, 36.8, NA, 38.1),
  response_time = c(0.45, NA, 0.68, 0.52, NA)
)

# Define column metadata
column_descriptions <- list(
  subject_id = list(description = "Unique subject identifier"),
  name = list(description = "Participant name"),
  age = list(description = "Age in years", unit = "years", minimum = 18, maximum = 100),
  treatment = list(description = "Experimental treatment group (unordered)"),
  severity = list(description = "Symptom severity level (ordered)"),
  temperature = list(description = "Body temperature in Celsius", unit = "°C", 
                     minimum = 35.0, maximum = 42.0),
  response_time = list(description = "Response time in seconds (NA if timeout)", 
                       unit = "s", na_strings = c("NA", "N/A", "timeout"))
)

# Create metadata from data frame (types inferred from R)
metadata <- document_bcsvw(
  csv_filename = "experiment_data.csv",
  data = sample_data,
  column_descriptions = column_descriptions,
  pretty_name = "Experiment Data",
  description = "Experimental data with treatment groups and measurements"
)

# Write both CSV and metadata with automatic file hash
write_bcsvw(
  data = sample_data,
  file = "experiment_data.csv",
  metadata_obj = metadata,
  metadata_file = "experiment_data.json"
)

# Validate the written files
validation_result <- validate_bcsvw(
  data_file = "experiment_data.csv",
  metadata_file = "experiment_data.json"
)
```


The Python version of this code should be very similar.

