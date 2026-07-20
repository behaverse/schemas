# Vocabulary Changelog

All notable changes to the vocabulary (SKOS concept schemes + concepts) will be
documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project uses [Calendar Versioning](https://calver.org/) (YY.MMDD).

## [26.0703] - 2026-07-03

### Fixed
- `terms.jsonld` was invalid JSON-LD: its context aliased both `schemes` and
  `concepts` to `@graph`, which JSON-LD 1.1 processors reject as "colliding
  keywords" — pyld could not expand the document at all. The two keys now map to
  distinct containment properties (`bdm:schemes` / `bdm:concepts`, `@container:
  @set`). **The JSON shape is unchanged** (consumers still read `schemes` and
  `concepts` arrays); only the RDF expansion differs: scheme/concept nodes are now
  linked from the vocabulary node via those properties instead of being asserted
  as (unreachable, since expansion failed) default-graph nodes.
- CI now expands `terms.jsonld` with pyld on every run, so this class of bug
  cannot ship again.

### Notes
- This is the vocabulary's first CHANGELOG entry; earlier releases (`26.0611` and
  before) predate it. See the git history of `terms.yaml` for prior changes.
