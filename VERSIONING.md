# Schema Versioning System

This repository uses an automated versioning system for managing schema changes.

## Overview

The versioning system provides:
- **Automatic version bumping** using CalVer (YY.MMDD format)
- **Version archiving** - old versions stored in `versions/` directories
- **Changelog management** - automatic updates to `CHANGELOG.md`
- **CI/CD integration** - automated deployment of documentation

## How to Version a Schema

When you make changes to a schema, use the versioning script:

```bash
python scripts/version_schema.py <schema_name> --message "Description of changes"
```

**Available schemas:** `bcsvw`, `catalog`, `dataset`, `studyflow`

### Example

```bash
# Make changes to bcsvw/schema.json
# Then run:
python scripts/version_schema.py bcsvw --message "Add new validation rules for column types"

# Review the changes
git status

# Commit and push
git add bcsvw/
git commit -m "chore(bcsvw): bump version to 25.1204"
git push origin main
```

## What the Script Does

1. **Archives old version**: Copies current `schema.json` to `versions/schema-v<old_version>.json`
2. **Bumps version**: Updates the `version` field in `schema.json` to current date (YY.MMDD)
3. **Updates CHANGELOG**: Adds new entry to `CHANGELOG.md` with your change description
4. **Provides next steps**: Shows git commands to commit and push

## Version Format

We use [Calendar Versioning (CalVer)](https://calver.org/) with format `YY.MMDD`:
- `25.1204` = December 4, 2025
- `26.0115` = January 15, 2026

Multiple changes on the same day will have the same version number.

## Automated Checks

The repository includes GitHub Actions workflows:

### Version Check (PR validation)
- **Trigger**: Pull requests that modify schema files
- **Checks**: 
  - Version was bumped
  - Old version was archived
  - CHANGELOG was updated
- **File**: `.github/workflows/version-check.yml`

### Documentation Deployment
- **Trigger**: Push to main branch
- **Actions**:
  - Fetches docs infrastructure from `gh-pages` branch
  - Regenerates documentation from schemas
  - Deploys to GitHub Pages
- **File**: `.github/workflows/deploy-docs.yml`

## Directory Structure

Each schema has:
```
<schema_name>/
├── schema.json          # Current version
├── CHANGELOG.md         # Version history with changes
├── versions/            # Archived versions
│   ├── schema-v25.1201.json
│   ├── schema-v25.1202.json
│   └── schema-v25.1204.json
└── ...
```

## Manual Versioning (Not Recommended)

If you need to version manually:

1. Copy current schema to `versions/schema-v<old_version>.json`
2. Update `version` field in `schema.json`
3. Add entry to `CHANGELOG.md`:
   ```markdown
   ## [25.1204] - 2025-12-04
   
   ### Changed
   - Your change description
   ```
4. Commit: `git commit -m "chore(schema): bump version to 25.1204"`

## Troubleshooting

### "Version not bumped" error in PR
- Run the versioning script: `python scripts/version_schema.py <schema> --message "..."`
- The script will handle version, archiving, and changelog

### Multiple updates same day
- CalVer will show same version for multiple changes on one day
- This is normal - the changelog will list all changes under that version

### Dry run to preview changes
```bash
python scripts/version_schema.py bcsvw --message "Test" --dry-run
```

## Workflow Summary

```
1. Edit schema.json
2. Run version_schema.py
3. Review changes
4. Commit and push
5. PR validation checks version
6. Merge triggers documentation deployment
```

The system ensures all schema changes are tracked, versioned, and automatically reflected in the online documentation.
