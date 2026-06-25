#!/usr/bin/env python3
"""Verify a file's SHA-256 digest."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: python tools/verify_artifact_sha256.py <path> <expected_sha256>", file=sys.stderr)
        return 2

    path = Path(argv[1])
    expected = argv[2].removeprefix("sha256:").strip().lower()

    if not path.exists():
        print(f"FAIL missing file: {path}")
        return 1

    actual = sha256_file(path)
    payload = {
        "path": str(path),
        "expected_sha256": expected,
        "actual_sha256": actual,
        "match": actual == expected,
    }

    import json

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if actual == expected else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
