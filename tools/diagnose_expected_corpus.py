#!/usr/bin/env python3
"""Emit detailed expected-corpus fixture diagnostics.

This tool is intentionally diagnostic: it does not change state, refresh hashes,
or mark standing. It exposes every failing fixture and failing expected check so
repo-node or PR-runner output can be inspected without relying on truncated logs.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from spe.verify import FAIL, PASS
from spe.verify_expected_result import verify_expected_result


def diagnose(corpus_dir: Path, repo_root: Path) -> dict[str, Any]:
    fixture_reports: list[dict[str, Any]] = []
    for fixture_path in sorted(corpus_dir.glob("*.expected.json")):
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        status, checks = verify_expected_result(fixture, repo_root)
        failing_checks = [
            {
                "name": check.name,
                "status": check.status,
                "detail": check.detail,
            }
            for check in checks
            if check.status == FAIL
        ]
        fixture_reports.append(
            {
                "fixture": fixture_path.name,
                "artifact": fixture.get("artifact"),
                "verifier": fixture.get("verifier"),
                "status": status,
                "failing_checks": failing_checks,
            }
        )

    failing = [report for report in fixture_reports if report["status"] != PASS]
    return {
        "spe_result": "PASS" if not failing else "FAIL",
        "fixture_count": len(fixture_reports),
        "failing_count": len(failing),
        "failing_fixtures": failing,
        "fixtures": fixture_reports,
    }


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parents[1]
    corpus_dir = repo_root / "expected_results"
    if len(argv) == 2:
        corpus_dir = (repo_root / argv[1]).resolve()

    payload = diagnose(corpus_dir, repo_root)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["spe_result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
