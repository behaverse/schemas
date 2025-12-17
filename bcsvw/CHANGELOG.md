# BCSVW Schema Changelog

All notable changes to the BCSVW schema will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses [Calendar Versioning](https://calver.org/) (YY.MMDD).

## [25.1201] - 2025-12-01

### Added
- Initial schema with license property (SPDX format)
- Renamed `tableSchema` to `table_schema` for consistency
- Core properties: @context, name, url, title, description, etc.
- Column definitions with metadata (name, title, datatype, required, etc.)
