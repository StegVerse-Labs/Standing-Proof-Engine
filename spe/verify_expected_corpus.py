#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.verify import FAIL, PASS, Check, render
from spe.verify_destination_event import verify_destination_event
from spe.verify_event_replay import verify_event_replay
from spe.verify_expected_result import verify_expected_result
from spe.verify_hash_import import verify_hash_import
from spe.verify_receipt_chain import verify_receipt_chain


def governance_result(artifact):
    if isinstance(artifact.get("event_result"), str):
        return artifact["event_result"]
    if isinstance(artifact.get("replay_result"), str):
        return artifact["replay_result"]
    if isinstance(artifact.get("expected_event_result"), str):
        return artifact["expected_event_result"]
    if isinstance(artifact.get("chain_result"), str):
        return artifact["chain_result"]
    return None


def run_supported_corpus_verifier(verifier, artifact, repo_root):
    if verifier == "spe/verify_destination_event.py":
        return verify_destination_event(artifact, repo_root)
    if verifier == "spe/verify_event_replay.py":
        return verify_event_replay(artifact, repo_root)
    if verifier == "spe/verify_hash_import.py":
        return verify_hash_import(artifact, repo_root)
    if verifier == "spe/verify_receipt_chain.py":
        return verify_receipt_chain(artifact, repo_root)
    return None


def verify_supported_expected_result(fixture, repo_root):
    artifact_ref = fixture.get("artifact")
    verifier = fixture.get("verifier")
    expected = fixture.get("expected", {})
    if not isinstance(artifact_ref, str) or not isinstance(verifier, str) or not isinstance(expected, dict):
        return FAIL, [Check("parse_expected_fixture", FAIL, "artifact, verifier, or expected section missing")]

    artifact_path = (repo_root / artifact_ref).resolve()
    try:
        artifact_path.relative_to(repo_root.resolve())
    except ValueError:
        return FAIL, [Check("parse_expected_fixture", FAIL, "artifact path escapes repo root")]

    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    routed = run_supported_corpus_verifier(verifier, artifact, repo_root)
    if routed is None:
        return verify_expected_result(fixture, repo_root)

    status, checks = routed
    check_map = {check.name: check.status for check in checks}
    result_checks = [Check("parse_expected_fixture", PASS, "expected result fixture parsed")]

    expected_status = expected.get("spe_result")
    result_checks.append(Check(
        "expected_spe_result",
        PASS if status == expected_status else FAIL,
        f"status {status} matched" if status == expected_status else f"expected {expected_status}, got {status}",
    ))

    if "governance_result" in expected:
        actual = governance_result(artifact)
        expected_governance = expected.get("governance_result")
        result_checks.append(Check(
            "expected_governance_result",
            PASS if actual == expected_governance else FAIL,
            f"governance result {actual} matched" if actual == expected_governance else f"expected {expected_governance}, got {actual}",
        ))

    required = expected.get("required_checks", {})
    if not isinstance(required, dict):
        result_checks.append(Check("expected_required_checks", FAIL, "required_checks is not an object"))
    else:
        for name, required_status in required.items():
            actual_status = check_map.get(name)
            result_checks.append(Check(
                f"expected_check:{name}",
                PASS if actual_status == required_status else FAIL,
                f"{name} matched {required_status}" if actual_status == required_status else f"expected {required_status}, got {actual_status}",
            ))

    return (FAIL if any(check.status == FAIL for check in result_checks) else PASS), result_checks


def verify_expected_corpus(corpus_dir, repo_root):
    if not corpus_dir.exists():
        return FAIL, [Check("expected_corpus", FAIL, "expected result directory missing")]

    checks = []
    fixture_paths = sorted(corpus_dir.glob("*.expected.json"))
    if not fixture_paths:
        return FAIL, [Check("expected_corpus", FAIL, "no expected result fixtures found")]

    for fixture_path in fixture_paths:
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        status, fixture_checks = verify_supported_expected_result(fixture, repo_root)
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
