#!/usr/bin/env python3
"""Validate frozen source-object hash bindings.

This module exists so workflow steps can run:

    python -m tools.refresh_frozen_hashes --check

The current safe behavior is check-only. It delegates binding validation to the
canonical hash-manifest verifier and fails closed if any tracked manifest is
missing, malformed, or stale.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

from spe.verify import FAIL, PASS, Check, render
from spe.verify_hash_manifest import verify_hash_manifest

ROOT = Path(__file__).resolve().parents[1]
HASH_MANIFESTS = ROOT / "samples" / "hash_manifests"


def _manifest_paths() -> list[Path]:
    if not HASH_MANIFESTS.exists():
        return []
    return sorted(HASH_MANIFESTS.glob("*.hashes.json"))


def check_manifests(paths: Iterable[Path] | None = None) -> tuple[str, list[Check]]:
    manifest_paths = list(paths) if paths is not None else _manifest_paths()
    checks: list[Check] = []

    if not manifest_paths:
        return FAIL, [Check("discover_hash_manifests", FAIL, "no frozen hash manifests found")]

    checks.append(Check("discover_hash_manifests", PASS, f"found {len(manifest_paths)} frozen hash manifest(s)"))

    for manifest_path in manifest_paths:
        relative = manifest_path.relative_to(ROOT).as_posix()
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            checks.append(Check(relative, FAIL, "manifest not found"))
            continue
        except json.JSONDecodeError as exc:
            checks.append(Check(relative, FAIL, f"manifest is not valid json: {exc}"))
            continue

        status, manifest_checks = verify_hash_manifest(manifest, ROOT)
        checks.append(Check(relative, status, "frozen hash bindings current" if status == PASS else "frozen hash bindings stale"))
        checks.extend(manifest_checks)

    if any(check.status == FAIL for check in checks):
        return FAIL, checks
    return PASS, checks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate frozen source-object hash bindings.")
    parser.add_argument("--check", action="store_true", help="verify checked-in frozen hash bindings without rewriting files")
    args = parser.parse_args(argv)

    if not args.check:
        parser.error("only --check mode is supported")

    status, checks = check_manifests()
    print(render(status, checks))
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
