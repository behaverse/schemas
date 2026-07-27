# Design: self-scoping data files, the run log, and the parameter grain split

**Status:** ACCEPTED and implemented in trial v26.0727 (+ timeseries v26.0727, vocabulary v26.0727).
Supersedes `_archive/trial-PROPOSAL_task_vs_trial_parameters.md`. Reviewed and annotated by Pedro
2026-07-27; all resolutions folded in below (see §8).
**Scope:** one breaking `trial` release. Rulings incorporated: data files must be self-scoping
(folders are a *view*), main files stay human-readable without joins, detail tables join on
`(runtime_id, response_id)`.

---

## 1. The problem, in one paragraph

Every trial table today depends on its folder for identity: `response_id` is unique only
*within a file*, and `Stimulus`/`Option`/`Input`/`Subtrial` scope by `response_id`/`trial_index`
alone, while the `*Component` tables carry no scoping at all. Concatenating all `stimulus.csv`
files in a dataset therefore silently mixes agents. Separately, "which attempt was this, and did
it finish?" is unanswerable from the trial tables: the attempt lives only in a filename suffix,
and an activity that was started and abandoned before the first trial completed produces **zero
rows** — its existence is unrepresentable. Both problems have one cause: **the run itself is not
a first-class entity.**

## 2. The entity: an activity run

BDM already has this concept, three times over, and never defined it:

- The event schema's `bdm:RuntimeInstance` — "one specific runtime execution of an Activity
  (**distinguishes restarts**)" — with a lifecycle (`initialized` → `started` → `paused`/`resumed`
  → `completed` | `abandoned` → `submitted`) and a `bdm:runtime_id` context key.
- `studyflow.csv`, which ships in every dataset's `data/agent_{x}/` folder and lists each agent's
  attempts — **but has no schema anywhere**. The `studyflow` *family* models the BPMN plan
  (Study/Activity/gateways), not execution.
- The trial schema's dangling note "See `Studyflow` table for more details"
  ([trial/schema.linkml.yaml:180](trial/schema.linkml.yaml#L180)), pointing at a table that
  does not exist.

**Proposal: schematize it once, as the `Studyflow` table in the `trial` family, keyed by
`runtime_id`.** Keeping the name `Studyflow` matches the file that already ships and resolves the
dangling reference for free; keeping the id `runtime_id` makes the trial and event layers join
directly. (Alternative names — `RuntimeInstance`, `Run`, `ActivityRun` — are more literal but
orphan the existing filename; see §8 open questions.)




### 2.1 `Studyflow` table

One row per activity run. File: `data/agent_{x}/studyflow.csv` (unchanged location).

| column | req | meaning |
|---|---|---|
| `runtime_id` | ✔ | **PK**, unique dataset-wide (UUID recommended). Equals the event layer's `bdm:runtime_id`. |
| `agent_id` | ✔ | who |
| `session_index` | ✔ | 1-based session within the agent |
| `session_uuid` | – | global session identity (matches `Response.session_uuid`) |
| `activity_index` | ✔ | 1-based order of the activity within the session |
| `instrument_id` | ✔ | which instrument/task ran |
| `timeline_id` | – | the instrument's parameterization |
| `attempt` | ✔ | 1-based ordinal of this run of this activity within the session — **the `_<attempt>` filename suffix, promoted to data** |
| `instrument_repetition` | – | existing study-wide count of prior completions (distinct from `attempt`; see §8) |
| `timeline_repetition` | – | ditto for the timeline |

-> it's study-wide but specific to this agent. This does not count how many times a instrument was completed across all participants within a study. attempt should clarify that this allows to identify sessions that were interrupted and possibly restarted multiple times.  

| `status` | ✔ | `initialized` · `in_progress` · `completed` · `abandoned` — a real LinkML enum |
| `abandon_reason` | – | free text; mirrors the event layer's `bdm:abandon_reason` |
| `started_datetime` | – | when first content was shown (event `bdm:started`) |
| `ended_datetime` | – | when the run reached its terminal state |
| `anchor_datetime` | – | RFC 9557 datetime at `engine_seconds` = 0 for this run (see §8 — this is per-run, not per-session) |

-> not sure if "start_datetime" or "started_datetime" would be most consistent with the naming convention adopted so far (same for "end_datatime"). What do you recommend?

`status` is **derived from the lifecycle events** where an event stream exists, and authored
directly otherwise. It is the authoritative record of completion.

### 2.2 What this makes possible

```
last complete attempt per agent per task =
  Studyflow  →  filter status == 'completed'
             →  max(attempt) per (agent_id, instrument_id)
             →  join Response on runtime_id
```

No attempt-counting across trial rows, no filename parsing, and abandoned runs that produced no
trials remain visible and auditable.

## 3. Two-tier scoping

Both rulings — self-scoping data, human-readable main files — are satisfied by a rule, applied
consistently:

**Tier A — standalone-readable.** Files a human opens directly to understand a run. They carry
the full human-meaningful scope even where it is technically redundant:
`Studyflow`, `Response`, `TaskParameter`.

**Tier B — join-oriented.** Row-level detail with large row counts, always consumed by joining:
`Stimulus`, `Option`, `Input`, `Subtrial`, `StimulusComponent`, `OptionComponent`,
`TrialParameter`. They carry `runtime_id` plus their existing local key, and nothing more.

### 3.1 Per-table changes

| table | tier | change |
|---|---|---|
| `Studyflow` | A | **new** (§2.1) |
| `Response` | A | **+ `runtime_id`** (required), **+ `attempt`** (required), **+ `status`** (optional, denormalized from `Studyflow`). Keeps every existing scoping column. |
| `Stimulus`, `Option`, `Input`, `Subtrial` | B | **+ `runtime_id`** (required). Keep `response_id` / `trial_index`. |
| `StimulusComponent`, `OptionComponent` | B | **+ `runtime_id`** (required). Their `stimulus_id` / `option_id` are file-local and collide on concatenation exactly like `response_id`. |
| `Instrument` | — | unchanged: it describes instruments, not runs. |
| `TrialParameter` | B | renamed from `TaskParameter` (§4) |
| `TaskParameter` | A | **new**, activity-run grained (§4) |

`Response.status` is a deliberate denormalization so "drop trials from abandoned runs" needs no
join. Rule: **`Studyflow` is authoritative**; `Response.status` is a copy, and any disagreement is
a dataset bug.

### 3.2 The join key

`response_id`, `trial_index`, `stimulus_id`, and `option_id` stay **file-local** (short, readable,
unchanged). Dataset-wide identity is the pair:

```
(runtime_id, response_id)      -- and (runtime_id, stimulus_id), etc.
```

Every affected `range_description` states this explicitly, replacing today's "of the same
agent/session/activity/attempt" (which encodes the folder dependency this design removes).

## 4. The parameter grain split

Two grains, two tables, both keeping the leakage doctrine (legitimate for simulation and
recovery, illegitimate as predictors of the responses they generated):

**`TrialParameter`** (tier B) — renamed from the shipped v26.0721 `TaskParameter`; values that
vary trial to trial (a two-step's drifting reward probabilities). Columns: `runtime_id` ✔,
`response_id` ✔, `trial_index`, `subtrial_index` (new — for parameters realized at a specific
stage), `task_index`, `parameter` ✔, `index_1`, `index_2`, `value` ✔.
Natural key: `(runtime_id, response_id, subtrial_index, task_index, parameter, index_1, index_2)`.

-> what do `index_1`, `index_2` refer to?


**`TaskParameter`** (tier A) — new; values constant across one activity run but varying between
runs/agents (a per-participant reward mapping, a per-group volatility level). Columns:
`runtime_id` ✔, `agent_id` ✔, `session_index` ✔, `instrument_id` ✔ (**names the activity, per the
ruling**), `task_index`, `parameter` ✔, `index_1`, `index_2`, `value` ✔.
Natural key: `(runtime_id, task_index, parameter, index_1, index_2)`.

Files live in the activity folder beside the trial tables:
`…/<activity>/task_parameter_<attempt>.csv` and `…/<activity>/trial_parameter_<attempt>.csv`.
No `activity_index` column is needed on either — `runtime_id` resolves it, and `instrument_id`
names it. Joining the two reconstructs the full generative state in effect on any trial.

-> I think we should skip the attempt suffixing (and splitting of files) and leave that to the data analyst. This makes the resulting tree structure look cleaner.


**Explicitly out of scope:** instrument-level generative *laws* (drift hyperparameters, fixed
constants), which belong to the task-levels design (`_archive/bdm_extensions.md` §8).

## 5. What this does *not* change

`Response` keeps every column it has today — this design only adds. No renames beyond
`TaskParameter` → `TrialParameter`. The folder layout is unchanged; it simply stops being
load-bearing, becoming what it should be: an export view of the catalog, reproducible by
partitioning `Studyflow` on `agent_id`/`session_index`/`instrument_id`/`attempt`.

## 6. Release plan

One breaking `trial` release (`v26.MMDD`), in this order:

1. `Studyflow` table + `RunStatusEnum` in `trial/schema.linkml.yaml`.
2. `runtime_id` across the eight existing tables; `Response` gains `attempt` + `status`.
3. `TaskParameter` → `TrialParameter` (+ `response_id`, `subtrial_index`); new `TaskParameter`.
4. Update every affected `range_description` to the composite-key wording (§3.2).
5. Regenerate, snapshot `versions/v26.MMDD/`, CHANGELOG with a `### Breaking` section, refresh
   the trial README table list and field counts, bump root README.

No deprecation window: the schemas have no external consumers yet, so prior versions are
documentation, not compatibility obligations.

## 7. Downstream consequences

- **`bdm-data-model-agent-prompt.md` needs two additions** once this ships: document
  `studyflow.csv`'s columns in the dataset-structure spec, and **correct the "Hive/Arrow-style
  partitioning" framing** — under this design partition keys are *duplicated* into the data, not
  delegated to the path.
- **The event layer gains a real join:** `bdm:runtime_id` in event context ↔ `Studyflow.runtime_id`.
  Worth stating in the event README.
- **`agents.csv` remains unspecified** — the other dataset-level file with no schema, and the
  target of the trial schema's second dangling reference ("See `Agent` table"). Natural follow-up.

-> OK

## 8. Resolutions (2026-07-27 review)

1. **Table name → `Studyflow`.** The class description states plainly that it is the realized run
   log (`studyflow.csv`), distinct from the study-level plan (the BPMN diagram in the `studyflow`
   family, authored as `.studyflow`/`.xml`). A reciprocal note was added to the `studyflow`
   family README so the two can't be confused.
2. **Keep both `attempt` and `instrument_repetition`.** `instrument_repetition`'s description now
   says explicitly that it counts *this agent's own* prior completions across sessions — never
   completions across participants — while `attempt` counts runs within the session and is what
   identifies an interrupted-and-restarted session.
3. **`anchor_datetime` is per run.** It lives on `Studyflow`, and the vocabulary definition was
   amended from "once per session" to "once per runtime instance" (vocabulary v26.0727).
4. **`Response.status` included**, optional, denormalized from `Studyflow`. Noted that it is only
   final once a run has ended — which is what the `initialized`/`in_progress` values are for; in a
   published dataset every run has a terminal state.
5. **`Studyflow` lives in the `trial` family.**
6. **Datetime naming → `start_datetime` / `end_datetime`.** `trial_start_datetime` is the family's
   only precedent and uses the noun form; the entity prefix is dropped because on `Studyflow` the
   row *is* the run (as `Stimulus.onset` drops its prefix inside its own table).
7. **No attempt suffix on filenames.** Files are `response.csv`, `stimulus.csv`,
   `task_parameter.csv` — several runs share one file, distinguished by `runtime_id`/`attempt`.
   Boundary: this works for the tidy tables and the events NDJSON (whose lines carry
   `bdm:runtime_id`), but **not** for timeseries payloads — a binary recording cannot be
   concatenated and two files cannot share a name, so those keep a per-run filename. The
   timeseries sidecar therefore gained `runtime_id` (v26.0727).
8. **Parameter payload redesigned.** `index_1`/`index_2`/`value` proved too weak: the value was an
   untyped `any`, the arity was capped at two, and nothing recorded what an index *meant*. Replaced
   by `parameter_dimensions` (axis names, `state;action`), `parameter_index` (coordinates, `1;2`),
   `value_numeric`, and `value_description` — following BDM's existing semicolon-list convention
   (`stimulus_index`) and its `*_numeric`/`*_description` pairing (`response`, `outcome`).
   Vector-valued parameters decompose into one row per element, which is the tidy form.

## 9. Follow-ups this created

- Apply the self-scoping rule to the remaining tables' local keys if pooling ever needs more than
  the `(runtime_id, local_id)` pair (tracked in `OPEN-ISSUES.md` §2).
- `agents.csv` is still unspecified — the last dataset-level file without a schema, and the target
  of the trial schema's remaining dangling reference ("See `Agent` table").
- The data-model site items in `OPEN-ISSUES.md` §5 now include documenting `studyflow.csv` and
  correcting the "Hive/Arrow-style partitioning" framing.
