#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.verify import FAIL, PASS, Check, render
from spe.verify_expected_result import verify_expected_result


def verify_derived_state_current(repo_root):
    """Guard expected-corpus consumption with a derived-state recheck.

    This is the repo-node/micro-node transition boundary for frozen derived
    hashes. Expected-corpus validation is a consumer of derived state, so it
    must not begin if known derived bindings have drifted.

    The guard does not rewrite files during CI/admissibility validation. It
    reports REFRESH_REQUIRED so a repair branch or repo-node cycle can run the
    refresh writer before retrying consumption.
    """
    from tools.refresh_frozen_hashes import compute_expected, _load

    drift = []
    for rel, field, expected in compute_expected():
        actual = _load(rel).get(field)
        if actual != expected:
            drift.append(
                {
                    "artifact": rel,
                    "field": field,
                    "actual": actual,
                    "expected": expected,
                }
            )

    if drift:
        rendered = "; ".join(
            f"{item['artifact']}::{item['field']} expected {item['expected']} got {item['actual']}"
            for item in drift
        )
        return FAIL, Check(
            "pre_corpus_derived_state",
            FAIL,
            "REFRESH_REQUIRED " + rendered,
        )

    return PASS, Check(
        "pre_corpus_derived_state",
        PASS,
        "derived state current before expected-corpus consumption",
    )


def verify_expected_corpus(corpus_dir, repo_root):
    if not corpus_dir.exists():
        return FAIL, [Check("expected_corpus", FAIL, "expected result directory missing")]

    checks = []

    state_status, state_check = verify_derived_state_current(repo_root)
    checks.append(state_check)
    if state_status == FAIL:
        return FAIL, checks

    fixture_paths = sorted(corpus_dir.glob("*.expected.json"))
    if not fixture_paths:
        return FAIL, checks + [Check("expected_corpus", FAIL, "no expected result fixtures found")]

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
