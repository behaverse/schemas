# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""Generate the published artifact for the vocabulary from terms.yaml.

The vocabulary is a terminology resource (SKOS concept schemes + concepts), not a JSON
Schema, so it emits a single artifact from the one source of truth:

  - terms.jsonld — a SKOS JSON-LD serialization. Consumed by behaverse/data-model (the
                   BDM glossary page merges it with terms harvested from each schema's
                   field-definitions.json) and readable as plain JSON by any consumer.

Concepts/schemes with `status: internal` are carried through unchanged — filtering for
display is the consumer's choice (the BDM glossary hides them).

Usage:
    uv run scripts/generate.py
    uv run scripts/generate.py --check   # dry run; exit 1 if the generated file is stale
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml  # type: ignore

VOCAB_DIR = Path(__file__).parent.parent

CONTEXT = {
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "bdm": "https://behaverse.org/schemas/vocabulary#",
    "label": "skos:prefLabel",
    "definition": "skos:definition",
    "description": "skos:definition",
    "notes": "skos:note",
    "scheme": {"@id": "skos:inScheme", "@type": "@id"},
    "data_type": "bdm:dataType",
    "range": "bdm:range",
    "status": "bdm:status",
    # NOT two aliases of @graph: aliasing two terms to the same keyword is invalid
    # JSON-LD ("colliding keywords"; pyld and other 1.1 processors reject it). Distinct
    # containment properties keep the JSON shape identical for consumers and keep every
    # scheme/concept node (with its @id/@type/SKOS properties) in the expanded graph.
    "schemes": {"@id": "bdm:schemes", "@container": "@set"},
    "concepts": {"@id": "bdm:concepts", "@container": "@set"},
}


def build(src: dict) -> dict:
    meta = src["vocabulary_metadata"]
    base = meta["namespace"].rstrip("/")

    def scheme_node(s: dict) -> dict:
        return {"@id": f"{base}/{s['id']}", "@type": "skos:ConceptScheme",
                **{k: v for k, v in s.items() if k != "id"}}

    def concept_node(c: dict) -> dict:
        node = {"@id": f"{base}/{c['scheme']}/{c['id']}", "@type": "skos:Concept",
                **{k: v for k, v in c.items() if k not in ("id", "scheme")}}
        node["scheme"] = f"{base}/{c['scheme']}"
        return node

    return {
        "@context": CONTEXT,
        "@id": base,
        "@type": "skos:ConceptScheme",
        "name": meta["name"],
        "version": meta["version"],
        "description": meta["description"],
        "schemes": [scheme_node(s) for s in src["schemes"]],
        "concepts": [concept_node(c) for c in src["concepts"]],
    }


def main() -> int:
    check = "--check" in sys.argv
    src = yaml.safe_load((VOCAB_DIR / "terms.yaml").read_text())
    out_path = VOCAB_DIR / "terms.jsonld"
    rendered = json.dumps(build(src), indent=2, ensure_ascii=False) + "\n"

    if check:
        if not out_path.exists() or out_path.read_text() != rendered:
            print(f"STALE: {out_path.name} is out of sync with terms.yaml — run scripts/generate.py")
            return 1
        print(f"{out_path.name} is in sync with terms.yaml")
        return 0

    out_path.write_text(rendered)
    n_schemes, n_concepts = len(src["schemes"]), len(src["concepts"])
    print(f"wrote {out_path.name} ({n_schemes} schemes, {n_concepts} concepts)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
