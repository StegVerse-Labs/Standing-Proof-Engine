#!/usr/bin/env python3
"""Generate and persist a JSON inventory for expected-result fixtures."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_RESULTS = ROOT / "expected_results"
REPORTS = ROOT / "reports"
INVENTORY_PATH = REPORTS / "expected_corpus_inventory.json"


def _run_fixture(path: Path) -> dict[str, object]:
    relative = path.relative_to(ROOT).as_posix()
    command = [sys.executable, "-m", "spe.verify_expected_result", relative]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    passed = completed.returncode == 0
    return {
        "fixture": relative,
        "passed": passed,
        "returncode": completed.returncode,
        "failed_checks": [] if passed else ["verify_expected_result"],
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def build_inventory() -> dict[str, object]:
    fixtures = sorted(EXPECTED_RESULTS.glob("*.expected.json")) if EXPECTED_RESULTS.exists() else []
    results = [_run_fixture(path) for path in fixtures]
    failed = [result for result in results if not result["passed"]]
    return {
        "spe_result": "PASS" if not failed else "FAIL",
        "fixture_count": len(results),
        "failed_fixture_count": len(failed),
        "failed_fixtures": failed,
        "fixtures": results,
    }


def main() -> int:
    inventory = build_inventory()
    rendered = json.dumps(inventory, indent=2, sort_keys=True) + "\n"

    REPORTS.mkdir(parents=True, exist_ok=True)
    INVENTORY_PATH.write_text(rendered, encoding="utf-8")

    print(rendered, end="")
    print(f"wrote: {INVENTORY_PATH.relative_to(ROOT)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
