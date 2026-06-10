#!/usr/bin/env python3
"""Generate dataset/schema.json + dataset/context.jsonld from field-definitions.yaml.

Thin wrapper around the shared generator in repo-root scripts/schema_gen.py, so the
catalog and dataset generators stay byte-identical in behaviour.

Usage:
    python scripts/generate_schema_files.py
    python scripts/generate_schema_files.py --check  # Dry run, show what would change
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from schema_gen import run  # noqa: E402

if __name__ == "__main__":
    run(Path(__file__).resolve().parent.parent, check_mode="--check" in sys.argv)
