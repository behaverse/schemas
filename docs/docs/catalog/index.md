---
id: index
title: catalog
sidebar_label: Overview
slug: /catalog
---

<!-- THIS FILE IS AUTO-GENERATED. DO NOT EDIT MANUALLY. -->

# <img src={require('@site/static/assets/img/schema_C.png').default} height="80" style={{verticalAlign: 'middle'}} /> catalog

**Version**: v26.0107  
**Namespace**: `https://behaverse.org/schemas/catalog`

A metadata schema for thematic catalogs of cognitive science and neuroscience datasets

## Properties

This schema defines **13 properties** for describing catalog metadata.

### Core Metadata

Essential fields for catalog identification

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [name](catalog/name) | `string` | required | Short URL-friendly identifier |
| [pretty_name](catalog/pretty_name) | `string` | required | Human-readable display title |
| [description](catalog/description) | `string` | required | Comprehensive description of the catalog's purpose and scope |
| [keywords](catalog/keywords) | `array` | recommended | Keywords describing the catalog's focus areas |
| [date_created](catalog/date_created) | `string` | recommended | Date this catalog was created (ISO 8601) |
| [date_modified](catalog/date_modified) | `string` | optional | Date this catalog definition was last modified (ISO 8601) |
| [curator](catalog/curator) | `array` | recommended | People or organizations that curate this catalog |

#### Curator Object

Each curator in the `curator` array is an object with the following properties:

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [name](catalog/curator/name) | `string` | required | Curator full name |
| [email](catalog/curator/email) | `string` | optional | Curator email address (format: email) |
| [orcid](catalog/curator/orcid) | `string` | optional | ORCID identifier (format: 0000-0000-0000-0000) |
| [affiliation](catalog/curator/affiliation) | `string` | optional | Institutional affiliation |

**Example:**
```json
{
  "curator": [
  {
    "name": "Curator Name",
    "email": "curator@institution.edu",
    "orcid": "0000-0001-2345-6789"
  }
]
}
```


### Catalog Definition

Criteria and scope of the catalog

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [inclusion_criteria](catalog/inclusion_criteria) | `array` | required | Specific rules a dataset must meet to be included in this catalog (all criteria ... |
| [exclusion_criteria](catalog/exclusion_criteria) | `array` | optional | Criteria that would exclude a dataset from this catalog |


### Catalog Membership

Datasets and child catalogs that belong to this catalog

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [datasets](catalog/datasets) | `array` | optional | List of dataset URLs or DOIs that belong to this catalog (use stable identifiers... |
| [catalogs](catalog/catalogs) | `array` | optional | List of child catalog URLs that belong to this catalog (for hierarchical organiz... |
| [dataset_count](catalog/dataset_count) | `integer` | optional | Number of datasets currently in this catalog |


### Relationships

Related catalogs and cross-references

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [related_catalogs](catalog/related_catalogs) | `array` | optional | Names of other catalogs that frequently overlap with this one |



## Usage

See the [examples](catalog/examples) for practical usage patterns.

## Version History

The current version of `catalog` is `v26.0107`.

Older versions are available in the [`catalog/versions/`](https://github.com/behaverse/schemas/tree/main/catalog/versions) directory.
