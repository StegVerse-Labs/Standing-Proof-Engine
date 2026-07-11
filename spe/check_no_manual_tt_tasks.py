#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "spe-tt-binding.yml"
HANDOFF = ROOT / "docs" / "SPE_MIRROR_HANDOFF.md"
RUNNER = ROOT / "spe" / "run_tt_integration_checks.py"

CANONICAL_RUNNER_COMMAND = "python -m spe.run_tt_integration_checks"
LEGACY_RUNNER_COMMAND = "python spe/run_tt_integration_checks.py"

REQUIRED_WORKFLOW_TERMS = [
    "schedule:",
    "workflow_dispatch:",
    CANONICAL_RUNNER_COMMAND,
]

REQUIRED_HANDOFF_TERMS = [
    CANONICAL_RUNNER_COMMAND,
    "Workflow paths displayed here without a leading period",
    "This file is the current handoff source of truth",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_file(path: Path) -> str:
    if not path.exists():
        fail(f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    workflow = require_file(WORKFLOW)
    handoff = require_file(HANDOFF)
    require_file(RUNNER)

    for term in REQUIRED_WORKFLOW_TERMS:
        if term not in workflow:
            fail(f"workflow missing term: {term}")

    for term in REQUIRED_HANDOFF_TERMS:
        if term not in handoff:
            fail(f"handoff missing term: {term}")

    if LEGACY_RUNNER_COMMAND in workflow:
        fail(f"workflow contains legacy runner invocation: {LEGACY_RUNNER_COMMAND}")

    print(
        "PASS: SPE TT integration has scheduled workflow coverage, "
        "canonical module execution, and a current handoff."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
