# bcsv: Behaverse CSV (WIP)

**Extension of W3C CSVW for R and Python data types**

## Overview

W3C [CSV on the Web (CSVW)](https://www.w3.org/TR/tabular-data-primer/) is excellent at scalar validation (typed XSD primitives, value-range and pattern constraints, foreign keys across CSVs) but predates the era when R and pandas became the dominant tabular tooling. bcsv extends CSVW with the vocabulary that R/Python data-science workflows actually need — without breaking CSVW compatibility for the properties CSVW already covers.

### Gaps that bcsv addresses

| Need                            | CSVW today                       | bcsv                                              |
|---------------------------------|----------------------------------|----------------------------------------------------|
| Unordered categorical           | regex format only                | `datatype: "categorical"` + `levels`               |
| Ordered categorical             | none                             | `datatype: "ordered"` + `levels` (in order)        |
| Multiple NA codes               | one `null` list                  | `null` + `na_strings`                              |
| Units                           | `propertyUrl` + QUDT IRIs        | `unit: "°C"`                                       |
| Human-readable label            | multilingual `titles` array      | `label` → rdfs:label                               |
| Description                     | `dc:description` (prefix needed) | `description` (no prefix; mapped to dc:description) |
| Data/metadata integrity         | none                             | `file_hash` (SHA-256)                              |
| Compatibility with CSVW tools   | —                                | compatible with permissive CSVW readers; strict CSVW validators will flag `categorical` and `ordered` as unknown datatypes |

### Non-goals

- bcsv is not a CSVW replacement. Every bcsv document remains a CSVW document with extra properties; permissive CSVW tools ignore the bcsv additions.
- bcsv does not introduce new scalar types beyond `categorical` and `ordered`.
- bcsv does not extend CSVW's multi-table relational model.
- bcsv does not attempt to formalise units (no unit algebra, no dimensional analysis). The `unit` field is a free-form string.

## Namespace

- **Base namespace**: `https://behaverse.org/schemas/bcsv#`
- **Context file**: `https://behaverse.org/schemas/bcsv/context.jsonld`

## Key Properties

### bcsv Extensions

#### New Data Types

bcsv supports the CSVW built-in scalar types: `string`, `integer`, `number`, `boolean`, `date`, `datetime`, and `time`. Other CSVW built-ins (`duration`, `binary`, `hexBinary`, `anyURI`, `json`, `xml`, `decimal`) are deferred and treated as `string` for v0 — they may gain explicit mappings in a future minor version. On top of the supported scalars, bcsv adds two types that CSVW lacks: **categorical variables** (factors, ordered and unordered), which are fundamental in data science.


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

| bcsv Property | CSVW Property | Description |
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

This example demonstrates all key bcsv features: categorical variables, ordered factors, units, missing values, and constraints.

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
  "@context": "https://behaverse.org/schemas/bcsv/context.jsonld",
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


## Type Mapping

| bcsv Specification | R Type | Python Type |
|---------------------|--------|-------------|
| `datatype: "string"` | `character` | `string` (StringDtype) |
| `datatype: "integer"` | `integer` | `Int64` (nullable) |
| `datatype: "number"` | `numeric` | `Float64` (nullable) |
| `datatype: "boolean"` | `logical` | `boolean` (nullable) |
| `datatype: "date"` | `Date` | `datetime64[ns]` |
| `datatype: "datetime"` | `POSIXct` | `datetime64[ns]` |
| `datatype: "categorical"` + `levels` | `factor()` | `pd.Categorical(ordered=False)` |
| `datatype: "ordered"` + `levels` | `ordered()` | `pd.Categorical(ordered=True)` |

Python types are pandas extension dtypes throughout (pandas ≥ 1.0). Missingness is represented as `pd.NA` (Python) or `NA` (R) for all columns.


## Using bcsv for data processing

Consumer R and Python packages that read, write, document, and validate
bcsv-paired CSVs are in development. This section will be expanded with
worked examples when those packages ship.





## Property Reference

This section documents all properties supported by bcsv, including bcsv extensions, inherited CSVW properties, and linked data properties.

### Table-Level Properties

#### `@context`

**URI**: Standard JSON-LD property  
**Type**: String (URL)  
**Description**: URL to the bcsv JSON-LD context file  
**Required**: Recommended  
**Example**: `"https://behaverse.org/schemas/bcsv/context.jsonld"`

#### `url`

**URI**: `http://www.w3.org/ns/csvw#url`  
**Type**: String  
**Description**: Path or URL to the CSV data file  
**Required**: Yes  
**Example**: `"experiment_data.csv"`

#### `name`

**URI**: `http://schema.org/name`  
**Type**: String  
**Description**: Short URL-friendly identifier (lowercase letters, numbers, hyphens, underscores)  
**Required**: No  
**Pattern**: `^[a-z0-9-_]+$`  
**Example**: `"experiment-results"`

> **Note**: `name` is used at two levels with different semantics — the table-level `name` (here) is a URL-friendly slug mapped to `schema:name`; the column-level `name` (below) must match the CSV header exactly and is mapped to `csvw:name`.

#### `pretty_name`

**URI**: `http://purl.org/dc/terms/title`  
**Type**: String  
**Description**: Human-readable title for the table  
**Required**: No  
**Example**: `"Experiment Results Dataset"`

#### `description`

**URI**: `http://purl.org/dc/terms/description`  
**Type**: String  
**Description**: Detailed description of the table contents  
**Required**: No  
**Example**: `"Experimental data with treatment groups and measurements"`

#### `file_hash`

**URI**: `https://behaverse.org/schemas/bcsv#file_hash`  
**Type**: String (SHA-256 hash)  
**Description**: SHA-256 hash of the CSV file for integrity verification. Ensures that the metadata corresponds to the correct version of the data file.  
**Required**: No  
**Example**: `"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"`

#### `date_created`

**URI**: `http://schema.org/dateCreated`  
**Type**: String (date in ISO 8601 format)  
**Description**: Date the table was created  
**Required**: No  
**Example**: `"2025-12-01"`

#### `creator`

**URI**: `http://schema.org/creator`  
**Type**: String, Object, or Array of Objects  
**Description**: Person or organization that created the table. Accepts a simple string, a single structured creator object, or an array of creator objects (each with `name`, optional `email`, `orcid`, `affiliation`).  
**Required**: No  
**Examples**:  
- Simple: `"Research Lab Name"`  
- Single object: `{"name": "Jane Researcher", "orcid": "0000-0001-2345-6789"}`  
- Array of objects: `[{"name": "Jane Researcher", "email": "jane@university.edu", "orcid": "0000-0001-2345-6789", "affiliation": "University Psychology Department"}]`

#### `license`

**URI**: `http://schema.org/license`  
**Type**: String (SPDX identifier)  
**Description**: License under which the data is published, given as an SPDX identifier.  
**Required**: No  
**Example**: `"CC-BY-4.0"`, `"MIT"`, `"Apache-2.0"`

#### `table_schema`

**URI**: `http://www.w3.org/ns/csvw#tableSchema`  
**Type**: Object  
**Description**: Container for column definitions  
**Required**: Yes  
**Contains**: `columns` array (required), `primary_key` (optional)

### Column-Level Properties

#### `name`

**URI**: `http://www.w3.org/ns/csvw#name`  
**Type**: String  
**Description**: Column name (must match CSV header exactly)  
**Required**: Yes  
**Example**: `"subject_id"`

#### `label`

**URI**: `http://www.w3.org/2000/01/rdf-schema#label`  
**Type**: String  
**Description**: Human-readable label for the column  
**Required**: No  
**Example**: `"Subject ID"`

#### `description`

**URI**: `http://purl.org/dc/terms/description`  
**Type**: String  
**Description**: Detailed description of the column  
**Required**: No  
**Example**: `"Unique identifier for each participant"`

#### `datatype`

**URI**: `http://www.w3.org/ns/csvw#datatype`  
**Type**: String  
**Description**: Data type of the column values  
**Required**: No (defaults to `string`)  
**Valid values**:

**Standard CSVW types:**
- `string` - Text data
- `integer` - Whole numbers
- `number` - Decimal numbers
- `boolean` - True/false values
- `date` - Date (YYYY-MM-DD)
- `datetime` - Date and time (ISO 8601)
- `time` - Time of day

**bcsv extensions:**
- `categorical` - Unordered categorical variable (factor)
- `ordered` - Ordered categorical variable (ordered factor)

**Example**:
```json
{
  "name": "treatment",
  "datatype": "categorical",
  "levels": ["control", "treatment_a", "treatment_b"]
}
```

#### `levels`

**URI**: `https://behaverse.org/schemas/bcsv#levels`  
**Type**: Array of strings, integers, or numbers  
**Description**: Defines the valid categories for `categorical` or `ordered` datatypes. For `ordered` type, the array defines the order from lowest to highest. Numeric levels are supported for Likert-scale and other numerically-encoded ordinal data.  
**Required**: Required when `datatype` is `categorical` or `ordered`; forbidden for other datatypes.  
**Examples**:  
- String levels: `["low", "medium", "high"]`  
- Likert-scale (integer levels): `[1, 2, 3, 4, 5]`

#### `format`

**URI**: `http://www.w3.org/ns/csvw#format`  
**Type**: String  
**Description**: Pattern or format for the values (e.g., date format, regex pattern). Forbidden when `datatype` is `categorical` or `ordered` — use `levels` to enumerate valid values.  
**Required**: No  
**Example**: `"yyyy-MM-dd"` for dates, `"[A-Z]{3}"` for regex

#### `null`

**URI**: `http://www.w3.org/ns/csvw#null`  
**Type**: String or Array of strings  
**Description**: String(s) that represent null/missing values in the CSV file  
**Required**: No (defaults to empty string)  
**Example**: `["", "NA", "null"]`

#### `na_strings`

**URI**: `https://behaverse.org/schemas/bcsv#na_strings`  
**Type**: Array of strings  
**Description**: Additional missing value codes beyond standard `null`. Useful for domain-specific missing value indicators like "BDL" (Below Detection Limit)  
**Required**: No  
**Example**: `["NA", "N/A", "missing", "not recorded", "BDL"]`

#### `unit`

**URI**: `https://behaverse.org/schemas/bcsv#unit`  
**Type**: String  
**Description**: Unit of measurement for numeric columns (e.g., SI units, custom units)  
**Required**: No  
**Example**: `"kg"`, `"°C"`, `"mol/L"`, `"ms"`

#### `minimum`

**URI**: `http://www.w3.org/ns/csvw#minInclusive`  
**Type**: Number  
**Description**: Minimum allowed value (inclusive) for numeric columns  
**Required**: No  
**Example**: `0`

#### `maximum`

**URI**: `http://www.w3.org/ns/csvw#maxInclusive`  
**Type**: Number  
**Description**: Maximum allowed value (inclusive) for numeric columns  
**Required**: No  
**Example**: `100`

#### `min_length`

**URI**: `https://behaverse.org/schemas/bcsv#min_length` (maps to `csvw:minLength`)  
**Type**: Integer (non-negative)  
**Description**: Minimum string length for the column value  
**Required**: No  
**Example**: `2`

#### `max_length`

**URI**: `https://behaverse.org/schemas/bcsv#max_length` (maps to `csvw:maxLength`)  
**Type**: Integer (non-negative)  
**Description**: Maximum string length for the column value  
**Required**: No  
**Example**: `50`

#### `required`

**URI**: `http://www.w3.org/ns/csvw#required`  
**Type**: Boolean  
**Description**: Whether the column must have a non-null value in every row  
**Required**: No (defaults to `false`)  
**Example**: `true`

#### `virtual`

**URI**: `http://www.w3.org/ns/csvw#virtual`  
**Type**: Boolean  
**Description**: Whether the column is virtual (exists in metadata but not in CSV file)  
**Required**: No (defaults to `false`)  
**Example**: `false`

### Complete Column Example

```json
{
  "name": "temperature",
  "label": "Body Temperature",
  "description": "Patient body temperature at time of measurement",
  "datatype": "number",
  "unit": "°C",
  "minimum": 35.0,
  "maximum": 42.0,
  "null": ["", "NA"],
  "na_strings": ["not measured", "equipment failure"],
  "required": false
}
```



## CSVW Pass-Through Properties

All standard CSVW properties pass through unchanged. The bcsv JSON-LD context declares the following CSVW terms so they expand to the correct W3C CSVW IRIs; consult the [W3C CSVW spec](https://www.w3.org/TR/tabular-data-primer/) for their semantics.

- `propertyUrl`, `valueUrl`, `aboutUrl` — URI templates for RDF mapping.
- `foreignKeys` — referential-integrity declarations.
- `default`, `separator`, `suppressOutput`, `rowTitles` — column-cell handling.
- `length`, `base` — additional value constraints.

These properties are not validated by `bcsv/schema.json`. If you need to use them, refer to the CSVW spec.

**Naming convention.** Where bcsv actively validates a CSVW property (e.g., `primary_key`, which bcsv checks for composite uniqueness), it is renamed to snake_case. Properties bcsv passes through without validation (e.g., `foreignKeys`) keep their CSVW casing. The renamed `primary_key` is documented above under `table_schema`; the underlying IRI is still the W3C CSVW IRI for primary key.

## Relationship to Standards

bcsv builds on and references:

- **[W3C CSVW](https://www.w3.org/TR/tabular-data-primer/)**: Core table and column definitions
- **[Dublin Core](https://www.dublincore.org/)**: `description` and `title` properties
- **[RDFS](https://www.w3.org/TR/rdf-schema/)**: `label` property
- **[Schema.org](https://schema.org/)**: General vocabulary alignment
- **[XSD](https://www.w3.org/TR/xmlschema-2/)**: Data type definitions

## Examples

Complete example datasets are available in the [`examples/`](examples/) directory:

- **`student_data.csv` / `student_data.json`**: Student test results demonstrating ordered factors (letter grades), numeric data with units (age), and file integrity verification with SHA-256 hash
- **`measurements.json` / `measurements.csv`**: Laboratory measurements showing categorical variables (site types), missing value codes (`na_strings` for "BDL"), units for scientific data (°C, mol/L), and datetime formats

These examples demonstrate all key bcsv features including categorical and ordered datatypes, units, missing value handling, constraints, and metadata structure.

## Versioning

**Current version**: v26.0513  
**Format**: Calendar versioning (vYY.MMDD)

Older versions are available in the [`versions/`](versions/) directory.

## Contributing

Issues and suggestions can be submitted to the [GitHub repository](https://github.com/behaverse/schemas/issues).

## License

This schema is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).


## AI Usage Disclosure 

This document was created with assistance from AI tools.