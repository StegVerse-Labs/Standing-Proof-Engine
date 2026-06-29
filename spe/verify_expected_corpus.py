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
    args = list(argv[1:])
    emit_json = False
    if "--json" in args:
        emit_json = True
        args = [a for a in args if a != "--json"]

    if len(args) > 1:
        print("usage: python -m spe.verify_expected_corpus [expected_results_dir] [--json]", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    corpus_dir = repo_root / "expected_results"
    if len(args) == 1:
        corpus_dir = (repo_root / args[0]).resolve()

    status, checks = verify_expected_corpus(corpus_dir, repo_root)
    if emit_json:
        print(json.dumps({
            "spe_result": status,
            "checks": [{"name": c.name, "status": c.status, "detail": getattr(c, "detail", "")} for c in checks],
        }, indent=2))
    else:
        print(render(status, checks))
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
