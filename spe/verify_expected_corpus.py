#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.verify import FAIL, PASS, Check, render
from spe.verify_expected_result import verify_expected_result


def verify_derived_state_current(repo_root):
    """Guard expected-corpus consumption with a derived-state recheck.

    Expected-corpus validation is a downstream consumer of derived state, so it
    must not begin if known frozen derived bindings have drifted.
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
        failed = [check.name for check in fixture_checks if check.status == FAIL]
        if status == PASS:
            checks.append(Check(f"fixture:{fixture_path.name}", PASS, "expected fixture matched"))
        else:
            detail = ", ".join(failed) if failed else "unknown fixture failure"
            checks.append(Check(f"fixture:{fixture_path.name}", FAIL, detail))

    if any(check.status == FAIL for check in checks):
        return FAIL, checks

    return PASS, checks


def corpus_payload(status, checks):
    return {
        "spe_result": status,
        "failed_fixtures": [
            {"name": check.name, "detail": check.detail}
            for check in checks
            if check.status == FAIL and check.name.startswith("fixture:")
        ],
        "checks": [
            {"name": check.name, "status": check.status, "detail": check.detail}
            for check in checks
        ],
    }


def main(argv):
    if len(argv) not in (1, 2, 3):
        print("usage: python spe/verify_expected_corpus.py [--json] [expected_results_dir]", file=sys.stderr)
        return 2

    json_mode = False
    args = list(argv[1:])
    if args and args[0] == "--json":
        json_mode = True
        args = args[1:]

    repo_root = Path(__file__).resolve().parents[1]
    corpus_dir = repo_root / "expected_results"
    if args:
        corpus_dir = (repo_root / args[0]).resolve()

    status, checks = verify_expected_corpus(corpus_dir, repo_root)
    if json_mode:
        print(json.dumps(corpus_payload(status, checks), indent=2, sort_keys=True))
    else:
        print(render(status, checks))
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
