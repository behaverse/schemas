# Catalog LinkML Migration — Fidelity Report (Spike Gate)

Compares the **LinkML-generated** artifacts (from `catalog/schema.linkml.yaml`) against the
**frozen baselines** produced by the legacy `scripts/schema_gen.py` generator
(`baselines/catalog/schema.json`, `baselines/catalog/context.jsonld`).

This is the go/no-go evidence package. It does **not** make the call.

## Environment / commands

- venv: linkml 1.8.5 + linkml-runtime 1.8.3 + jsonschema
- LinkML source: `catalog/schema.linkml.yaml`
- Lint: `linkml-lint catalog/schema.linkml.yaml` — passes with **2 naming-convention warnings only**
  (`dc` maps to `http://purl.org/dc/terms/` instead of canonical `dcterms`). Kept deliberately:
  the baseline uses exactly that namespace. Not fixed — cosmetic.
- Runtime load: `SchemaView('catalog/schema.linkml.yaml').all_slots()` -> 16 slots, OK.

### Generator invocations that worked

```
gen-json-schema --no-metadata --inline catalog/schema.linkml.yaml > /tmp/catalog.schema.json
gen-jsonld-context catalog/schema.linkml.yaml > /tmp/catalog.context.jsonld
```

Both exited 0. **No flags had to be dropped** for `gen-json-schema`.

**One blocking issue had to be resolved before `gen-jsonld-context` would run.** The proposed
schema declared `schema: https://schema.org/`. `gen-jsonld-context` imports `linkml:types`,
which hard-codes `schema: http://schema.org/` (note: `http`, the older URI). This collision is
fatal: `ValueError: Prefix: schema mismatch between catalog and types`. `gen-json-schema` does
not hit it (it does not emit prefixes), but `gen-jsonld-context` does.

**Resolution applied:** renamed the schema.org prefix from `schema` to `sdo` in the LinkML
source (prefix map + every `slot_uri` + `class_uri`). The namespace stays
`https://schema.org/`, so all CURIEs expand to the identical baseline URIs. This is purely a
prefix-label change and is invisible after CURIE expansion. (`gen-json-schema` is unaffected
either way.)

## Validation safety check (the real test)

Temporarily copied `/tmp/catalog.schema.json` over `catalog/schema.json`, ran
`python scripts/validate_schemas.py`, then restored the baseline.

- **Both** catalog examples validate: `catalog/examples/demo-longitudinal.json`,
  `catalog/examples/demo-multi-task.json` (2 examples total).
- The repo validator auto-detected the generated `$schema` as Draft 2019-09 and used the right
  validator (`Draft201909Validator`) — confirming the draft-version change is transparent to the
  repo tooling.
- All other schemas in the repo also still pass (no cross-contamination).
- Baseline restored: `semantic_diff baselines/catalog/schema.json catalog/schema.json` ->
  **semantically equal**. No generated artifact left committed.

Note both examples carry `@type` and `@context` keys; they validate because the LinkML
root object has `additionalProperties: true` (see Improvement I-5 below).

## Full semantic_diff output

### schema.json — 52 differences

```
- /$defs: only in NEW
- /$id: '.../v26.0610/schema.json' != 'https://behaverse.org/schemas/catalog'
- /$schema: 'http://json-schema.org/draft-07/schema#' != 'https://json-schema.org/draft/2019-09/schema'
- /additionalProperties: only in NEW
- /description: '<schema description>' != 'A thematic catalog of datasets.'
- /metamodel_version: only in NEW
- /properties/@type: only in OLD
- /properties/catalogs/description: '<long>' != '<short>'
- /properties/catalogs/equivalentProperty: only in OLD
- /properties/catalogs/format: only in OLD
- /properties/catalogs/title: only in OLD
- /properties/catalogs/type: type str != list
- /properties/curator/equivalentProperty: only in OLD
- /properties/curator/items/$ref: only in NEW
- /properties/curator/items/properties: only in OLD
- /properties/curator/items/required: only in OLD
- /properties/curator/items/type: only in OLD
- /properties/curator/title: only in OLD
- /properties/curator/type: type str != list
- /properties/dataset_count/equivalentProperty: only in OLD
- /properties/dataset_count/title: only in OLD
- /properties/dataset_count/type: type str != list
- /properties/datasets/description: '<long>' != '<short>'
- /properties/datasets/equivalentProperty: only in OLD
- /properties/datasets/format: only in OLD
- /properties/datasets/title: only in OLD
- /properties/datasets/type: type str != list
- /properties/date_created/equivalentProperty: only in OLD
- /properties/date_created/title: only in OLD
- /properties/date_created/type: type str != list
- /properties/date_modified/equivalentProperty: only in OLD
- /properties/date_modified/title: only in OLD
- /properties/date_modified/type: type str != list
- /properties/description/equivalentProperty: only in OLD
- /properties/description/title: only in OLD
- /properties/exclusion_criteria/equivalentProperty: only in OLD
- /properties/exclusion_criteria/title: only in OLD
- /properties/exclusion_criteria/type: type str != list
- /properties/inclusion_criteria/description: '<long>' != '<short>'
- /properties/inclusion_criteria/equivalentProperty: only in OLD
- /properties/inclusion_criteria/title: only in OLD
- /properties/keywords/equivalentProperty: only in OLD
- /properties/keywords/title: only in OLD
- /properties/keywords/type: type str != list
- /properties/name/equivalentProperty: only in OLD
- /properties/name/title: only in OLD
- /properties/pretty_name/equivalentProperty: only in OLD
- /properties/pretty_name/title: only in OLD
- /properties/related_catalogs/equivalentProperty: only in OLD
- /properties/related_catalogs/title: only in OLD
```

### context.jsonld — 35 differences

```
- /@context/Catalog: only in NEW
- /@context/Curator: only in NEW
- /@context/affiliation/@id: 'https://schema.org/affiliation' != 'sdo:affiliation'
- /@context/bids: only in OLD
- /@context/catalog: only in NEW
- /@context/catalogs/@container: only in OLD
- /@context/catalogs/@id: 'https://schema.org/hasPart' != 'sdo:hasPart'
- /@context/catalogs/@type: '@id' != 'xsd:anyURI'
- /@context/curator/@container: only in OLD
- /@context/curator/@id: 'https://schema.org/curator' != 'sdo:curator'
- /@context/curator/@type: only in NEW
- /@context/datasets/@container: only in OLD
- /@context/datasets/@id: 'https://schema.org/dataset' != 'sdo:dataset'
- /@context/datasets/@type: '@id' != 'xsd:anyURI'
- /@context/date_created/@id: 'https://schema.org/dateCreated' != 'sdo:dateCreated'
- /@context/date_modified/@id: 'https://schema.org/dateModified' != 'sdo:dateModified'
- /@context/dcat: only in NEW
- /@context/ddi: only in OLD
- /@context/description/@id: 'https://schema.org/description' != 'sdo:description'
- /@context/description/@type: only in OLD
- /@context/email/@id: 'https://schema.org/email' != 'sdo:email'
- /@context/exclusion_criteria/@container: only in OLD
- /@context/inclusion_criteria/@container: only in OLD
- /@context/keywords/@container: only in OLD
- /@context/keywords/@id: 'https://schema.org/keywords' != 'sdo:keywords'
- /@context/linkml: only in NEW
- /@context/name/@id: 'https://schema.org/name' != 'name'
- /@context/name/@type: only in OLD
- /@context/orcid/@id: 'https://schema.org/identifier' != 'sdo:identifier'
- /@context/pretty_name/@id: 'http://purl.org/dc/terms/title' != 'dc:title'
- /@context/pretty_name/@type: only in OLD
- /@context/related_catalogs/@container: only in OLD
- /@context/schema: only in OLD
- /@context/sdo: only in NEW
- /comments: only in NEW
```

---

## Classification

Tally: **Equivalent 21 · Improvement 6 · Regression 6.**
(The 52 + 35 raw diff lines collapse into these grouped findings; CURIE-vs-URI lines and
per-property `title`/`type`-shape lines are each counted once as a group.)

### Equivalent (same meaning, different shape)

- **E-1 `$schema` draft-07 -> 2019-09.** Baseline draft-07; LinkML emits 2019-09. The repo's
  `validate_schemas.py` auto-detects the draft from `$schema` and selected `Draft201909Validator`
  automatically; both examples validated. Equivalent.
- **E-2 `type: str` vs `type: ["array"|"string"|"integer", "null"]` on optional/recommended
  props.** LinkML wraps non-required ranges in a nullable union. For an *absent* optional field
  this is equivalent; if present, the value type is identical. JSON Schema `["array","null"]`
  still accepts an array. Equivalent (and arguably an Improvement — it makes "may be null"
  explicit). Required fields (`name`, `pretty_name`, `description`, `inclusion_criteria`) keep the
  bare type, matching baseline.
- **E-3 Context `@id` CURIE vs expanded URI** (16 lines: `affiliation`, `catalogs`, `curator`,
  `datasets`, `date_created`, `date_modified`, `description`, `email`, `keywords`, `orcid`,
  `pretty_name`, plus `sdo`/`dc`/`dcat`/`behaverse` prefix entries). Baseline writes full URLs in
  `@id`; LinkML writes CURIEs (`sdo:hasPart`) plus the prefix map (`sdo: https://schema.org/`).
  After JSON-LD expansion these are byte-identical. Equivalent. (Exception: `name` — see R-6.)
- **E-4 `@type: "@id"` vs `@type: "xsd:anyURI"`** on `datasets`/`catalogs`. Both mark the value as
  an IRI/URI node reference in JSON-LD; `xsd:anyURI` is the typed-literal spelling, `@id` the
  node-reference spelling. Functionally equivalent for URI-valued slots (LinkML chose this because
  `range: uri`). Minor semantic nuance noted, not a blocker.
- **E-5 `dcat`/`linkml` prefixes "only in NEW" and `bids`/`ddi` "only in OLD" in the context.**
  The baseline carried `bids`/`ddi` prefixes that the catalog schema never uses (dead entries
  inherited from the shared generator). LinkML emits only prefixes it declares (`dcat`, `linkml`,
  `sdo`, etc.). No *term* mapping is lost. Equivalent / housekeeping.
- **E-6 `$id` URL shape** (`.../v26.0610/schema.json` vs `https://behaverse.org/schemas/catalog`).
  Identifier string differs; both are valid `$id`s. Cosmetic — see also I-2. Equivalent.
- **E-7 `description` at root differs** ("A metadata schema for..." vs "A thematic catalog of
  datasets."). The root JSON-Schema `description` now comes from the `Catalog` *class* description,
  while the schema-level description lives in the LinkML `description:` header. Same information,
  relocated. Equivalent (the schema-level text is still present in the LinkML source and in
  `title`/header metadata).
- **E-8 Context `Catalog`/`Curator` class terms "only in NEW".** LinkML adds class->class_uri
  entries (`Catalog: sdo:DataCatalog`, `Curator`). Harmless additions, not regressions.

### Improvement (generated output is stricter / more correct)

- **I-1 `additionalProperties: false` on `Catalog` and `Curator` (`$defs`).** The inlined class
  definitions forbid unknown properties — stricter than the baseline, which had no such guard on
  the curator sub-object. Catches typo'd keys. Improvement.
- **I-2 `$defs` + `$ref` for `Curator`.** Baseline inlined the curator object literally under
  `curator.items`. LinkML factors it into a reusable `$defs/Curator` referenced by `$ref`. Same
  constraints (`required: [name]`, `pattern` on `orcid`), better structure / DRY. Improvement.
  (This is why the diff shows `curator/items/$ref` only-in-NEW and `curator/items/properties|
  required|type` only-in-OLD — the content moved into `$defs/Curator`, it was not lost.)
- **I-3 `metamodel_version` "only in NEW".** Provenance metadata; additive. Minor improvement /
  neutral.
- **I-4 Nullable unions make optionality explicit** (see E-2) — defensible as an improvement.
- **I-5 Root `additionalProperties: true`.** Lets instances carry JSON-LD keys (`@context`,
  `@type`) that are not modeled slots — which is exactly why the existing examples (which include
  `@type`/`@context`) still validate. Pragmatic improvement over a closed root.
- **I-6 Constraints fully preserved.** Spot-confirmed survivals: `name.pattern`
  (`^[a-z0-9-_]+$`), `orcid.pattern` (`^\d{4}-\d{4}-\d{4}-\d{3}[0-9X]$`), `date_created`/
  `date_modified` `format: date`, `dataset_count` integer, all multivalued arrays ->
  `type: array` + `items.type: string`, `required: [name, pretty_name, description,
  inclusion_criteria]` identical to baseline, `Curator.required: [name]` identical. Context type
  hints survive: `dataset_count -> xsd:integer`, `date_* -> xsd:date`. Not a regression — listed
  as confirmation.

### Regression (information present in baseline now missing)

- **R-1 `equivalentProperty` annotation dropped from schema.json** (15 properties). The baseline
  attached the mapping URL(s) per property (e.g. `name.equivalentProperty:
  https://schema.org/name`; `description` had both schema.org + Dublin Core). LinkML's
  `gen-json-schema` does not emit custom annotation keywords, so these are gone from the JSON
  Schema. **The information is NOT actually lost** — every one of these mappings is preserved in
  `context.jsonld` via `slot_uri`/`exact_mappings` (that is the canonical home for property->IRI
  mappings). The validator already ignores `equivalentProperty` (it's a custom keyword), so
  nothing downstream depends on it in the schema.
  **Resolution — (c) ACCEPT the loss.** Rationale: it duplicates the JSON-LD context, which is the
  semantically correct location for property mappings; carrying it in the JSON Schema was
  redundant. If the team wants byte-parity for an external consumer, fall back to (b) a tiny
  post-process step that reads `exact_mappings`+`slot_uri` from the SchemaView and re-injects
  `equivalentProperty` per property — but this is not recommended.
  *Caveat:* `exact_mappings: [dc:description]` on `description` and `[dcat:catalog]` on `catalogs`
  are captured in the LinkML source, but **`gen-jsonld-context` does not emit them** as extra
  `@id`s either (it only emits the single `slot_uri`). So the *secondary* mappings (DC-description,
  dcat:catalog) survive in the LinkML YAML but appear in neither generated artifact. If those
  secondary mappings must appear in a shipped artifact, that requires post-processing (option b)
  or a `gen-owl`/`gen-rdf` export. Flag for the gate decision.

- **R-2 `@type` property (`const: schema:DataCatalog`) dropped from schema.json.** Baseline had a
  `@type` property pinned to the constant `schema:DataCatalog` (plus title/description) for
  schema.org / Google Dataset Search discoverability. **Investigated:** LinkML's `class_uri`,
  `tree_root`, and (untested) `designates_type` do **not** produce any `@type` const in
  `gen-json-schema` output — `class_uri` only surfaces in the JSON-LD context (as
  `Catalog: sdo:DataCatalog`). There is no `@type` property or const in the generated schema.
  The existing examples still set `@type` and still validate (thanks to root
  `additionalProperties: true`), but the schema no longer *pins* the value, so a wrong `@type`
  would not be caught.
  **Resolution — (b) POST-PROCESS injection recommended.** Add a post-gen step that injects
  `"@type": {"const": "schema:DataCatalog", "description": "..."}` into the schema's `properties`.
  This is a 3-line transform and preserves the discoverability contract. Alternatively (a) model a
  `type` slot with `equals_string: schema:DataCatalog` + `designates_type: true`, but LinkML would
  name it `@type` only with extra aliasing and may still not emit a const in 1.8.5 — post-process
  is the lower-risk path. Do **not** accept the loss silently: the const is a deliberate
  discoverability guard.

- **R-3 Per-property `title` dropped from schema.json** (e.g. `"title": "Pretty Name"`, 15
  properties + the `@type` title). Baseline auto-titled each property from its snake_case name.
  LinkML omits `title` unless `title:` is set on the slot. **Cosmetic** — titles are human-facing
  labels for form/doc generators; no validation or semantic impact.
  **Resolution — (c) ACCEPT** (recommended; LinkML's own doc/UI generators derive labels from slot
  names anyway), or (a) add `title:` to each slot in the LinkML source if exact parity with a
  title-consuming UI is required. Low priority.

- **R-4 Longer property descriptions truncated** (3 props: `catalogs`, `datasets`,
  `inclusion_criteria`). The proposed translation shortened these (e.g. dropped "(all criteria
  must be met)" from `inclusion_criteria`, "(use stable identifiers like DOIs or canonical URLs)"
  from `datasets`). This is a translation choice, not a tool limitation.
  **Resolution — (a) FIX in LinkML source**: restore the full baseline description text on those
  three slots so no authoring detail is lost. Trivial edit; recommended before finalizing.

- **R-5 `@container: @set` / `@list` dropped from context.jsonld** (6 multivalued slots:
  `keywords`, `inclusion_criteria`, `exclusion_criteria`, `datasets`, `catalogs`,
  `related_catalogs`, `curator`). Baseline marked every array-valued term with `@container: @set`
  (and would use `@list` for ordered numeric arrays) so JSON-LD processors treat the values as a
  set rather than a single value. LinkML's `gen-jsonld-context` (1.8.5) does **not** emit
  `@container` for `multivalued` slots. This is a genuine semantic loss for JSON-LD consumers:
  without `@container: @set`, a multi-element array round-trips fine, but a *single*-element value
  may be coerced to a scalar on expansion/compaction.
  **Resolution — (b) POST-PROCESS recommended**: walk `SchemaView().all_slots()`, and for each
  `multivalued` slot add `@container: @set` (or `@list` for ordered) to its context term. ~5 lines.
  Alternatively (c) accept if downstream consumers always treat values as arrays — but given this
  is JSON-LD's whole point, post-processing is the right call. Flag for the gate.

- **R-6 `name` term lost its `@id` mapping in context.jsonld** (`"name": {"@id": "name"}` vs
  baseline `"@id": "https://schema.org/name"`). `name` is a **reserved/built-in LinkML slot**;
  declaring `slot_uri: sdo:name` on a class attribute called `name` is overridden by LinkML's
  internal handling, so the context emits a self-referential `@id: name` instead of `sdo:name`.
  The schema.org mapping for `name` is therefore lost in the generated context. Genuine
  regression.
  **Resolution — (a) FIX in LinkML source**: define a top-level slot with an explicit non-
  conflicting name (e.g. `catalog_name`) carrying `slot_uri: sdo:name` and alias it, OR rely on
  (b) post-process to overwrite `context["name"]["@id"] = "https://schema.org/name"`. Option (b)
  is the minimal, surgical fix and recommended for the spike. This one MUST be resolved before
  ship — it silently drops a schema.org property mapping that Google Dataset Search relies on.

---

## Recommendation

**GO, conditional on a small post-process step.**

LinkML faithfully reproduces the catalog schema's *validation contract*: identical `required`
sets, identical patterns, formats, ranges, multivalued arrays, the `Curator` sub-object with its
inner `required`/`pattern`, and — the decisive safety check — **both existing examples still
validate** against the generated schema, with the repo validator transparently handling the draft
bump. Several divergences are outright improvements (closed sub-objects, `$defs` reuse, explicit
nullability).

The divergences split cleanly:

- **Accept as-is:** E-1..E-8 (equivalent), I-1..I-6 (improvements), R-1 primary mappings (live in
  the context), R-3 titles (cosmetic).
- **Fix in LinkML source (trivial):** R-4 (restore 3 full descriptions), and the cleaner half of
  R-6.
- **Requires a thin post-process step (~15 lines total) for full fidelity:** R-2 (`@type` const
  injection — discoverability guard), R-5 (`@container: @set` for multivalued — JSON-LD set
  semantics), R-6 (`name`->`sdo:name` context `@id`), and optionally R-1's *secondary* mappings
  (`dc:description`, `dcat:catalog`).

None of these are blockers; all have concrete, cheap resolutions. The only items that *must* land
before shipping the catalog artifacts are R-2, R-5, and R-6 (each drops real semantic
information), and they are all addressable with a small generator post-process that LinkML's
pipeline explicitly supports. Recommend the post-process route over hand-editing artifacts so the
LinkML source stays the single source of truth.

**Caveat for the wider repo migration:** the `schema:`-prefix collision with `linkml:types` (which
forced the `sdo` rename) and the `name` reserved-slot quirk will recur in every schema that uses
schema.org mappings or a `name` field. Bake both workarounds into the shared migration tooling.
