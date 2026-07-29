# Studyflow Schema Changelog

All notable changes to the Studyflow schema will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses [Calendar Versioning](https://calver.org/) (YY.MMDD).

## [26.0803] - 2026-08-03

### Added
- `field-definitions.json` now publishes each enum-ranged field's value set as `values`
  (a list of `{value, description?}` objects) plus `values_exhaustive` — the
  artifact-shape addition introduced with trial v26.0803, applied uniformly to every
  family that ships `field-definitions.json`. Seven fields gain it (e.g.
  `CognitiveTest.behaverseTask`, `RandomGateway.algorithm`, `Dataset.bidsDataType`).
  `schema.json` validation is unchanged.
- Every field now publishes a non-null `type`, derived from its LinkML range (`enum`,
  `string`, `boolean`, `Checklist`, …) when no explicit `bdm_type` annotation exists.
  All 34 fields previously carried `type: null`, leaving the documentation site's Type
  column empty. Requested by `behaverse/data-model`.

## [26.0730] - 2026-07-30

### Added
- **The family publishes artifacts for the first time**: a generated `schema.json`
  (validation contract) and `field-definitions.json` (render contract). Until now this was
  the only LinkML family emitting nothing, so the documentation site had to describe the
  studyflow format by hand — prose that could drift from the schema with nothing to catch it.
  - This required the render emitter to read a class's *induced* slots rather than only its
    inline `attributes`: studyflow takes its fields from parents (`is_a`) and mixins
    throughout, so reading `attributes` alone published most classes as empty sections.

### Changed
- The run-log table in the `trial` schema was renamed `Studyflow` → **`StudyflowLog`**
  (trial v26.0730), and its file `studyflow.csv` → `studyflow_log.csv`, to end the collision
  with this family's name. The relationship is unchanged and now reads plainly:
  `studyflow.xml` is the plan, `studyflow_log.csv` is what happened.

## [26.0728] - 2026-07-28

**First tagged release.** The schema had been sitting at `25.1217.dev2` with no published
version, no snapshot, and no release entry; everything below had accumulated as
"Unreleased". It is now on the same CalVer + snapshot footing as the other families.
(Dated 26.0728 because the 26.0727 slot was already published and snapshots are immutable.)

### Changed
- Version `25.1217.dev2` → `26.0728`, the family's first stable release, archived under
  `versions/v26.0728/`.
- Removed a trailing block of commented-out placeholder classes (`DataCatalog`, `Tensor`,
  `Table`, `Snapshot`, `DataOperation`) left over from early drafting.
- README now states what this schema is *not*: it describes a studyflow **as designed** (the
  BPMN diagram authored in the Studyflow Modeler), whereas what an agent actually did is the
  `Studyflow` **run log** table in the `trial` schema (`studyflow.csv`, one row per activity
  run). The two are different levels and were easy to confuse once the run log was specified.

### Fixed
- `Dataset.bidsDataType` default was `trials`, which is not a member of `BIDSDataTypeEnum`; it is now `beh` (behavioral data).
- `RandomGateway.probabilityFunction` was a free-text `string`; it now ranges over the (previously unused) `ProbabilityDistributionEnum`, matching its `uniform` default.
- `Dataset.bdmDataLevel` description listed a `summary` level that `BDMDataLevelEnum` does not define; the description now matches the enum (events, trials, models).

### Added
- Initial studyflow schema structure (LinkML YAML format)
- Moddle JSON format for workflow modeling
- Templates for study workflows
