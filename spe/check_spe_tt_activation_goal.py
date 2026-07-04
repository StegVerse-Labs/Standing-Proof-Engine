#!/usr/bin/env python3
"""Check SPE TT integration activation goal file presence and boundaries."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOAL = ROOT / "samples" / "spe_tt_activation_goal.json"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    goal = json.loads(GOAL.read_text(encoding="utf-8"))
    if goal.get("repository") != "StegVerse-Labs/Standing-Proof-Engine":
        fail("repository mismatch")
    if goal.get("activation_state") != "ready_when_all_checks_pass":
        fail("activation state mismatch")

    for path in goal.get("required_docs", []):
        if not (ROOT / path).exists():
            fail(f"missing doc: {path}")
    for path in goal.get("required_scripts", []):
        if not (ROOT / path).exists():
            fail(f"missing script: {path}")

    checks = goal.get("required_checks", [])
    if len(checks) != len(set(checks)) or len(checks) < 8:
        fail("required checks are incomplete or duplicated")

    non_claims = "\n".join(goal.get("non_claims", []))
    for term in ["does not make SPE the TT source of truth", "does not grant commit-time permission", "does not make Commitment Candidates authorizing"]:
        if term not in non_claims:
            fail(f"missing non-claim: {term}")

    print("PASS: SPE TT integration activation goal is ready when workflow checks pass.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
