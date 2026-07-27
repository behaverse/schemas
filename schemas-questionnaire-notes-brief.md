# Handoff — migrate questionnaire-specific field guidance into `behaverse/schemas`

> **For an agent working on `behaverse/schemas`.** Prepared 2026-07-27 from the
> `behaverse/data-model` side. Companion docs in that repo: `schemas-agent-brief.md`
> (the standing schemas work queue — read it too; this brief adds to it), `HANDOFF.md`
> (ecosystem and pipeline).

---

## 1. Why this exists

`behaverse/data-model`'s questionnaire guide (`guides/4-questionnaire-data.qmd`) carried a
field-by-field reference list: sixteen entries defining `stimulus_id`, `option_source`,
`response_numeric`, `score`, and so on. That duplicated what the trial schema already
publishes, and it drifted — the page documented a `trial_id` column that does not exist in
the schema, and a `response_time` definition that contradicted it.

The guide has now been rewritten to link to the generated reference instead. But some of
what it said was **not** redundant: it explained how the general trial fields behave *for
questionnaires specifically*. That guidance is a property of the fields, not of the task of
building a dataset, so it belongs with the field definitions — that is, in the schema.

**Your job:** move the guidance below into the trial schema as field-level notes, so it
appears automatically on `behaverse.org/schemas/trial/...` and on the data-model site's
generated `spec/trial/*` pages.

## 2. How field notes reach the documentation

```
trial/schema.linkml.yaml   (source of truth; per-slot annotations)
        │  scripts/generate.py
        ▼
trial/field-definitions.json   ──fetched by──►  data-model/scripts/build_spec.py
        │                                              │
        ▼                                              ▼
behaverse.org/schemas/trial/…              behaverse.org/data-model/spec/trial/…
```

- Each field in `field-definitions.json` carries `name / type / requirement / categories /
  description / range? / notes?`. **`notes` is the field you want.** `build_spec.py` already
  renders per-field notes on the data-model side (as "*Note:* …" after the description), so
  anything you add appears on both sites with no data-model change required.
- Do **not** hand-edit `field-definitions.json` — edit the LinkML source and regenerate
  (`python scripts/generate.py`), then confirm `--check` is a no-op.
- Deploy order matters: publish `behaverse/schemas` first, then rebuild data-model (it
  tracks current).

## 3. The guidance to migrate

Source: `data-model/guides/4-questionnaire-data.qmd` as it stood before the rewrite (git
history, or the pre-rewrite version in that repo). Below is the substance, per field. Wording
is a starting point — tighten to match schema house style, and keep BDM terminology
(**agent**, not subject/participant).

| Field (Response unless noted) | Note to add |
|---|---|
| `stimulus_index` | In a questionnaire, this is the position of the question: `stimulus_index = 1` is the first question presented, `= 23` the twenty-third. |
| `stimulus_description` | For questionnaires this holds the question text as presented, in English. When a question was shown in another language (recorded in `language`), the translations belong in the questionnaire's supplementary resources rather than in this column. |
| `stimulus_onset` | In questionnaires this is typically 0, since the question is usually present from the start of the trial. |
| `option_onset` | In questionnaires this is typically 0, since the options usually appear together with the question. |
| `option_id` | A question is often reused with different option sets (`agreement_7` vs `agreement_5`), and the resulting measures are not interchangeable. The combination of a question and its options is what the survey literature calls an **item**; BDM has no separate identifier for it — it is `stimulus_id` together with `option_id`. |
| `option_source` | Identifies where the option set came from (e.g., `likert_1_to_7`, `gender`). This is what lets a reader determine whether two datasets used the same scale, and it is the natural attachment point for psychometric metadata about that scale. |
| `response_description` | For questionnaires this is typically the label of the chosen option ("strongly agree"), the text entered in a free-text field, or a numeric entry. |
| `response_option_index` | Records which option was chosen by its position in the offered set. Essential whenever options are presented in a random order, since the label alone does not identify the choice. |
| `response_numeric` **and** `score` | **The most important item in this list — see §4.** |

### Fields whose guide text was redundant (do NOT migrate)

`stimulus_id`, `stimulus_duration`, `option_duration`, `response_time`, `accuracy`,
`correct` — the guide restated the schema's own definitions. Nothing to add.

## 4. The `response_numeric` / `score` distinction (highest value)

This is the one piece of guidance that materially affects whether a questionnaire dataset is
usable, and it is currently stated **only** in the data-model guide. It should be in the
schema, on both fields:

> `response_numeric` is a numeric reading of what the agent chose, independent of the
> question asked ("never" → 0, "always" → 1). It is empty for free-text answers, and equal to
> `response_description` when the agent entered a number. It is **not** an encoding of the
> scoring.
>
> `score` is the value the experimenter assigns to that answer in this particular context.
> In the BIS/BAS questionnaire, answering "very true for me" yields a score of 1 for some
> items, 4 for reverse-coded items, and 0 for filler items; item scores are then aggregated
> into questionnaire-level scores.
>
> Both are required. When they are collapsed into a single column, a reader cannot tell
> whether the numbers are raw answers, option positions, or already reverse-coded — which
> arguably makes the dataset unusable.

Consider whether this warrants a `.warning`-level note rather than a plain one (see §6).

## 5. Related: the attempt suffix is being removed (owner decision, 2026-07-27)

Separate from the notes work, but a schema change with the same downstream path:

The owner has decided to **drop the attempt suffix from data filenames** — `response.csv`
rather than `response_1.csv`, and correspondingly for `stimulus`, `option`, `input`,
`events`, and timeseries payloads.

- **Where it lives now:** the suffix is described in the trial schema's prose and in the
  data-model's folder-structure spec. Establish what the schema currently mandates before
  changing anything.
- **Decide what replaces it:** if multiple attempts remain representable, something else has
  to carry that information (a column in the Response table? a subfolder?). The guide
  previously argued the filename made attempt counts and incomplete data visible without
  opening files; if that property is being given up, say so deliberately in the changelog.
- **Downstream impact, measured 2026-07-27:** the suffix appears **60 times across 7
  data-model pages** (`response_1.csv` ×23, `mouse_1.ndjson.gz` ×8, `stimulus_1.csv` ×7,
  `response_2.csv` ×7, `option_1.csv` ×6, `events_1.ndjson` ×5, `input_1.csv` ×2, plus
  `stimulus_2.csv`, `option_2.csv`), in: `guides/1-getting-started.qmd`,
  `guides/3-organize-your-data.qmd`, `guides/4-questionnaire-data.qmd`,
  `guides/7-events-data.qmd`, `concepts/index.qmd`, `spec/timeseries.qmd`,
  `spec/conventions/folder-structure.qmd`. Several generated `spec/trial/*` pages also
  mention attempts. **Coordinate:** land the schema change, then sweep the data-model site
  in one pass.

## 6. Related open items already queued

From `schemas-agent-brief.md` — relevant because they touch the same machinery:

- **Note severity levels were stripped** when trial was seeded into `behaverse/schemas`.
  Notes render as a generic "*Note:*" rather than `.tip` / `.important` / `.warning`
  callouts. Modelling notes as `[{level, text}]` would let §4's warning render as a warning.
  Doing that **before** adding these notes avoids editing them twice.
- **Trial prose still says "subject(s)"** in places; a branch (`chore/trial-agent-terminology`)
  exists in the local clone but is stale-dated and unmerged. Any new notes must use **agent**.
- **Legacy site paths** (`/spec/general/2-dataset-cards.qmd`) still appear in trial field
  descriptions ×4; the data-model rewrites them at build time as a stopgap.

## 7. Definition of done

- [ ] Notes added to the LinkML source (not the generated JSON), using BDM terminology.
- [ ] `python scripts/generate.py` run; `--check` reports no drift; `validate_schemas.py` passes.
- [ ] Version bumped per `VERSIONING.md`, changelog entry written, `versions/` snapshot created.
- [ ] Deployed, and `behaverse.org/schemas/trial/field-definitions.json` serves the new notes.
- [ ] Data-model rebuilt; confirm the notes appear on `spec/trial/1-response.qmd`,
      `2-stimulus.qmd`, and `3-option.qmd`.
- [ ] Report back to the data-model side so the questionnaire guide can drop any wording that
      is now redundant.
