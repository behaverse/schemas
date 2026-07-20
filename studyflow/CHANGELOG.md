# Studyflow Schema Changelog

All notable changes to the Studyflow schema will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses [Calendar Versioning](https://calver.org/) (YY.MMDD).

## [Unreleased]

### Fixed
- `Dataset.bidsDataType` default was `trials`, which is not a member of `BIDSDataTypeEnum`; it is now `beh` (behavioral data).
- `RandomGateway.probabilityFunction` was a free-text `string`; it now ranges over the (previously unused) `ProbabilityDistributionEnum`, matching its `uniform` default.
- `Dataset.bdmDataLevel` description listed a `summary` level that `BDMDataLevelEnum` does not define; the description now matches the enum (events, trials, models).

### Added
- Initial studyflow schema structure (LinkML YAML format)
- Moddle JSON format for workflow modeling
- Templates for study workflows
