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


def spe_module(module: str, *args: str) -> tuple[str, ...]:
    return (sys.executable, "-m", f"spe.{module}", *args)


CHECKS: tuple[StandingCheck, ...] = (
    StandingCheck("research-standing", "Validate research package standing and required artifacts.", (sys.executable, "tools/validate_research_standing.py"), "SPE RESEARCH STANDING: PASS"),
    StandingCheck("problem-encodings", "Verify calibration problem encodings against expected-result fixtures.", spe_module("verify_problem_encodings"), "SPE PROBLEM ENCODINGS: PASS"),
    StandingCheck("problem-encodings-json", "Verify machine-readable problem encoding standing export.", spe_module("verify_problem_encodings", "--json"), '"spe_result": "PASS"'),
    StandingCheck("automation-addendum", "Check automation addendum metadata and referenced files.", (sys.executable, "tools/check_automation_addendum.py"), "SPE AUTOMATION ADDENDUM: PASS"),
    StandingCheck("automation-addendum-json", "Check machine-readable automation addendum metadata output.", (sys.executable, "tools/check_automation_addendum.py", "--json"), '"automation_addendum": "PASS"'),
    StandingCheck("destination-event-installed", "Verify installed destination event binding.", spe_module("verify_destination_event", "samples/destination_event_001.json"), "SPE RESULT: PASS"),
    StandingCheck("destination-event-deferred", "Verify deferred destination event binding.", spe_module("verify_destination_event", "samples/destination_event_deferred_001.json"), "SPE RESULT: PASS"),
    StandingCheck("event-replay-installed", "Verify installed event replay binding.", spe_module("verify_event_replay", "samples/event_replay_001.json"), "SPE RESULT: PASS"),
    StandingCheck("event-replay-deferred", "Verify deferred event replay binding.", spe_module("verify_event_replay", "samples/event_replay_deferred_001.json"), "SPE RESULT: PASS"),
    StandingCheck("source-bound-sample", "Verify source-hash-bound stale-state sample.", spe_module("verify_source_bound", "samples/source_hash_bound_stale_state_001.json"), "SPE RESULT: PASS"),
    StandingCheck("source-bound-json", "Verify source-hash-bound JSON export.", spe_module("verify_source_bound", "--json", "samples/source_hash_bound_stale_state_001.json"), '"spe_result": "PASS"'),
    StandingCheck("external-source-refs-sample", "Verify external source reference stale-state sample.", spe_module("verify_external_refs", "samples/external_source_ref_stale_state_001.json"), "SPE RESULT: PASS"),
    StandingCheck("external-source-refs-json", "Verify external source reference JSON export.", spe_module("verify_external_refs", "--json", "samples/external_source_ref_stale_state_001.json"), '"spe_result": "PASS"'),
    StandingCheck("destination-hash-import", "Verify destination-generated hash import binding.", spe_module("verify_hash_import", "samples/destination_generated_event_hash_001.json"), "SPE RESULT: PASS"),
    StandingCheck("destination-receipt-chain", "Verify destination-generated receipt chain binding.", spe_module("verify_receipt_chain", "samples/destination_receipt_chain_001.json"), "SPE RESULT: PASS"),
    StandingCheck("expected-corpus", "Verify every expected-result fixture in the expected corpus.", spe_module("verify_expected_corpus"), "SPE RESULT: PASS"),
    StandingCheck("release-readiness", "Generate and verify local SPE release readiness artifacts.", (sys.executable, "tools/write_release_readiness.py"), "SPE RELEASE READINESS: READY"),
    StandingCheck("problem-encoding-tests", "Run unittest coverage for problem encoding verification.", (sys.executable, "-m", "unittest", "tests.test_problem_encodings"), "OK"),
    StandingCheck("automation-addendum-metadata-tests", "Run unittest coverage for automation addendum metadata.", (sys.executable, "-m", "unittest", "tests.test_automation_addendum_metadata"), "OK"),
    StandingCheck("repo-standing-handoff-metadata-tests", "Run unittest coverage for machine-readable repo standing handoff metadata.", (sys.executable, "-m", "unittest", "tests.test_repo_standing_handoff_metadata"), "OK"),
    StandingCheck("release-readiness-runner-doc-tests", "Run unittest coverage for release-readiness runner documentation.", (sys.executable, "-m", "unittest", "tests.test_release_readiness_runner_doc"), "OK"),
    StandingCheck("confirmation-hash-binding-tests", "Run unittest coverage for master-records confirmation hash binding.", (sys.executable, "-m", "unittest", "tests.test_confirmation_hash_binding"), "OK"),
    StandingCheck("destination-event-hash-binding-tests", "Run unittest coverage for destination event confirmation hash binding.", (sys.executable, "-m", "unittest", "tests.test_destination_event_hash_binding"), "OK"),
    StandingCheck("event-replay-hash-binding-tests", "Run unittest coverage for event replay source event hash binding.", (sys.executable, "-m", "unittest", "tests.test_event_replay_hash_binding"), "OK"),
    StandingCheck("event-expected-result-tests", "Run expected-result coverage for destination event and replay fixtures.", (sys.executable, "-m", "unittest", "tests.test_event_expected_results"), "OK"),
    StandingCheck("hash-import-tests", "Run destination hash import formalism tests.", (sys.executable, "-m", "unittest", "tests.test_hash_import"), "OK"),
    StandingCheck("receipt-chain-tests", "Run destination receipt chain formalism tests.", (sys.executable, "-m", "unittest", "tests.test_receipt_chain"), "OK"),
    StandingCheck("formalism-tests", "Run all unittest-discoverable formalism tests.", (sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"), "OK"),
)


def run_check(repo_root: Path, check: StandingCheck) -> StandingResult:
    completed = subprocess.run(check.command, cwd=repo_root, text=True, capture_output=True, check=False)
    combined_output = completed.stdout + completed.stderr
    has_expected_output = check.expected_substring is None or check.expected_substring in combined_output
    return StandingResult(check.check_id, check.description, list(check.command), completed.returncode, completed.returncode == 0 and has_expected_output, completed.stdout, completed.stderr)


def run_all(repo_root: Path, checks: Sequence[StandingCheck]) -> list[StandingResult]:
    return [run_check(repo_root, check) for check in checks]


def result_payload(results: Sequence[StandingResult]) -> dict[str, object]:
    passed = all(result.passed for result in results)
    return {
        "spe_result": "PASS" if passed else "FAIL",
        "repo_standing": "PASS" if passed else "FAIL",
        "mathematical_claim_standing": "PARTIAL",
        "follow_up_actions": [],
        "check_count": len(results),
        "passed_count": sum(1 for result in results if result.passed),
        "results": [asdict(result) for result in results],
        "non_claim": "Repo standing checks validate automation structure only; they do not prove any open mathematical problem.",
    }


def render_markdown(payload: dict[str, object]) -> str:
    rows = []
    for result in payload["results"]:
        status = "PASS" if result["passed"] else "FAIL"
        rows.append(f"| `{result['check_id']}` | **{status}** | {result['description']} |")
    return "\n".join([
        "# Repo Standing Report",
        "",
        f"- SPE Result: **{payload['spe_result']}**",
        f"- Repo Standing: **{payload['repo_standing']}**",
        f"- Mathematical Claim Standing: **{payload['mathematical_claim_standing']}**",
        f"- Passed Checks: **{payload['passed_count']} / {payload['check_count']}**",
        "",
        "## Checks",
        "",
        "| Check | Status | Description |",
        "|---|---:|---|",
        *rows,
        "",
        "## Non-Claim",
        "",
        str(payload["non_claim"]),
        "",
    ])


def write_reports(repo_root: Path, payload: dict[str, object]) -> None:
    reports_dir = repo_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "repo_standing.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (reports_dir / "repo_standing.md").write_text(render_markdown(payload), encoding="utf-8")


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
    print("SPE REPO STANDING:", "PASS" if all(result.passed for result in results) else "FAIL")
    if all(result.passed for result in results):
        print("SPE MATHEMATICAL CLAIM STANDING: PARTIAL")
        print("SPE FOLLOW-UP ACTIONS: []")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run automated SPE repo-standing checks.")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--write-reports", action="store_true", help="write reports/repo_standing.json and reports/repo_standing.md")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    results = run_all(repo_root, CHECKS)
    payload = result_payload(results)

    if args.write_reports:
        write_reports(repo_root, payload)

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        emit_text(results)

    return 0 if all(result.passed for result in results) else 1


if __name__ == "__main__":
    sys.exit(main())
