---
id: index
title: collection
sidebar_label: Overview
slug: /collection
---

<!-- THIS FILE IS AUTO-GENERATED. DO NOT EDIT MANUALLY. -->

# <img src={require('@site/static/assets/img/schema_C.png').default} height="80" style={{verticalAlign: 'middle'}} /> collection

**Version**: v25.1202  
**Namespace**: `https://behaverse.org/schemas/collection`

A metadata schema for thematic collections of cognitive science and neuroscience datasets

## Properties

This schema defines **12 properties** for describing collection metadata.

### Core Metadata

Essential fields for collection identification

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [name](collection/name) | `string` | required | Short URL-friendly identifier |
| [pretty_name](collection/pretty_name) | `string` | required | Human-readable display title |
| [description](collection/description) | `string` | required | Comprehensive description of the collection's purpose and scope |
| [keywords](collection/keywords) | `array` | recommended | Keywords describing the collection's focus areas |
| [date_created](collection/date_created) | `string` | recommended | Date this collection was created (ISO 8601) |
| [date_modified](collection/date_modified) | `string` | optional | Date this collection definition was last modified (ISO 8601) |
| [curator](collection/curator) | `array` | recommended | People or organizations that curate this collection |

#### Curator Object

Each curator in the `curator` array is an object with the following properties:

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [name](collection/curator/name) | `string` | required | Curator full name |
| [email](collection/curator/email) | `string` | optional | Curator email address (format: email) |
| [orcid](collection/curator/orcid) | `string` | optional | ORCID identifier (format: 0000-0000-0000-0000) |
| [affiliation](collection/curator/affiliation) | `string` | optional | Institutional affiliation |

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


### Collection Definition

Criteria and scope of the collection

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [inclusion_criteria](collection/inclusion_criteria) | `array` | required | Specific rules a dataset must meet to be included in this collection (all criter... |
| [exclusion_criteria](collection/exclusion_criteria) | `array` | optional | Criteria that would exclude a dataset from this collection |


### Collection Membership

Datasets that belong to this collection

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [datasets](collection/datasets) | `array` | optional | List of dataset URLs or DOIs that belong to this collection (use stable identifi... |
| [dataset_count](collection/dataset_count) | `integer` | optional | Number of datasets currently in this collection |


### Relationships

Related collections and cross-references

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [related_collections](collection/related_collections) | `array` | optional | Names of other collections that frequently overlap with this one |



## Usage

See the [examples](collection/examples) for practical usage patterns.

## Version History

The current version of `collection` is `v25.1202`.

Older versions are available in the [`collection/versions/`](https://github.com/behaverse/schemas/tree/main/collection/versions) directory.
