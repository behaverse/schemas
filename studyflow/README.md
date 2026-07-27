# WIP: Behaverse Studyflow Schema

**Version:** v25.1217.dev2
**Namespace:** `https://behaverse.org/schemas/studyflow#`

## Overview

Studyflow schema defines the formal structure of studyflow diagrams. A studyflow represents a sequence of activities and resources designed to facilitate experimental research and data analysis.

Currently the main use case for the studyflow schema is to support the Studyflow Modeler app, which allows users to visually design and manage studyflows.

For detailed documentation, visit the [Studyflow Documentation](https://behaverse.org/studyflow-modeler/docs).

> **The plan, not the run log.** This schema describes a studyflow *as designed* — the diagram of activities, gateways, and resources authored in the Studyflow Modeler. What an agent **actually did** is recorded per dataset in `studyflow.csv`, whose columns are defined by the `Studyflow` table in the [`trial`](../trial/) schema (one row per activity run, with `attempt`, `status`, and timing). The two are different levels: design-time artifact here, realized run log there.


## Files

- `schema.linkml.yaml`: The main LinkML schema file defining the Studyflow structure. It is used by the Studyflow Modeler app to extend BPMN and validate studyflow diagrams.
