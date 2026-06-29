#!/usr/bin/env python3
"""Verify that a file's SHA-256 matches an expected pinned digest.

This tool exists so a workflow step can pin the byte-level identity of a
generated artifact (for example the expected-corpus inventory) and detect
drift:

    python tools/verify_artifact_sha256.py <path> <expected_sha256>

It prints a JSON verdict to stdout and exits 0 when the digest matches, 1
when it does not, and 2 on a usage or I/O error. Callers that only want a
non-blocking diagnostic guard the invocation with ``|| true`` so the verdict
is recorded without failing the job; callers that want the pin enforced drop
the guard.

The digest is computed over the raw on-disk bytes of the file, not a
canonical re-serialization, so the pinned value tracks exactly what was
written and uploaded.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def compute_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(path: Path, expected: str) -> tuple[bool, dict]:
    actual = compute_sha256(path)
    matches = actual == expected.strip().lower()
    verdict = {
        "artifact": path.as_posix(),
        "expected_sha256": expected.strip().lower(),
        "actual_sha256": actual,
        "matches": matches,
        "status": "PASS" if matches else "FAIL",
    }
    return matches, verdict


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Verify a file's SHA-256 against an expected pinned digest.",
    )
    parser.add_argument("path", help="path to the artifact whose bytes are hashed")
    parser.add_argument("expected_sha256", help="expected lowercase hex SHA-256 digest")
    args = parser.parse_args(argv[1:])

    path = Path(args.path)
    if not path.is_file():
        print(
            json.dumps(
                {
                    "artifact": path.as_posix(),
                    "expected_sha256": args.expected_sha256.strip().lower(),
                    "actual_sha256": None,
                    "matches": False,
                    "status": "FAIL",
                    "error": "artifact not found",
                },
                indent=2,
            )
        )
        return 2

    matches, verdict = verify(path, args.expected_sha256)
    print(json.dumps(verdict, indent=2))
    return 0 if matches else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
