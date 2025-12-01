# BCSVW: Behaverse CSV for the Web

**Extension of W3C CSVW for R and Python data types**

## Overview

BCSVW extends the [W3C CSV on the Web (CSVW)](https://www.w3.org/TR/tabular-data-primer/) standard with data types and properties commonly used in R and Python:

- **New data types**: `categorical` and `ordered` for factor variables
- **File integrity**: SHA-256 hash to ensure data and metadata correspondence
- **Missing value codes**: Multiple NA string representations beyond standard null
- **Units of measurement**: SI units and custom units for scientific data
- **Rich metadata**: Human-readable labels and descriptions
- **Consistent naming**: snake_case property names for better readability

BCSVW maintains compatibility with standard CSVW while making CSV files self-documenting and ready for immediate use in data analysis workflows.

## Namespace

- **Base namespace**: `https://behaverse.github.io/schemas/bcsvw#`
- **Context file**: `https://behaverse.github.io/schemas/bcsvw/context.jsonld`

## Key Properties

### BCSVW Extensions

#### New Data Types

CSVW defines the following built-in data types: `string`, `integer`, `number`, `boolean`, `date`, `datetime`, `time`, `duration`, `binary`, `hexBinary`, `anyURI`, `json`, and `xml`. However, it lacks native support for **categorical variables** (factors, ordered and unordered) which are fundamental in data science. BCSVW adds thus adds two new data types to fill this gap:


| Data Type | Description | Example Use |
|-----------|-------------|-------------|
| `categorical` | Unordered categorical variable (factor) | Gender, color, treatment group |
| `ordered` | Ordered categorical variable | Education level, Likert scale, size (S/M/L) |

These types map directly to R's `factor()` and `ordered()` functions, and Python's `pd.Categorical()` with the `ordered` parameter.

#### Additional Properties

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `levels` | array | Factor levels (in order for `ordered` type) | `["low", "medium", "high"]` |
| `na_strings` | array | Additional missing value codes | `["NA", "N/A", "missing"]` |
| `unit` | string | Unit of measurement | `"kg"`, `"°C"`, `"mol/L"` |
| `file_hash` | string | SHA-256 hash of CSV file for integrity verification | `"abc123..."` |

#### Renamed for Consistency (snake_case)

| BCSVW Property | CSVW Property | Description |
|----------------|---------------|-------------|
| `min_length` | `minLength` | Minimum string length |
| `max_length` | `maxLength` | Maximum string length |

### Inherited from CSVW

All standard CSVW properties are supported:
- `name` - Column identifier
- `datatype` - Data type (string, integer, number, date, etc.)
- `format` - Value pattern/constraint
- `null` - Missing value representation
- `minimum`, `maximum` - Numeric constraints

### Inherited from Linked Data Standards

- `label` (from RDFS) - Human-readable label
- `description` (from Dublin Core) - Detailed description

## Quick Start

### Basic Example

This example demonstrates all key BCSVW features: categorical variables, ordered factors, units, missing values, and constraints.

**experiment_data.csv:**
```csv
subject_id,name,age,treatment,severity,temperature,response_time
1,Alice,25,control,mild,36.5,0.45
2,Bob,30,treatment_a,moderate,37.2,
3,Carol,35,treatment_b,severe,36.8,0.68
4,David,28,control,mild,,0.52
5,Eve,32,treatment_a,critical,38.1,NA
```

**experiment_data.json:**
```json
{
  "@context": "https://behaverse.github.io/schemas/bcsvw/context.jsonld",
  "url": "experiment_data.csv",
  "tableSchema": {
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


## Type Mapping

| BCSVW Specification | R Type | Python Type |
|---------------------|--------|-------------|
| `datatype: "string"` | `character` | `str` |
| `datatype: "integer"` | `integer` | `int64` |
| `datatype: "number"` | `numeric` | `float64` |
| `datatype: "boolean"` | `logical` | `bool` |
| `datatype: "date"` | `Date` | `datetime64[ns]` |
| `datatype: "datetime"` | `POSIXct` | `datetime64[ns]` |
| `datatype: "categorical"` + `levels` | `factor()` | `pd.Categorical(ordered=False)` |
| `datatype: "ordered"` + `levels` | `ordered()` | `pd.Categorical(ordered=True)` |


## Using BCSVW for data processing

**Currently not implemented.** 


The goal is to provide two small packages/libraries to support the following functions in R and Python (same API):

### `read_bcsvw(data_file, metadata_file = NULL)`

Reads a CSV file and applies data types defined in the BCSVW metadata.

**Inputs:**
- `data_file`: Path to CSV file
- `metadata_file`: Path to JSON metadata file (optional, defaults to same name with `.json` extension)

**Output:** Data frame with proper types applied (factors, ordered factors, dates, missing values handled)

### `document_bcsvw(csv_filename, data, column_descriptions, title, description)`

Documents a data frame by generating BCSVW metadata and inferring types from the R data frame.

**Inputs:**
- `csv_filename`: Name of the CSV file this metadata describes
- `data`: Data frame with properly typed columns (factors, ordered, dates, etc.)
- `column_descriptions`: Named list with metadata for each column (description, unit, constraints)
- `title`: Dataset title
- `description`: Dataset description

**Output:** Metadata object (JSON structure) ready for writing

### `write_bcsvw(data, file, metadata_obj, metadata_file = NULL)`

Saves a data frame as CSV and generates its BCSVW metadata file with automatic file hash.

**Inputs:**
- `data`: Data frame to save
- `file`: Path for output CSV file
- `metadata_obj`: Metadata object (from `document_bcsvw()`)
- `metadata_file`: Path for output JSON metadata file (optional, defaults to same name with `.json` extension)

**Output:** Saves both CSV and JSON files, returns paths to saved files

### `validate_bcsvw(data_file, metadata_file = NULL)`

Validates that a CSV file conforms to its BCSVW metadata specification.

**Inputs:**
- `data_file`: Path to CSV file
- `metadata_file`: Path to JSON metadata file (optional, defaults to same name with `.json` extension)

**Output:** Validation result object with pass/fail status and detailed error messages for any violations




### Example in R

```r
# Source the BCSVW functions
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
  title = "Experiment Data",
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





## Property Reference

### Data Type: `categorical`

**URI**: `https://behaverse.github.io/schemas/bcsvw#categorical`  
**Description**: Unordered categorical variable (factor). Use with `levels` property to define valid categories.

**Example**:
```json
{
  "name": "treatment",
  "datatype": "categorical",
  "levels": ["control", "treatment_a", "treatment_b"]
}
```

### Data Type: `ordered`

**URI**: `https://behaverse.github.io/schemas/bcsvw#ordered`  
**Description**: Ordered categorical variable. Use with `levels` property to define categories in order.

**Example**:
```json
{
  "name": "education",
  "datatype": "ordered",
  "levels": ["high_school", "bachelors", "masters", "doctorate"]
}
```

### `levels`

**URI**: `https://behaverse.github.io/schemas/bcsvw#levels`  
**Type**: Array of strings  
**Description**: Defines the levels (categories) of a categorical or ordered variable. For `ordered` type, the array defines the order from lowest to highest.

### `na_strings`

**URI**: `https://behaverse.github.io/schemas/bcsvw#na_strings`  
**Type**: Array of strings  
**Description**: Additional strings to treat as missing values beyond CSVW's `null`

**Example**:
```json
{
  "name": "response",
  "datatype": "string",
  "na_strings": ["NA", "N/A", "missing", "not recorded"]
}
```

### `unit`

**URI**: `https://behaverse.github.io/schemas/bcsvw#unit`  
**Type**: String  
**Description**: Unit of measurement for the column (e.g., "kg", "°C", "m/s")

### `file_hash`

**URI**: `https://behaverse.github.io/schemas/bcsvw#file_hash`  
**Type**: String  
**Description**: SHA-256 hash of the CSV file for integrity verification. Ensures that the metadata corresponds to the correct version of the data file.

**Example**:
```json
{
  "url": "experiment_data.csv",
  "file_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```

### `min_length`

**URI**: `https://behaverse.github.io/schemas/bcsvw#min_length` (maps to `csvw:minLength`)  
**Type**: Integer  
**Description**: Minimum string length for the column value

**Example**:
```json
{
  "name": "name",
  "datatype": "string",
  "min_length": 2,
  "max_length": 50
}
```

### `max_length`

**URI**: `https://behaverse.github.io/schemas/bcsvw#max_length` (maps to `csvw:maxLength`)  
**Type**: Integer  
**Description**: Maximum string length for the column value



## Relationship to Standards

BCSVW builds on and references:

- **[W3C CSVW](https://www.w3.org/TR/tabular-data-primer/)**: Core table and column definitions
- **[Dublin Core](https://www.dublincore.org/)**: `description` property
- **[RDFS](https://www.w3.org/TR/rdf-schema/)**: `label` property
- **[Schema.org](https://schema.org/)**: General vocabulary alignment
- **[XSD](https://www.w3.org/TR/xmlschema-2/)**: Data type definitions

## Examples

Complete example datasets are available in the [`examples/`](examples/) directory:

- **`student_data.csv` / `student_data.json`**: Student test results demonstrating ordered factors (letter grades), numeric data with units (age), and file integrity verification with SHA-256 hash
- **`measurements.json` / `measurements.csv`**: Laboratory measurements showing categorical variables (site types), missing value codes (`na_strings` for "BDL"), units for scientific data (°C, mol/L), and datetime formats

These examples demonstrate all key BCSVW features including categorical and ordered datatypes, units, missing value handling, constraints, and metadata structure.

## Versioning

**Current version**: v25.1201  
**Format**: Calendar versioning (vYY.MMDD)

Older versions are available in the [`versions/`](versions/) directory.

## Contributing

Issues and suggestions can be submitted to the [GitHub repository](https://github.com/behaverse/schemas/issues).

## License

This schema is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
