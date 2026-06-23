#!/usr/bin/env python3
"""Check the SPE automation addendum metadata."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ADDENDUM_PATH = "research/automation_addendum.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check SPE automation addendum metadata.")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    failures: list[str] = []

    addendum_path = repo_root / ADDENDUM_PATH
    if not addendum_path.exists():
        failures.append(f"missing {ADDENDUM_PATH}")
        data: dict[str, Any] = {}
    else:
        try:
            data = load_json(addendum_path)
        except json.JSONDecodeError as exc:
            failures.append(f"invalid JSON: {exc}")
            data = {}

    if data:
        if data.get("addendum_id") != "spe_research_automation_addendum_001":
            failures.append("unexpected addendum_id")
        if data.get("repo") != "StegVerse-Labs/Standing-Proof-Engine":
            failures.append("unexpected repo")
        if data.get("status") != "PASS":
            failures.append("status must be PASS")

        runner = data.get("automation_runner")
        if not isinstance(runner, dict):
            failures.append("automation_runner must be an object")
        else:
            runner_path = runner.get("path")
            if runner_path != "tools/run_repo_standing.py":
                failures.append("runner path mismatch")
            elif not (repo_root / runner_path).exists():
                failures.append("runner file is missing")
            if runner.get("text_command") != "python tools/run_repo_standing.py":
                failures.append("text command mismatch")
            if runner.get("json_command") != "python tools/run_repo_standing.py --json":
                failures.append("json command mismatch")

        ci_route = data.get("ci_route")
        if not isinstance(ci_route, dict):
            failures.append("ci_route must be an object")
        else:
            if ci_route.get("display_path") != "github/workflows/verify.yml":
                failures.append("workflow display path mismatch")
            if not (repo_root / ".github/workflows/verify.yml").exists():
                failures.append("workflow file is missing")
            required_steps = ci_route.get("required_steps")
            if not isinstance(required_steps, list):
                failures.append("ci_route.required_steps must be a list")
            else:
                for command in [
                    "python tools/run_repo_standing.py",
                    "python tools/run_repo_standing.py --json",
                ]:
                    if command not in required_steps:
                        failures.append(f"missing CI step: {command}")

        component_checks = data.get("component_checks")
        if not isinstance(component_checks, list) or len(component_checks) < 5:
            failures.append("component_checks must list at least five checks")

        non_claims = data.get("non_claims")
        if not isinstance(non_claims, list) or len(non_claims) < 3:
            failures.append("non_claims must list at least three entries")

    passed = not failures
    payload = {
        "spe_result": "PASS" if passed else "FAIL",
        "automation_addendum": "PASS" if passed else "FAIL",
        "checked_file": ADDENDUM_PATH,
        "failures": failures,
        "follow_up_actions": [],
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        if passed:
            print("SPE AUTOMATION ADDENDUM: PASS")
            print("SPE FOLLOW-UP ACTIONS: []")
        else:
            print("SPE AUTOMATION ADDENDUM: FAIL")
            for failure in failures:
                print(f"- {failure}")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
