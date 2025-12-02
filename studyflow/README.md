# WIP: Behaverse Studyflow Schema

**Version:** v25.0414
**Namespace:** `https://behaverse.org/schemas/studyflow#`

## Overview

Studyflow schema defines the formal structure of studyflow diagrams. A studyflow represents a sequence of activities and resources designed to facilitate experimental research and data analysis.

Currently the main use case for the studyflow schema is to support the Studyflow Modeler app, which allows users to visually design and manage studyflows.

For detailed documentation, visit the [Studyflow Documentation](https://behaverse.org/studyflow-modeler/docs).


## Files

- [studyflow/schema.moddle.json](./schema.moddle.json): The schema definition for studyflow diagrams used by the Modeler app. It uses [moddle format](https://github.com/bpmn-io/moddle) for defining the structure of studyflow elements.
- [studyflow/templates.json](./templates.json): Predefined templates for common studyflow patterns to help users quickly create studyflows. This is also used by the bpmnjs in the Modeler app to provide composite elements in the palette.
