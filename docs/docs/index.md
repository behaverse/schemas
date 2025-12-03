---
slug: /
---

<!-- THIS FILE IS MANUALLY EDITABLE -->

# Behaverse Schemas Documentation

Welcome to the Behaverse Schemas documentation.

This site provides comprehensive documentation for all schema properties, with auto-generated pages from the schema definitions.

## Available Schemas

### [bcsvw](/bcsvw) - Behaverse CSV for the Web

Extension of W3C CSVW with support for R/Python data types including categorical and ordered factors, missing value codes, units of measurement, and file integrity verification.

**Key features:**
- `categorical` and `ordered` data types
- Rich metadata to describe tables and columns
- Missing value codes (NA strings)
- Units of measurement
- SHA-256 file hashing

### [collection](/collection) - Collection Schema

Metadata schema for describing thematic collections of datasets that share specific characteristics or serve particular research applications.

**Key features:**
- Inclusion/exclusion criteria
- Dataset membership management

### [dataset](/dataset) - Dataset Schema

Comprehensive metadata for cognitive science datasets with coverage of participant demographics, measurement techniques, cognitive tasks, and data access information.

**Key features:**
- 40+ metadata properties
- Population demographics
- Measurement techniques (e.g., EEG, fMRI, eye tracking)
- Activities (e.g., cognitive tasks, questionnaires)
- Ethics

### [studyflow](/studyflow) - Studyflow Schema

Schema for defining the formal structure of studyflow diagrams - sequences of activities and resources designed to facilitate experimental research and data analysis.

**Key features:**
- Activity sequences
- Resource management
- Visual modeling support

## Quick Links

- [GitHub Repository](https://github.com/behaverse/schemas)
- [Behaverse Platform](https://behaverse.org)
- [License: CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## Using This Documentation

Each schema has:

1. **Overview page** - Introduction and quick reference
2. **Property pages** - Detailed documentation for each property with:
   - Type information
   - Status (required/recommended/optional)
   - Namespace URIs
   - Mappings to standard vocabularies
   - Constraints and validation rules
   - Examples
3. **Example pages** - Real-world usage patterns

## Search

Use the search bar at the top to find specific properties or concepts across all schemas.

## Versioning

All schemas use **Calendar Versioning (CalVer)** with format: `vYY.MMDD`

Property URIs remain stable across versions, ensuring backward compatibility.

## Contributing

We welcome feedback and suggestions for improving these schemas!

If you have ideas for new properties, improvements to existing definitions, or have found issues, please:

1. [Open an issue](https://github.com/behaverse/schemas/issues) on GitHub describing your suggestion or concern
2. We will review and discuss the proposal
3. Approved changes will be implemented by the maintainers

**Note:** Please do not submit pull requests directly to the schema files. All contributions should begin with an issue for discussion.
