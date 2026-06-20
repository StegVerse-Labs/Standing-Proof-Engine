#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.verify import FAIL, PASS, Check, render
from spe.verify_expected_result import verify_expected_result


def verify_expected_corpus(corpus_dir, repo_root):
    if not corpus_dir.exists():
        return FAIL, [Check("expected_corpus", FAIL, "expected result directory missing")]

    checks = []
    fixture_paths = sorted(corpus_dir.glob("*.expected.json"))
    if not fixture_paths:
        return FAIL, [Check("expected_corpus", FAIL, "no expected result fixtures found")]

    for fixture_path in fixture_paths:
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        status, fixture_checks = verify_expected_result(fixture, repo_root)
        if status == PASS:
            checks.append(Check(f"fixture:{fixture_path.name}", PASS, "expected fixture matched"))
        else:
            failed = [check.name for check in fixture_checks if check.status == FAIL]
            checks.append(Check(f"fixture:{fixture_path.name}", FAIL, ", ".join(failed)))

    if any(check.status == FAIL for check in checks):
        return FAIL, checks
    return PASS, checks


def main(argv):
    if len(argv) not in (1, 2):
        print("usage: python spe/verify_expected_corpus.py [expected_results_dir]", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    corpus_dir = repo_root / "expected_results"
    if len(argv) == 2:
        corpus_dir = (repo_root / argv[1]).resolve()

    status, checks = verify_expected_corpus(corpus_dir, repo_root)
    print(render(status, checks))
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
