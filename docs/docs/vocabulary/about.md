---
id: about
title: About
sidebar_label: About
---

<!-- THIS FILE IS MANUALLY EDITABLE -->

# About vocabulary

The **Behaverse Vocabulary** is a cross-cutting [SKOS](https://www.w3.org/2004/02/skos/)-style controlled terminology for Behaverse data. It collects the terms that **no single schema owns** — general terms, demographics, and the naming conventions (suffixes) used across variable names in the [Behaverse Data Model (BDM)](https://behaverse.org/data-model).

## Motivation

Many terms recur across the BDM: a `*_mean` aggregation, an `age` demographic, a `*_id` foreign-key suffix. Defining these once, in a shared vocabulary, keeps variable naming consistent across schemas and datasets. Terms that a specific schema owns (e.g. the trial table fields) live in that schema instead.

## Structure

The vocabulary is organised as SKOS **concept schemes** (categories), each grouping a set of **concepts** (terms):

- **General** and **Demographics** — common measures and participant attributes.
- **Generic / Aggregation / Transformation / Referencing Suffixes** — the conventions for building variable names (e.g. `age_mean`, `age_log`, `participant_id`).

The [Overview](./) page lists every public scheme with its concepts, definitions, and (where applicable) data type.

## Namespace & source

- **Namespace:** `https://behaverse.org/schemas/vocabulary`
- **Source of truth:** `terms.yaml` (hand-maintained, SKOS-style schemes + concepts). A SKOS `terms.jsonld` is generated from it.

## Status

Some internal schemes and concepts are kept in the source for reference but are **excluded from this public glossary**.
