---
id: index
title: bcsvw
sidebar_label: Overview
slug: /bcsvw
---

<!-- THIS FILE IS AUTO-GENERATED. DO NOT EDIT MANUALLY. -->

# <img src={require('@site/static/assets/img/schema_B.png').default} height="80" style={{verticalAlign: 'middle'}} /> bcsvw

**Version**: v25.1201  
**Namespace**: `https://behaverse.org/schemas/bcsvw`

JSON Schema for BCSVW (Behaverse CSV for the Web) metadata files

## Properties

This schema defines **25 properties** for describing bcsvw metadata.

### Table Properties

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [@context](bcsvw/@context) | `string` | optional | JSON-LD context URL |
| [name](bcsvw/name) | `string` | optional | Short URL-friendly identifier |
| [url](bcsvw/url) | `string` | optional | URL or path to the CSV file |
| [pretty_name](bcsvw/pretty_name) | `string` | optional | Human-readable title for the table |
| [description](bcsvw/description) | `string` | optional | Detailed description of the table contents |
| [date_created](bcsvw/date_created) | `string` | optional | Date the table was created |
| [creator](bcsvw/creator) | `string` | optional | Person or organization that created the table (string or array of objects) |
| [file_hash](bcsvw/file_hash) | `string` | optional | SHA-256 hash of the CSV file for integrity verification |
| [license](bcsvw/license) | `string` | optional | License identifier in SPDX format (e.g., CC-BY-4.0, MIT, Apache-2.0) |
| [table_schema](bcsvw/table_schema) | `object` | optional | Schema describing the structure and properties of columns in the CSV table |

### Column Properties

These properties are used within the `table_schema.columns` array to describe individual columns.

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [name](bcsvw/name) | `string` | required | Column name (must match CSV header) |
| [label](bcsvw/label) | `string` | optional | Human-readable label |
| [description](bcsvw/description) | `string` | optional | Detailed description of the column |
| [datatype](bcsvw/datatype) | `enum` | optional | Data type of the column |
| [format](bcsvw/format) | `string` | optional | Format pattern or constraint for values |
| [unit](bcsvw/unit) | `string` | optional | Unit of measurement (e.g., 'kg', '°C', 'mol/L') |
| [levels](bcsvw/levels) | `array` | optional | Factor levels for categorical variables |
| [minimum](bcsvw/minimum) | `number` | optional | Minimum value for numeric columns |
| [maximum](bcsvw/maximum) | `number` | optional | Maximum value for numeric columns |
| [min_length](bcsvw/min_length) | `integer` | optional | Minimum string length (snake_case alias for minLength) |
| [max_length](bcsvw/max_length) | `integer` | optional | Maximum string length (snake_case alias for maxLength) |
| [null](bcsvw/null) | `string` | optional | String(s) representing null values |
| [na_strings](bcsvw/na_strings) | `array` | optional | Additional missing value codes |
| [required](bcsvw/required) | `boolean` | optional | Whether column values are required (not null) |
| [virtual](bcsvw/virtual) | `boolean` | optional | Whether column is virtual (not in CSV) |

## Usage

See the [examples](bcsvw/examples) for practical usage patterns.

## Version History

The current version of `bcsvw` is `v25.1201`.

Older versions are available in the [`bcsvw/versions/`](https://github.com/behaverse/schemas/tree/main/bcsvw/versions) directory.
