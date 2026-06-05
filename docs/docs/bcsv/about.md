---
id: about
title: About
sidebar_label: About
---

<!-- THIS FILE IS MANUALLY EDITABLE -->

# <img src={require('@site/static/assets/img/schema_B.png').default} height="80" style={{verticalAlign: 'middle'}} /> About bcsv

bcsv stands for **Behaverse CSV**; it is an extension of the [W3C CSV on the Web (CSVW)](https://www.w3.org/TR/tabular-data-primer/) standard designed to enhance CSV metadata for use in R and Python data analysis workflows.

## Motivation

CSV files are ubiquitous in data science, but they often lack the metadata needed to correctly interpret their contents. The [W3C CSV on the Web (CSVW)](https://www.w3.org/TR/tabular-data-primer/) standard provides a foundation for describing tabular data, but it was designed primarily for web publishing and lacks several features essential for modern data analysis workflows. bcsv aims to bridge this gap.

## Features

### 1. Categorical Variables

CSVW defines many data types (`string`, `integer`, `number`, `boolean`, `date`, etc.), but lacks native support for **categorical variables** (factors) — one of the most fundamental data types in statistics and data science.

bcsv adds `categorical` and `ordered` data types that map directly to:

- **R**: `factor()` and `ordered()`
- **Python**: `pd.Categorical()` with the `ordered` parameter

### 2. Rich Metadata via Dublin Core

CSVW lacks properties for common metadata fields essential for documentation and discovery. bcsv incorporates properties from Dublin Core and other vocabularies — `description`, `creator`, `date_created`, and a human-readable `pretty_name` — making datasets more discoverable and self-documenting.

### 3. Units of Measurement

CSVW has no standardized way to record units for numeric columns. bcsv adds a `unit` property for SI and custom units (e.g., `"kg"`, `"°C"`, `"mol/L"`, `"years"`).

### 4. Missing Value Semantics

CSVW's `null` allows a single missing-value representation. Real data often uses several codes (`NA`, `N/A`, `missing`, `BDL` for "Below Detection Limit", …). bcsv adds `na_strings` to declare additional missing-value codes alongside `null`.

### 5. Data Integrity

Metadata and data files can drift apart. bcsv adds a `file_hash` property (SHA-256) so metadata can be cryptographically tied to the correct data file.

### 6. Consistent Naming

bcsv uses `snake_case` consistently (e.g., `min_length`, `max_length`, `na_strings`). Where bcsv actively validates a CSVW property it renames it to snake_case; properties it merely passes through keep their CSVW casing.

## Benefits

### For Data Producers

- **Self-documenting data**: metadata travels with the data
- **Type safety**: explicit data types catch errors early
- **Reproducibility**: file hashing ties metadata to the exact data file
- **Standards-based**: built on W3C recommendations

### For Data Consumers

- **Immediate usability**: load a CSV with the correct types in one step
- **Rich metadata**: labels, descriptions, and units embedded in the structure
- **Cross-platform**: the same metadata serves R, Python, and other tools
- **Validation**: constraints (min/max, string length) enable automatic quality checks

### For the Ecosystem

- **CSVW-aligned**: bcsv builds on CSVW; valid bcsv files work with permissive CSVW readers (strict CSVW validators will flag the `categorical`/`ordered` extensions)
- **Semantic-web ready**: a JSON-LD context maps properties to standard vocabularies
- **Tool-agnostic**: any tool that reads CSVW can read the CSVW subset of bcsv

## Relationship to Standards

bcsv builds on and references:

- **[W3C CSVW](https://www.w3.org/TR/tabular-data-primer/)**: core table and column definitions
- **[Dublin Core](https://www.dublincore.org/)**: metadata properties (`description`, `pretty_name` → `dc:title`)
- **[RDFS](https://www.w3.org/TR/rdf-schema/)**: the `label` property
- **[Schema.org](https://schema.org/)**: general vocabulary alignment
- **[XSD](https://www.w3.org/TR/xmlschema-2/)**: data type definitions

## Namespace

- **Base namespace**: `https://behaverse.org/schemas/bcsv#`
- **Context file**: `https://behaverse.org/schemas/bcsv/context.jsonld`

## Learn more

- **[Overview](/bcsv)** — the full property reference (auto-generated from the schema), with a page per property.
- **[Examples](examples)** — a complete worked CSV + metadata example.
- **[README on GitHub](https://github.com/behaverse/schemas/blob/main/bcsv/README.md)** — quick start, type mapping, dialect, and versioning details.
