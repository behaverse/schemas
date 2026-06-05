# Schema Versioning System

This repository versions each schema with CalVer and archives every release so
consumers can pin to an immutable snapshot.

## Overview

- **CalVer (YY.MMDD)** version strings on every schema release.
- **Version archiving** — each release is copied to a per-version directory under
  `<schema_name>/versions/`.
- **Changelog** — every release is recorded in `<schema_name>/CHANGELOG.md`.
- **CI/CD** — the docs site redeploys when the `gh-pages` branch is pushed or the
  workflow is dispatched manually; the build fetches schema content from `main`.

> **Immutability commitment.** Snapshots under each schema's `versions/vYY.MMDD/`
> directory are never modified after publication. Once a snapshot is online,
> downstream consumers can safely pin to that URL.

## How to Version a Schema

Versioning is a deliberate manual process — there is no automation script. Doing
each step by hand keeps the author aware of whether a change is breaking. After
editing a schema:

1. **Bump the version.** Set the new CalVer (today, `YY.MMDD`) in two places in
   `<schema_name>/schema.json`:
   - the `version` field, and
   - the `$id` field →
     `https://behaverse.org/schemas/<schema_name>/v<new_version>/schema.json`.

2. **Update the changelog.** Prepend a section to `<schema_name>/CHANGELOG.md`:

   ```markdown
   ## [<new_version>] - <YYYY-MM-DD>

   ### Changed
   - Description of changes
   ```

   Use a `### Breaking` heading for backward-incompatible changes so consumers
   pinning to an older snapshot know why.

3. **Snapshot the new release.** Copy the current files into a per-version
   directory named for the *new* version:

   ```bash
   mkdir -p <schema_name>/versions/v<new_version>
   cp <schema_name>/{schema.json,context.jsonld,README.md} \
      <schema_name>/versions/v<new_version>/
   ```

   The snapshot's `schema.json` keeps the version and `$id` you just set, so it is
   a faithful, immutable copy of that release. (The previous release already has
   its own snapshot from when it shipped; if one is missing, create it the same
   way.)

4. **Commit and push.**

   ```bash
   git add <schema_name>/
   git commit -m "chore(<schema_name>): bump version to <new_version>"
   git push origin main
   ```

**Available schemas:** `bcsv`, `catalog`, `dataset`, `studyflow`.

## Version Format

We use [Calendar Versioning (CalVer)](https://calver.org/) with format `YY.MMDD`:
- `25.1204` = December 4, 2025
- `26.0115` = January 15, 2026

Multiple changes on the same day share one version number; list them all under
that version in the changelog.

## Pinning vs. latest

- **Unversioned URL** (e.g. `https://behaverse.org/schemas/bcsv/schema.json`)
  always serves the latest release and MAY change without notice.
- **Versioned URL** (e.g.
  `https://behaverse.org/schemas/bcsv/versions/v26.0605/schema.json`) is
  immutable. Consumers SHOULD pin to a versioned URL for production use.

Because CalVer does not telegraph breaking changes, the changelog's `### Breaking`
callouts are the authoritative signal that a new version is incompatible.

## Directory Structure

Each JSON-Schema-based schema (`bcsv`, `catalog`, `dataset`) has:

```
<schema_name>/
├── schema.json          # Current release
├── context.jsonld       # JSON-LD context
├── CHANGELOG.md         # Version history
├── README.md
└── versions/            # Immutable archived releases (one directory per version)
    ├── v25.1201/
    │   ├── schema.json
    │   ├── context.jsonld
    │   └── README.md
    └── v26.0605/
        └── ...
```

`studyflow` is LinkML-based (`schema.linkml.yaml`) and follows the same CalVer +
changelog conventions; its archive layout may differ.

## Documentation Deployment

The `deploy-docs.yml` workflow lives on the **`gh-pages`** branch (the repo's CI was
consolidated there). It runs on a push to `gh-pages` or via manual dispatch
(GitHub Actions → "Deploy Documentation" → Run workflow, or
`gh workflow run deploy-docs.yml --ref gh-pages`). At build time it fetches the
`bcsv/`, `catalog/`, `dataset/`, and `studyflow/` directories from `main`,
regenerates the Docusaurus site, and deploys to GitHub Pages.

**Important:** the workflow file is not present on `main`, so **pushing to `main`
does not by itself trigger a deploy.** After pushing schema changes to `main`,
trigger the workflow (push `gh-pages`, or dispatch it) to publish them.

## Workflow Summary

```
1. Edit schema.json (and context.jsonld / README.md as needed)
2. Bump version + $id in schema.json
3. Prepend a CHANGELOG entry (mark breaking changes)
4. Snapshot the new version under versions/v<new>/
5. Commit and push to main
6. Trigger the gh-pages deploy (push gh-pages, or dispatch deploy-docs.yml);
   it fetches main and redeploys the docs site
```
