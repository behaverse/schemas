# Changelog

All notable changes to the Behaverse Agents Schema are documented in this file.

## [26.0804] - 2026-08-04

### Added

- Initial release of the `agents` family: the `Agent` table specifying `agents.csv` — one
  row per agent at the dataset root. Identity is the `agent_id` / `agent_index` pair
  (both required; `agent_id` is the key). Optional core attributes: `agent_type`
  (open enum: `human` · `non_human_animal` · `artificial`), `age` (years), `sex`
  (open enum), and `language` (BCP-47). Datasets may add custom columns.
- Per-agent data availability is deliberately out of scope: it is derivable from each
  agent's `studyflow_log.csv`, and duplicating it in the roster would invite drift.
