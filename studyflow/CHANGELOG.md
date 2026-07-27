# Studyflow Schema Changelog

All notable changes to the Studyflow schema will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses [Calendar Versioning](https://calver.org/) (YY.MMDD).

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
