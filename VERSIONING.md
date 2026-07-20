# Schema Versioning System

This repository versions each schema with CalVer and archives every release so
consumers can pin to an immutable snapshot.

## Overview

- **CalVer (YY.MMDD)** version strings on every schema release.
- **Version archiving** — each release is copied to a per-version directory under
  `<schema_name>/versions/`.
- **Changelog** — every release is recorded in `<schema_name>/CHANGELOG.md`.
- **CI/CD** — the docs site redeploys on every push to `main` (and on pushes to
  `gh-pages`, or manual dispatch); the build fetches schema content from `main`.

> **Immutability commitment.** Snapshots under each schema's `versions/vYY.MMDD/`
> directory are never modified after publication. Once a snapshot is online,
> downstream consumers can safely pin to that URL.

## How to Version a Schema

Versioning is a deliberate manual process — there is no automation script. Doing
each step by hand keeps the author aware of whether a change is breaking. For the
generated schemas (catalog, dataset, trial, event), you edit the LinkML **source** and
regenerate; never hand-edit the generated `schema.json`/`context.jsonld`.

1. **Bump the version in the source.** Set the new CalVer (today, `YY.MMDD`) in the
   `version:` field of `<schema_name>/schema.linkml.yaml`. (Other sources: **studyflow** —
   also `schema.linkml.yaml` (consumed directly, nothing to regenerate); **bcsv** is
   hand-maintained — set `version` *and* `$id` directly in `bcsv/schema.json`;
   **vocabulary** — set `version` in `vocabulary/terms.yaml`.)

2. **Regenerate the artifacts.** This also writes the versioned, self-identifying
   `$id` (`…/v<new_version>/schema.json`) automatically. (studyflow has no generated
   artifact — skip; bcsv is hand-maintained — skip.)

   ```bash
   python scripts/generate.py                  # catalog / dataset / trial / event
   python vocabulary/scripts/generate.py       # vocabulary (terms.jsonld)
   ```

3. **Update the changelog.** Prepend a section to `<schema_name>/CHANGELOG.md`:

   ```markdown
   ## [<new_version>] - <YYYY-MM-DD>

   ### Changed
   - Description of changes
   ```

   Use a `### Breaking` heading for backward-incompatible changes so consumers
   pinning to an older snapshot know why.

4. **Snapshot the new release.** Copy the *generated* artifacts into a per-version
   directory named for the new version (which artifacts exist varies by schema —
   catalog/dataset: `schema.json` + `context.jsonld`; trial: `schema.json` +
   `field-definitions.json`; event: both plus `context.jsonld`; bcsv: `schema.json` +
   `context.jsonld`):

   ```bash
   mkdir -p <schema_name>/versions/v<new_version>
   cp <schema_name>/{schema.json,context.jsonld} \
      <schema_name>/versions/v<new_version>/
   ```

   The snapshot keeps the `version`/`$id` just generated, so it is a faithful,
   immutable copy of that release. (The previous release already has its own
   snapshot; if one is missing, create it the same way.)

5. **Commit and push.** Pushing to `main` regenerates+redeploys the docs site (CI
   also fails if the committed artifacts drift from the regenerated source).

   ```bash
   git add <schema_name>/
   git commit -m "chore(<schema_name>): bump version to <new_version>"
   git push origin main
   ```

**Available schemas:** `bcsv`, `catalog`, `dataset`, `trial`, `event`, `timeseries`,
`studyflow`, `vocabulary`.

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

A generated LinkML-sourced schema (`catalog`, `dataset`, `trial`, `event`) has:

```
<schema_name>/
├── schema.linkml.yaml   # Source of truth (hand-edited)
├── schema.json          # Generated — current release
├── context.jsonld       # Generated JSON-LD context (not for trial)
├── field-definitions.json  # Generated render artifact (trial, event only)
├── CHANGELOG.md         # Version history
├── README.md
└── versions/            # Immutable archived releases (one directory per version)
    ├── v26.0610/
    │   ├── schema.json
    │   └── context.jsonld
    └── v26.0615/
        └── ...
```

`studyflow` is LinkML (`schema.linkml.yaml`) but is consumed directly (no generated
`schema.json`); it archives its LinkML source under `versions/`. `bcsv` has the same layout
as the generated schemas but is **hand-maintained** (no `schema.linkml.yaml`; edit
`schema.json`/`context.jsonld` directly). `vocabulary` is a SKOS resource: source
`terms.yaml` → generated `terms.jsonld` (no `schema.json`). All follow the same CalVer +
changelog conventions.

## Documentation Deployment

The build+deploy is defined once, in the reusable workflow
`main:.github/workflows/build-deploy-pages.yml` (`on: workflow_call`). It checks out the
Docusaurus site from **`gh-pages`**, fetches the schema directories from `main`, regenerates
the site, and deploys to GitHub Pages. Two thin triggers call it:

- `main:deploy-on-main.yml` — on every push to `main`, **so pushing schema changes to
  `main` publishes them automatically** (no separate deploy step needed).
- `gh-pages:deploy-docs.yml` — on pushes to `gh-pages` (manual site edits), via
  `uses: behaverse/schemas/.github/workflows/build-deploy-pages.yml@main`.

Manual dispatch: GitHub Actions → "Deploy docs (main)" → Run workflow, or
`gh workflow run deploy-on-main.yml --ref main`. Verify against
`https://behaverse.github.io/schemas/...` first — `behaverse.org` is Cloudflare/Varnish-cached
(~10 min) and lags.

## Workflow Summary

```
1. Edit the source of truth (schema.linkml.yaml; or schema.json for bcsv, terms.yaml for vocabulary)
2. Bump the version in the source
3. Regenerate: python scripts/generate.py  (writes schema.json/context.jsonld + the versioned $id)
4. Prepend a CHANGELOG entry (mark breaking changes)
5. Snapshot the new version under versions/v<new>/
6. Commit and push to main — CI validates + the docs site redeploys automatically
```
