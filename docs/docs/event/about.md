---
id: about
title: About
sidebar_label: About
---

<!-- THIS FILE IS MANUALLY EDITABLE -->

# About event

The **Behaverse Event Schema** captures *raw experimental events* for cognitive tests, questionnaires, and games. It is the **Events** layer of the [Behaverse Data Model (BDM)](https://behaverse.org/data-model); the task-level aggregates analysts usually work with live in the [trial schema](https://behaverse.org/schemas/trial).

## Motivation

Behaverse spans many task types, each historically logging events its own way. The event schema unifies them under a single **xAPI-style envelope** — *actor / verb / object* — carrying one canonical `bdm:` vocabulary, so a single set of analytics tooling can process every domain. Continuous signals (mouse, keyboard, EEG, …) are referenced via `attachments` rather than inlined, keeping each event small.

## Vocabulary at a glance

- **24 verbs** across 6 layers: RuntimeInstance lifecycle, presentation, agent interaction, system, recording, and navigation.
- **15 object types** — RuntimeInstance, Screen, Panel, Stimulus, Option, Trial, UIComponent, Window, Feedback, ConsentForm, Consent, Recording, Timer, Scorer, LocaleSwitch.
- **5 actor types** — Agent, Group, Engine, Orchestrator, Researcher.
- **`bdm:*` extension keys** (open by design) carry response data, the scoping hierarchy, environment, and interaction-specific payloads under `result.extensions` / `context.extensions`.

The **Verbs**, **Object types**, and **Actor types** pages in the sidebar list the full controlled vocabulary; **Event envelope** is the per-field reference.

## Scoping hierarchy

Each event is positioned in a five-level hierarchy carried in `context.extensions`:
**session → activity → RuntimeInstance → block → trial**. The Activity-vs-RuntimeInstance distinction separates *what was planned* from *a specific execution* (a restart produces a distinct RuntimeInstance).

## Relationship to standards

The envelope follows the **xAPI** (Experience API) actor/verb/object shape; the `bdm:` vocabulary is the Behaverse-specific extension. The schema ships a JSON Schema (Draft 2020-12) and a JSON-LD context (`bdm:`, `xapi:`, `schema:`, `as2:`).

## Namespace & source

- **Namespace:** `https://behaverse.org/schemas/event#`
- **Source of truth:** `field-definitions.yaml` (envelope + vocabulary) drives the docs and the `field-definitions.json` render contract. **Note:** `schema.json` and `context.jsonld` are currently *hand-maintained alongside* the YAML, not generated from it.

## Status

Work in progress, relocated and canonicalized from the Behaverse questionnaire project. A tighter per-verb `result` contract is a tracked follow-up.
