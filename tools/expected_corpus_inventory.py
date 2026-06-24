#!/usr/bin/env python3
"""Inventory expected-result fixtures and their canonical verifier outcomes."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from spe.verify import FAIL, PASS
from spe.verify_expected_result import verify_expected_result


def inventory_expected_corpus(corpus_dir: Path, repo_root: Path) -> dict[str, object]:
    fixtures = []
    for fixture_path in sorted(corpus_dir.glob("*.expected.json")):
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        status, checks = verify_expected_result(fixture, repo_root)
        fixtures.append(
            {
                "fixture": fixture_path.name,
                "status": status,
                "failed_checks": [check.name for check in checks if check.status == FAIL],
                "passed_checks": [check.name for check in checks if check.status == PASS],
            }
        )

    failed = [item for item in fixtures if item["status"] != PASS]
    return {
        "spe_result": PASS if not failed else FAIL,
        "fixture_count": len(fixtures),
        "failed_fixture_count": len(failed),
        "failed_fixtures": failed,
        "fixtures": fixtures,
    }


def main(argv: list[str]) -> int:
    if len(argv) not in (1, 2):
        print("usage: python tools/expected_corpus_inventory.py [expected_results_dir]", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    corpus_dir = repo_root / "expected_results"
    if len(argv) == 2:
        corpus_dir = (repo_root / argv[1]).resolve()

    payload = inventory_expected_corpus(corpus_dir, repo_root)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["spe_result"] == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
