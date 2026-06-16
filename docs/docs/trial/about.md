---
id: about
title: About
sidebar_label: About
---

<!-- THIS FILE IS MANUALLY EDITABLE -->

# About trial

The **Behaverse Trial Schema** defines a set of tidy tables describing *trial-level* behavioral data — the task-specific aggregates derived from raw events — for cognitive tests and questionnaires. It is the **Trials** layer of the [Behaverse Data Model (BDM)](https://behaverse.org/data-model).

## Motivation

A *trial* is a single instance of a participant interacting with a task. The information about a trial naturally spans several related entities — the response, the stimuli shown, the options offered, the raw inputs, and the instrument used. Rather than flatten that into one wide table, the trial schema models it as a small set of **tidy tables joined by `_id` foreign keys**, so each concern stays normalized and analysable.

## The tables

| Table | Fields | Description |
|-------|-------:|-------------|
| **Response** | 75 | Main table; one row per response in a trial. |
| **Stimulus** | 19 | Each stimulus shown during a trial. |
| **Option** | 18 | Each option a subject could choose from. |
| **Input** | 15 | Detailed log of inputs/clicks during the trial. |
| **StimulusComponent** | 13 | Components that make up a stimulus. |
| **OptionComponent** | 14 | Components that make up an option. |
| **Instrument** | 7 | The instrument (and its parameterizations) used for acquisition. |

Each table is a group in the sidebar; expand one to browse its fields, each of which has its own page.

## Conventions

- A trailing `_id` denotes a **foreign key** into the table of that name (e.g. `stimulus_id` → the **Stimulus** table).
- When several entities occur in one trial (e.g. multiple stimuli), their ids/values are concatenated into a single string on CSV export.

## Relationship to events

Trial-level data is *derived from* the raw event stream (the **Events** layer of the BDM — see the [event schema](https://behaverse.org/schemas/event)). Events capture what happened moment-to-moment; trials are the task-specific aggregates analysts work with.

## Namespace & source

- **Namespace:** `https://behaverse.org/schemas/trial#`
- **Source of truth:** `schema.linkml.yaml` (LinkML). The docs, the `field-definitions.json` render contract, and a per-table `schema.json` are all generated from it via `scripts/generate.py`.

## Status

Work in progress, relocated from `behaverse/data-model`. Published as-is while a handful of typing and structure follow-ups are tracked.
