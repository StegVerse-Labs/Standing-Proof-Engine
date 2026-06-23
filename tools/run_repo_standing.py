#!/usr/bin/env python3
"""Run automated Standing-Proof-Engine repo-standing checks.

This runner executes the current structural standing checks in one sequence so
CI, downstream agents, and reviewers do not have to remember multiple commands.
It does not prove any open mathematical problem.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class StandingCheck:
    check_id: str
    description: str
    command: tuple[str, ...]
    expected_substring: str | None = None


@dataclass(frozen=True)
class StandingResult:
    check_id: str
    description: str
    command: list[str]
    returncode: int
    passed: bool
    stdout: str
    stderr: str


CHECKS: tuple[StandingCheck, ...] = (
    StandingCheck(
        check_id="research-standing",
        description="Validate research package standing and required artifacts.",
        command=(sys.executable, "tools/validate_research_standing.py"),
        expected_substring="SPE RESEARCH STANDING: PASS",
    ),
    StandingCheck(
        check_id="problem-encodings",
        description="Verify calibration problem encodings against expected-result fixtures.",
        command=(sys.executable, "spe/verify_problem_encodings.py"),
        expected_substring="SPE PROBLEM ENCODINGS: PASS",
    ),
    StandingCheck(
        check_id="problem-encodings-json",
        description="Verify machine-readable problem encoding standing export.",
        command=(sys.executable, "spe/verify_problem_encodings.py", "--json"),
        expected_substring='"spe_result": "PASS"',
    ),
    StandingCheck(
        check_id="automation-addendum",
        description="Check automation addendum metadata and referenced files.",
        command=(sys.executable, "tools/check_automation_addendum.py"),
        expected_substring="SPE AUTOMATION ADDENDUM: PASS",
    ),
    StandingCheck(
        check_id="automation-addendum-json",
        description="Check machine-readable automation addendum metadata output.",
        command=(sys.executable, "tools/check_automation_addendum.py", "--json"),
        expected_substring='"automation_addendum": "PASS"',
    ),
    StandingCheck(
        check_id="problem-encoding-tests",
        description="Run unittest coverage for problem encoding verification.",
        command=(sys.executable, "-m", "unittest", "tests.test_problem_encodings"),
        expected_substring="OK",
    ),
    StandingCheck(
        check_id="formalism-tests",
        description="Run all unittest-discoverable formalism tests.",
        command=(sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"),
        expected_substring="OK",
    ),
)


def run_check(repo_root: Path, check: StandingCheck) -> StandingResult:
    completed = subprocess.run(
        check.command,
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )

    combined_output = completed.stdout + completed.stderr
    has_expected_output = True
    if check.expected_substring is not None:
        has_expected_output = check.expected_substring in combined_output

    return StandingResult(
        check_id=check.check_id,
        description=check.description,
        command=list(check.command),
        returncode=completed.returncode,
        passed=completed.returncode == 0 and has_expected_output,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def run_all(repo_root: Path, checks: Sequence[StandingCheck]) -> list[StandingResult]:
    return [run_check(repo_root, check) for check in checks]


def emit_text(results: Sequence[StandingResult]) -> None:
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {result.check_id} - {result.description}")
        if not result.passed:
            print("  command:", " ".join(result.command))
            if result.stdout:
                print("  stdout:")
                print(result.stdout.rstrip())
            if result.stderr:
                print("  stderr:")
                print(result.stderr.rstrip())

    if all(result.passed for result in results):
        print("SPE REPO STANDING: PASS")
        print("SPE MATHEMATICAL CLAIM STANDING: PARTIAL")
        print("SPE FOLLOW-UP ACTIONS: []")
    else:
        print("SPE REPO STANDING: FAIL")


def emit_json(results: Sequence[StandingResult]) -> None:
    passed = all(result.passed for result in results)
    print(
        json.dumps(
            {
                "spe_result": "PASS" if passed else "FAIL",
                "repo_standing": "PASS" if passed else "FAIL",
                "mathematical_claim_standing": "PARTIAL",
                "follow_up_actions": [],
                "check_count": len(results),
                "passed_count": sum(1 for result in results if result.passed),
                "results": [asdict(result) for result in results],
                "non_claim": "Repo standing checks validate automation structure only; they do not prove any open mathematical problem.",
            },
            indent=2,
            sort_keys=True,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run automated SPE repo-standing checks.")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    results = run_all(repo_root, CHECKS)

    if args.json:
        emit_json(results)
    else:
        emit_text(results)

    return 0 if all(result.passed for result in results) else 1


if __name__ == "__main__":
    sys.exit(main())
