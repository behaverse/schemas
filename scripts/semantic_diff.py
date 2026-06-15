#!/usr/bin/env python3
"""Deep semantic comparison of two JSON files, order-insensitive for objects.

Usage: python scripts/semantic_diff.py OLD.json NEW.json
Exit 0 if semantically equal; exit 1 and print the first differences otherwise.
Used to verify a migrated artifact loses no information vs its frozen baseline.
"""
from __future__ import annotations
import json, sys
from pathlib import Path


def canon(x):
    if isinstance(x, dict):
        return {k: canon(v) for k, v in sorted(x.items())}
    if isinstance(x, list):
        return [canon(v) for v in x]
    return x


def diff(a, b, path=""):
    out = []
    if type(a) is not type(b):
        out.append(f"{path or '<root>'}: type {type(a).__name__} != {type(b).__name__}")
        return out
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append(f"{path}/{k}: only in NEW")
            elif k not in b:
                out.append(f"{path}/{k}: only in OLD")
            else:
                out += diff(a[k], b[k], f"{path}/{k}")
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append(f"{path}: list length {len(a)} != {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            out += diff(x, y, f"{path}[{i}]")
    elif a != b:
        out.append(f"{path}: {a!r} != {b!r}")
    return out


def main() -> int:
    old, new = (json.loads(Path(p).read_text()) for p in sys.argv[1:3])
    d = diff(canon(old), canon(new))
    if d:
        print(f"✗ {len(d)} difference(s):")
        for line in d[:50]:
            print("  -", line)
        return 1
    print("✓ semantically equal")
    return 0


if __name__ == "__main__":
    sys.exit(main())
