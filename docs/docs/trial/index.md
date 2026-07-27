---
id: index
title: trial
sidebar_label: Overview
slug: /trial
---

<!-- THIS FILE IS AUTO-GENERATED. DO NOT EDIT MANUALLY. -->

# trial

**Version**: v26.0728
**Namespace**: `https://behaverse.org/schemas/trial`

Tidy tables describing trial-level behavioral data for cognitive tests and questionnaires, derived from raw events.


Trial-level data is organised as **11 tidy tables** (228 fields total), joined by `_id` foreign keys. Open a table to browse its fields.

| Table | Fields | Description |
|:------|------:|:------------|
| [Response](response.md) | 82 | Main table where each row describes a response in a trial. |
| [Stimulus](stimulus.md) | 20 | Describes each of the stimuli that were shown during a trial. |
| [Option](option.md) | 19 | Describes each option that a agent could choose from in a trial. |
| [Input](input.md) | 16 | A detailed log of all inputs and clicks recorded during the trial. |
| [StimulusComponent](stimulus-component.md) | 14 | Stimuli can comprise multiple components. This table describes each component of a stimulus. |
| [OptionComponent](option-component.md) | 15 | Options can comprise multiple components. This table describes each component of an option. |
| [Instrument](instrument.md) | 7 | Describes the instrument used for data acquisition. |
| [Subtrial](subtrial.md) | 20 | Per-stage detail for trials composed of successive, dependent stages, each with its own stimulus → response → outcome cycle (e.g., the two-step task). The trial row in `Response` remains THE unit and carries the trial-level (aggregate or final) response and evaluation; each `Subtrial` row is a miniature trial anatomy for one stage. |
| [Studyflow](studyflow.md) | 15 | The run log: one row per activity run — a single execution of one activity by one agent, with restarts counted as separate runs. Shipped as `studyflow.csv` in the agent's folder. This is the REALIZED record of what an agent actually did; it is not the study-level plan (the BPMN studyflow diagram authored in the `studyflow` schema family), which describes what was designed to happen. |
| [TrialParameter](trial-parameter.md) | 10 | Per-trial (and per-subtrial) ground-truth GENERATIVE task parameters — latent task state, not behavior — in long format: one row per parameter, per grid cell, per trial. These are the values that vary from trial to trial within a run, such as a two-step task's drifting reward probabilities. Serves simulation, parameter recovery, and engine calibration. |
| [TaskParameter](task-parameter.md) | 10 | Per-activity-run ground-truth GENERATIVE task parameters — latent task state, not behavior — in long format: one row per parameter and grid cell per run. These are the values that stay constant across one run of an activity but vary between runs and agents, such as a per-agent fixed reward mapping or a per-group volatility level. |