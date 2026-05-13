---
id: index
title: bcsv
sidebar_label: Overview
slug: /bcsv
---

<!-- THIS FILE IS AUTO-GENERATED. DO NOT EDIT MANUALLY. -->

# <img src={require('@site/static/assets/img/schema_B.png').default} height="80" style={{verticalAlign: 'middle'}} /> bcsv

**Version**: v25.1201  
**Namespace**: `https://behaverse.org/schemas/bcsv`

JSON Schema for BCSV (Behaverse CSV) metadata files

## Properties

This schema defines **25 properties** for describing bcsv metadata.

### Table Properties

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [@context](bcsv/@context) | `string` | optional | JSON-LD context URL |
| [name](bcsv/name) | `string` | optional | Short URL-friendly identifier |
| [url](bcsv/url) | `string` | optional | URL or path to the CSV file |
| [pretty_name](bcsv/pretty_name) | `string` | optional | Human-readable title for the table |
| [description](bcsv/description) | `string` | optional | Detailed description of the table contents |
| [date_created](bcsv/date_created) | `string` | optional | Date the table was created |
| [creator](bcsv/creator) | `string` | optional | Person or organization that created the table (string or array of objects) |
| [file_hash](bcsv/file_hash) | `string` | optional | SHA-256 hash of the CSV file for integrity verification |
| [license](bcsv/license) | `string` | optional | License identifier in SPDX format (e.g., CC-BY-4.0, MIT, Apache-2.0) |
| [table_schema](bcsv/table_schema) | `object` | optional | Schema describing the structure and properties of columns in the CSV table |

### Column Properties

These properties are used within the `table_schema.columns` array to describe individual columns.

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [name](bcsv/name) | `string` | required | Column name (must match CSV header) |
| [label](bcsv/label) | `string` | optional | Human-readable label |
| [description](bcsv/description) | `string` | optional | Detailed description of the column |
| [datatype](bcsv/datatype) | `enum` | optional | Data type of the column |
| [format](bcsv/format) | `string` | optional | Format pattern or constraint for values |
| [unit](bcsv/unit) | `string` | optional | Unit of measurement (e.g., 'kg', '°C', 'mol/L') |
| [levels](bcsv/levels) | `array` | optional | Factor levels for categorical variables |
| [minimum](bcsv/minimum) | `number` | optional | Minimum value for numeric columns |
| [maximum](bcsv/maximum) | `number` | optional | Maximum value for numeric columns |
| [min_length](bcsv/min_length) | `integer` | optional | Minimum string length (snake_case alias for minLength) |
| [max_length](bcsv/max_length) | `integer` | optional | Maximum string length (snake_case alias for maxLength) |
| [null](bcsv/null) | `string` | optional | String(s) representing null values |
| [na_strings](bcsv/na_strings) | `array` | optional | Additional missing value codes |
| [required](bcsv/required) | `boolean` | optional | Whether column values are required (not null) |
| [virtual](bcsv/virtual) | `boolean` | optional | Whether column is virtual (not in CSV) |

## Usage

See the [examples](bcsv/examples) for practical usage patterns.

## Version History

The current version of `bcsv` is `v25.1201`.

Older versions are available in the [`bcsv/versions/`](https://github.com/behaverse/schemas/tree/main/bcsv/versions) directory.
