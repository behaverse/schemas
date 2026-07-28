# Agent prompt: outstanding work in `behaverse/schemas`

_Copy everything below the line into a fresh agent session inside the **`behaverse/schemas`**
repository. Prepared 2026-07-28 by the `behaverse/data-model` project (its downstream
consumer). State below was verified against `origin/main` at `323e00f` and the live site on
2026-07-28. **Supersedes** `schemas-agent-brief.md` and `schemas-questionnaire-notes-brief.md`
in the data-model repo — most of their contents shipped in v26.0722–v26.0728._

---

You are working in `behaverse/schemas`, which owns the machine-readable Behaverse schemas.
Its main downstream consumer is `behaverse/data-model` (the Quarto docs site), which fetches
each family's `field-definitions.json` plus the vocabulary's `terms.jsonld` at build time and
generates its spec and glossary pages from them. Changes here therefore surface on
`behaverse.org/data-model/` automatically, and breaking the published artifact shape breaks
that build.

Before changing anything, read `README.md`, `VERSIONING.md`, `CONTRIBUTING.md`,
`scripts/generate.py`, and the CHANGELOG of any family you touch.

## Ground rules

- **LinkML is the source of truth.** Edit `<family>/schema.linkml.yaml` and regenerate with
  `python scripts/generate.py`; never hand-edit `schema.json` or `field-definitions.json`.
  `generate.py --check` must report no drift afterwards, and `scripts/validate_schemas.py`
  must pass.
- **Version deliberately** per `VERSIONING.md`: bump the CalVer in the source, regenerate,
  write the changelog entry, and copy the generated artifacts into `<family>/versions/v<ver>/`.
  Snapshots are immutable once published.
- **Terminology:** BDM says **agent**, never subject or participant, for the entity producing
  data. (The trial prose was cleaned in v26.0722 — keep it that way.)
- **Deploy order matters:** publish here first, then the data-model rebuilds against current.

## Verified state, 2026-07-28

| Family | `schema.json` | `field-definitions.json` | `context.jsonld` |
|---|---|---|---|
| trial | ✅ | ✅ | ❌ **missing** |
| event | ✅ | ✅ | ✅ |
| timeseries | ✅ | ❌ | — |
| studyflow | ❌ **none** | ❌ **none** | — |
| dataset, catalog, bcsv | ✅ | — | ✅ |
| vocabulary | — (`terms.jsonld`) | — | — |

Recently shipped, do not redo: run log + `runtime_id` + parameter-grain split (v26.0727),
questionnaire field notes and the note-severity convention (v26.0728), studyflow's first
tagged release, subject→agent prose (v26.0722), `SCHEMA_DIRS` centralized in
`build-deploy-pages.yml`.

---

## 1. Close or ship the two open GitHub issues

**Issue #11 — "trial: rename `session_id` → `session_index`, add a UUID `session_id`" —
appears already shipped.** `session_index` and `session_uuid` are both in the trial schema
(v26.0720). The issue is still open. Verify it is genuinely satisfied — note the deviation
that the UUID field was named `session_uuid`, **not** a re-typed `session_id` — then close it
with a comment recording that choice, or reopen the naming question deliberately.

**Issue #10 — `Response.stimulus_id` typing — NOT shipped.** It is still `range: integer` in
`trial/schema.linkml.yaml`. The request is to relax it to accept a string or an integer.
Decide and act: either implement it (a breaking change for anyone parsing it as an integer,
so version and changelog accordingly) or close the issue with the reasoning. Check whether
the same argument applies to sibling ids (`option_id`, `response_id`, `trial_index`) so the
family stays internally consistent.

## 2. `studyflow` publishes no artifacts at all

The `studyflow` family got its first tagged release, but `origin/main` contains **no
`schema.json` and no `field-definitions.json`** for it, and `studyflow` is absent from
`scripts/generate.py`'s `SCHEMAS` list. It is, however, in `SCHEMA_DIRS` for deployment.

Decide what `studyflow` is meant to publish and make the generator do it. This matters
downstream: the data-model site documents the studyflow format by hand because it has nothing
to render from.

**Beware a name collision while you work.** "Studyflow" now denotes two different things:

- the **`studyflow` family** — the study *design* (BPMN-based; the Studyflow Modeler's format,
  saved as `studyflow.xml` at a dataset's root);
- the **`Studyflow` table** in the *trial* family — the *run log* (`studyflow.csv`, one row
  per activity run, in each agent's folder).

Both are correct and both are documented on the data-model site, but the names invite
confusion. Consider whether the trial table should be renamed (e.g. `Run` or `ActivityRun`),
which would be a breaking change worth making early rather than late. If they keep their
names, say explicitly in both families' docs that the two are distinct.

## 3. `timeseries` publishes no `field-definitions.json`

`generate.py` has `{"name": "timeseries", "emits_field_definitions": False}`. Consequence:
the data-model site cannot render timeseries as a generated reference section the way it does
trial and event, so `spec/timeseries.qmd` is hand-written prose that can drift.

Flip it on and check the output is sensible for a schema whose primitive is a channel rather
than a table. If the field-definitions shape genuinely does not fit this family, say so in the
changelog and tell the data-model project, so it stops waiting for it.

## 4. `trial/context.jsonld` is still missing

`generate.py` marks trial `emits_context: False`; every other generated family emits a
JSON-LD context. Add the prefixes and `slot_uri` mappings to `trial/schema.linkml.yaml` (use
`event/schema.linkml.yaml` as the model — note trial is multi-table, so check the generator
handles per-class contexts), flip the flag, regenerate, validate by round-tripping an example
through a JSON-LD processor, and snapshot.

## 5. Legacy site paths in trial field text

`trial/schema.linkml.yaml` still contains **4 occurrences** of `/spec/general/2-dataset-cards.qmd`,
a path that stopped existing in the data-model's 2026-06 redesign. The data-model rewrites
them at build time (`LEGACY_LINKS` in its `scripts/build_spec.py`) purely as a stopgap.

Replace them with `/spec/dataset-cards.html` and tell the data-model project, which can then
delete that rewrite table. While you are there, consider whether schema field text should
contain site-relative links at all, or whether it should link to `behaverse.org/...`
absolutely so the text is correct wherever it is rendered.

## 6. Emit per-table slugs so the `_slug()` coupling can die

The data-model's `build_spec.py` recomputes each table's documentation URL with its own
`_slug()` (CamelCase → kebab-case), which **must** match `gh-pages:scripts/generate_docs.py`'s
`_slug()`. The two are character-identical today, but nothing enforces it: if this repo's URL
scheme changes, every outbound "Full reference →" link on the data-model site 404s silently.

Fix by publishing the answer instead of making consumers guess: add the slug (or the full docs
URL) per table in `field-definitions.json`. Then tell the data-model project so it can use the
published value and delete its copy of the function.

## 7. Remaining hardcoded schema lists

`SCHEMA_DIRS` centralized the deploy list, but two others remain and disagree with it:

- `scripts/validate_schemas.py`: `SCHEMAS = ["bcsv", "catalog", "dataset", "trial", "event", "timeseries"]`
  — omits **studyflow** and **vocabulary**, which are therefore deployed but never validated.
- `scripts/generate.py`: its own `SCHEMAS` list of dicts (which also omits studyflow).

Derive all of them from one manifest, so adding a family is a single edit. At minimum, bring
`validate_schemas.py` up to full coverage.

## 8. D2 — session-level scoring surface

The last unresolved BDM deviation (D1 and D3 are issues #10/#11; D4–D6 shipped). There is
currently no agreed home for scores computed at the session level rather than per trial.
Drafts are in the data-model repo under `_design/bdm_backlog_wip/`. Decide where such scores
live — a models schema, a dataset-level table, or explicitly out of scope — and record the
decision so it stops being an open question.

## 9. Consider whether `Studyflow` should lead the trial table order

The data-model site renders trial tables in the order this repo lists them, so `Response`
comes first and `Studyflow` ninth. Since `Studyflow` is the run log that every other table
references via `runtime_id`, it arguably belongs first. This is your call; if you change the
order, the site follows automatically on its next build.

## Method and output

- One coherent change-set per item; version and changelog anything that alters a published
  artifact.
- Verify against the live site (`https://behaverse.org/schemas/...`) rather than cached copies.
- Final output: per item — what changed, what you decided differently and why, and **anything
  `behaverse/data-model` must do in response** (e.g. delete `LEGACY_LINKS`, drop its `_slug()`,
  add a lockfile pin for a newly-publishing family). That last list is what the data-model
  agent will act on.
