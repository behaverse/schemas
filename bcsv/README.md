# bcsv: Behaverse CSV (WIP)

**Extension of W3C CSVW for R and Python data types**

## Overview

W3C [CSV on the Web (CSVW)](https://www.w3.org/TR/tabular-data-primer/) extends CSV with scalar validation (typed XSD primitives, value-range and pattern constraints, foreign keys across CSVs).

bcsv extends CSVW with the vocabulary that R/Python data-science workflows need without breaking CSVW compatibility for the properties CSVW already covers.

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

bcsv supports the CSVW built-in scalar types: `string`, `integer`, `number`, `boolean`, `date`, `datetime`, and `time`. Other CSVW built-ins (`duration`, `binary`, `hexBinary`, `anyURI`, `json`, `xml`, `decimal`) are deferred and treated as `string` for now—they may gain explicit mappings in a future version. On top of the supported scalars, bcsv adds two types that CSVW lacks: **categorical variables** (factors, ordered and unordered), which are fundamental in data science.


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





## Properties

This is a summary of every bcsv property. **Authoritative per-property detail — types, URIs, vocabulary mappings, constraints, and examples — is generated from [`schema.json`](schema.json) and published as one page per property on the [documentation site](https://behaverse.org/schemas/bcsv).**

### Table properties

| Property | Type | Required | Description |
|---|---|---|---|
| `@context` | string | yes | JSON-LD context URL |
| `name` | string | no | Short URL-friendly identifier |
| `url` | string | yes | URL or path to the CSV file |
| `dialect` | object | no | CSV serialization hints. v0 honors `delimiter` and `encoding`; other CSVW dialect sub-properties pass through but are not interpreted by bcsv tooling. |
| `pretty_name` | string | no | Human-readable title for the table |
| `description` | string | no | Detailed description of the table contents |
| `date_created` | string | no | Date the table was created |
| `creator` | string/object/array | no | Person or organization that created the table (string, object, or array of objects) |
| `file_hash` | string | no | SHA-256 hash of the CSV file for integrity verification (lowercase hex) |
| `license` | string | no | License identifier in SPDX format (e.g., CC-BY-4.0, MIT, Apache-2.0) |
| `table_schema` | object | yes | Schema describing the structure and properties of columns in the CSV table |

### Column properties

These appear inside each object in `table_schema.columns`. Several constraints are conditional (e.g. `format` is forbidden for `categorical`/`ordered`; `levels` is required for them; `minimum`/`maximum` apply only to numeric datatypes) — see the per-property pages for the rules.

| Property | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Column name (must match CSV header) |
| `label` | string | no | Human-readable label |
| `description` | string | no | Detailed description of the column |
| `datatype` | enum | no | Data type of the column |
| `format` | string | no | Format pattern or constraint for values (forbidden when datatype is categorical or ordered) |
| `unit` | string | no | Unit of measurement (e.g., 'kg', '°C', 'mol/L') |
| `levels` | array | no | Factor levels for categorical or ordered datatypes (strings or numbers; integers count as numbers) |
| `minimum` | number | no | Minimum value for numeric columns |
| `maximum` | number | no | Maximum value for numeric columns |
| `min_length` | integer | no | Minimum string length |
| `max_length` | integer | no | Maximum string length |
| `null` | string/array | no | String(s) representing null values |
| `na_strings` | array | no | Additional missing value codes |
| `required` | boolean | no | Whether column values are required (not null) |
| `virtual` | boolean | no | Whether column is virtual (not in CSV) |

## CSVW Pass-Through Properties

All standard CSVW properties pass through unchanged. The bcsv JSON-LD context declares the following CSVW terms so they expand to the correct W3C CSVW IRIs; consult the [W3C CSVW spec](https://www.w3.org/TR/tabular-data-primer/) for their semantics.

- `propertyUrl`, `valueUrl`, `aboutUrl` — URI templates for RDF mapping.
- `foreignKeys` — referential-integrity declarations.
- `default`, `separator`, `suppressOutput`, `rowTitles` — column-cell handling.
- `length`, `base` — additional value constraints.

These properties are not validated by `bcsv/schema.json`. If you need to use them, refer to the CSVW spec.

**Naming convention.** Where bcsv actively validates a CSVW property (e.g., `primary_key`, which bcsv checks for composite uniqueness), it is renamed to snake_case. Properties bcsv passes through without validation (e.g., `foreignKeys`) keep their CSVW casing. The renamed `primary_key` is documented above under `table_schema`; the underlying IRI is still the W3C CSVW IRI for primary key.

## Dialect

The optional top-level `dialect` object carries CSV serialization hints, mirroring the [CSVW dialect description](https://www.w3.org/TR/tabular-metadata/#dialects).

**Honored in v0:** `delimiter`, `encoding`.

**Pass-through:** all other CSVW dialect sub-properties (`quoteChar`, `lineTerminators`, `header`, `commentPrefix`, etc.). Schema validation accepts them — `dialect` declares `additionalProperties: true` — but bcsv tooling does not interpret them. Consumer tooling MAY emit a `DIALECT_UNSUPPORTED` warning when it encounters an unhonored sub-property; schema validation does not reject them.

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

**Current version**: v26.0605  
**Format**: Calendar versioning (vYY.MMDD)

Older versions are available in the [`versions/`](versions/) directory.

Calver versioning does not telegraph breaking changes. Consumers SHOULD pin to a specific snapshot under `versions/` for production use:

```
https://behaverse.org/schemas/bcsv/versions/v26.0605/schema.json
```

Snapshots under `versions/` are immutable once published. Breaking changes are announced under a new calver tag with an explicit "Breaking" callout in [`CHANGELOG.md`](CHANGELOG.md). Unversioned URLs (e.g., `bcsv/schema.json` without the `versions/...` prefix) always serve the latest release and MAY change without notice.

## Contributing

Issues and suggestions can be submitted to the [GitHub repository](https://github.com/behaverse/schemas/issues).

## License

This schema is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).


## AI Usage Disclosure 

This document was created with assistance from AI tools.