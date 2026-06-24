#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.verify import FAIL, PASS, Check, render, verify_artifact
from spe.verify_confirmation import verify_confirmation
from spe.verify_destination_event import verify_destination_event
from spe.verify_event_replay import verify_event_replay
from spe.verify_external_refs import verify_external_ref_artifact
from spe.verify_hash_import import verify_hash_import
from spe.verify_pointer import verify_pointer
from spe.verify_receipt_chain import verify_receipt_chain
from spe.verify_sdk_intake import verify_sdk_intake
from spe.verify_source_bound import verify_source_bound_artifact


def run_declared_verifier(verifier, artifact, repo_root):
    if verifier == "spe/verify_destination_event.py":
        return verify_destination_event(artifact, repo_root)
    if verifier == "spe/verify_event_replay.py":
        return verify_event_replay(artifact, repo_root)
    if verifier == "spe/verify_external_refs.py":
        return verify_external_ref_artifact(artifact, repo_root)
    if verifier == "spe/verify_source_bound.py":
        return verify_source_bound_artifact(artifact)
    if verifier == "spe/verify_sdk_intake.py":
        return verify_sdk_intake(artifact, repo_root)
    if verifier == "spe/verify_pointer.py":
        return verify_pointer(artifact, repo_root)
    if verifier == "spe/verify_confirmation.py":
        return verify_confirmation(artifact, repo_root)
    if verifier == "spe/verify_hash_import.py":
        return verify_hash_import(artifact, repo_root)
    if verifier == "spe/verify_receipt_chain.py":
        return verify_receipt_chain(artifact, repo_root)
    if verifier == "spe/verify.py":
        return verify_artifact(artifact)
    return FAIL, [Check("select_verifier", FAIL, f"unknown verifier {verifier}")]


def governance_result(artifact):
    receipt = artifact.get("receipt", {})
    if isinstance(receipt, dict) and isinstance(receipt.get("decision"), str):
        return receipt["decision"]
    if isinstance(artifact.get("final_decision"), str):
        return artifact["final_decision"]
    if isinstance(artifact.get("confirmation_result"), str):
        return artifact["confirmation_result"]
    if isinstance(artifact.get("event_result"), str):
        return artifact["event_result"]
    if isinstance(artifact.get("observed_result"), str):
        return artifact["observed_result"]
    if isinstance(artifact.get("expected_event_result"), str):
        return artifact["expected_event_result"]
    if isinstance(artifact.get("chain_result"), str):
        return artifact["chain_result"]
    evaluation = artifact.get("standing_evaluation", {})
    if isinstance(evaluation, dict) and isinstance(evaluation.get("result"), str):
        return evaluation["result"]
    if isinstance(artifact.get("expected_package_status"), str):
        return artifact["expected_package_status"]
    target = artifact.get("reconstruction_target", {})
    if isinstance(target, dict) and isinstance(target.get("expected_package_status"), str):
        return target["expected_package_status"]
    return None


def verify_expected_result(fixture, repo_root):
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
    status, checks = run_declared_verifier(verifier, artifact, repo_root)
    check_map = {check.name: check.status for check in checks}

    result_checks = [Check("parse_expected_fixture", PASS, "expected result fixture parsed")]
    expected_status = expected.get("spe_result")
    if status == expected_status:
        result_checks.append(Check("expected_spe_result", PASS, f"status {status} matched"))
    else:
        result_checks.append(Check("expected_spe_result", FAIL, f"expected {expected_status}, got {status}"))

    if "governance_result" in expected:
        actual_governance_result = governance_result(artifact)
        expected_governance_result = expected.get("governance_result")
        if actual_governance_result == expected_governance_result:
            result_checks.append(Check("expected_governance_result", PASS, f"governance result {actual_governance_result} matched"))
        else:
            result_checks.append(Check("expected_governance_result", FAIL, f"expected {expected_governance_result}, got {actual_governance_result}"))

    required = expected.get("required_checks", {})
    if not isinstance(required, dict):
        result_checks.append(Check("expected_required_checks", FAIL, "required_checks is not an object"))
    else:
        for name, required_status in required.items():
            actual_status = check_map.get(name)
            if actual_status == required_status:
                result_checks.append(Check(f"expected_check:{name}", PASS, f"{name} matched {required_status}"))
            else:
                result_checks.append(Check(f"expected_check:{name}", FAIL, f"expected {required_status}, got {actual_status}"))

    if any(check.status == FAIL for check in result_checks):
        return FAIL, result_checks
    return PASS, result_checks


def main(argv):
    if len(argv) != 2:
        print("usage: python spe/verify_expected_result.py <expected.json>", file=sys.stderr)
        return 2
    repo_root = Path(__file__).resolve().parents[1]
    fixture = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    status, checks = verify_expected_result(fixture, repo_root)
    print(render(status, checks))
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
