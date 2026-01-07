---
id: index
title: studyflow
sidebar_label: Overview
slug: /studyflow
---

<!-- THIS FILE IS AUTO-GENERATED. DO NOT EDIT MANUALLY. -->

# <img src={require('@site/static/assets/img/schema_S.png').default} height="80" style={{verticalAlign: 'middle'}} /> studyflow

**Version**: v25.1217.dev  
**Namespace**: `http://behaverse.org/schemas/studyflow`

LinkML schema for Behaverse Studyflow

## Properties

This schema defines **18 properties** for describing studyflow metadata.

### All Properties

| Property | Type | Requirement | Description |
|:---------|:-----|:------------|:------------|
| [Element](studyflow/Element) | `class` | optional | [Abstract] Base class for all elements in the Studyflow. |
| [Checklist](studyflow/Checklist) | `class` | optional | A checklist for the element. |
| [Study](studyflow/Study) | `class` | optional | Process definition for a Studyflow study. |
| [StartEvent](studyflow/StartEvent) | `class` | optional | StartEvent element type |
| [EndEvent](studyflow/EndEvent) | `class` | optional | EndEvent element type |
| [Activity](studyflow/Activity) | `class` | optional | [Abstract] Base class for all activities in the Studyflow. |
| [CognitiveTest](studyflow/CognitiveTest) | `class` | optional | CognitiveTest element type |
| [Questionnaire](studyflow/Questionnaire) | `class` | optional | Questionnaire element type |
| [Instruction](studyflow/Instruction) | `class` | optional | Instruction element type |
| [RandomGateway](studyflow/RandomGateway) | `class` | optional | RandomGateway element type |
| [Dataset](studyflow/Dataset) | `class` | optional | Base class for all datasets in the Studyflow. |
| [DatasetFormatEnum](studyflow/DatasetFormatEnum) | `enum` | optional | Format of the dataset (BDM, BIDS, Psych-DS, etc). |
| [BDMDataLevelEnum](studyflow/BDMDataLevelEnum) | `enum` | optional | BDM level of the data (events, trials, models). |
| [BIDSDataTypeEnum](studyflow/BIDSDataTypeEnum) | `enum` | optional | BIDS data type (e.g., anat, func, etc). |
| [AssignmentAlgorithmEnum](studyflow/AssignmentAlgorithmEnum) | `enum` | optional | The scheduling algorithm used for the assignment. |
| [ProbabilityDistributionEnum](studyflow/ProbabilityDistributionEnum) | `enum` | optional | The random statistical distribution used for the assignment. |
| [InstrumentEnum](studyflow/InstrumentEnum) | `enum` | optional | The type of instrument used to measure cognitive performance. |
| [BehaverseTaskEnum](studyflow/BehaverseTaskEnum) | `enum` | optional | BehaverseTaskEnum enumeration |

## Usage

See the [examples](./studyflow/examples) for practical usage patterns.

## Version History

The current version of `studyflow` is `v25.1217.dev`.

Older versions are available in the [`studyflow/versions/`](https://github.com/behaverse/schemas/tree/main/studyflow/versions) directory.
