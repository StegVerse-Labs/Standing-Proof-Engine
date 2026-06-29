#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Any

from spe.result_export import result_dict
from spe.tt_registry import resolve_transition
from spe.verify import FAIL, PARTIAL, PASS, verify_artifact


def governance_result(artifact: dict[str, Any]) -> str | None:
    receipt = artifact.get("receipt", {})
    if isinstance(receipt, dict) and isinstance(receipt.get("decision"), str):
        return receipt["decision"]
    if isinstance(artifact.get("final_decision"), str):
        return artifact["final_decision"]
    return None


def _hash_label(value: str) -> str:
    return value.replace(" ", "_").replace(":", "_").lower()


def artifact_from_transition_case(test_case: dict[str, Any]) -> dict[str, Any]:
    transition_cell = test_case["transition_cell"]
    tt_transition_id = test_case.get("tt_transition_id") or test_case.get("transition_id") or transition_cell
    tt_resolution = resolve_transition(tt_transition_id)
    failed_dimensions = test_case.get("failed_dimensions", [])
    required_dimensions = test_case.get(
        "required_dimensions",
        [
            "actor",
            "target",
            "scope",
            "policy",
            "delegation",
            "context",
            "validity_window",
            "recoverability",
        ],
    )
    dimension_states = {
        dimension: dimension not in failed_dimensions
        for dimension in required_dimensions
    }
    bindings = {
        dimension: {
            "candidate_value": test_case.get(dimension),
            "current_value": test_case.get("current_state", {}).get(dimension, test_case.get(dimension)),
            "matches_candidate": dimension not in failed_dimensions,
        }
        for dimension in required_dimensions
    }
    decision = test_case.get("expected_governance_result", "FAIL_CLOSED")

    return {
        "artifact_type": "commitment_candidate_test",
        "test_id": test_case["test_id"],
        "schema_version": "0.3",
        "generated_from": "transition_case_manifest",
        "scenario": test_case.get("scenario", test_case["test_id"]),
        "historical_review": {
            "review_id": test_case.get("historical_review_ref"),
            "transition_cell_id": transition_cell,
            "tt_transition_id": tt_resolution.transition_id,
            "review_artifact_hash": f"review_{_hash_label(test_case.get('historical_review_ref', 'unknown'))}",
            "evidence_packet_hash": f"evidence_{_hash_label('_'.join(test_case.get('evidence_refs', ['unknown'])))}",
            "decision": "REVIEWED",
            "replayable": True,
            "carries_execution_authority": False,
        },
        "commitment_candidate": {
            "candidate_id": test_case.get("candidate_id", f"candidate_{test_case['test_id']}"),
            "candidate_type": "commitment_candidate",
            "transition_cell_id": transition_cell,
            "tt_transition_id": tt_resolution.transition_id,
            "tt_code_ref": tt_resolution.code_ref,
            "requested_action": test_case.get("requested_action"),
            "actor": test_case.get("actor"),
            "target": test_case.get("target"),
            "scope": test_case.get("scope"),
            "policy_ref": test_case.get("policy_ref"),
            "delegation_ref": test_case.get("delegation_ref"),
            "evidence_refs": test_case.get("evidence_refs", []),
            "execution_context": test_case.get("execution_context"),
            "validity_window": test_case.get("validity_window"),
            "recoverability_profile": test_case.get("recoverability_profile"),
            "commit_requested": True,
            "carries_execution_authority": False,
            "inherits_review_authority": False,
        },
        "current_state": {
            "state_id": test_case.get("current_state", {}).get("state_id", f"current_{test_case['test_id']}"),
            "bindings": bindings,
        },
        "standing_rule": {
            "rule_id": test_case.get("standing_rule_id", "SPE-COMMITMENT-CANDIDATE-001"),
            "description": "Commitment Candidate is non-authorizing; SPE must re-bind standing at commit time.",
            "requires": required_dimensions,
        },
        "standing_evaluation": {
            "historical_review_replayable": True,
            "candidate_carries_authority": False,
            "dimension_current_or_rebound": dimension_states,
            "failed_dimensions": failed_dimensions,
            "aggregate_standing": False,
            "result": decision,
        },
        "receipt": {
            "receipt_id": test_case.get("receipt_id", f"receipt_{test_case['test_id']}"),
            "receipt_type": "commit_time_standing_receipt",
            "transition_cell_id": transition_cell,
            "tt_transition_id": tt_resolution.transition_id,
            "tt_transition_receipt": tt_resolution.as_receipt(),
            "candidate_carries_authority": False,
            "commit_allowed": False,
            "failed_dimensions": failed_dimensions,
            "decision": decision,
            "reason": test_case.get("reason", "Current standing failed for one or more required dimensions."),
        },
        "formalism_expectation": {
            "expected_result": decision,
            "expected_spe_status": test_case.get("expected_spe_result", PASS),
        },
    }


def _sample_artifact(root: Path, sample: dict[str, Any]) -> dict[str, Any]:
    if "path" in sample:
        sample_path = root / sample["path"]
        return json.loads(sample_path.read_text(encoding="utf-8"))
    if "transition_case" in sample:
        return artifact_from_transition_case(sample["transition_case"])
    raise KeyError("sample must declare either path or transition_case")


def _sample_label(sample: dict[str, Any]) -> str:
    if "path" in sample:
        return sample["path"]
    return sample.get("transition_case", {}).get("test_id", "inline_transition_case")


def verify_manifest(manifest_path: Path) -> tuple[str, dict[str, Any]]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    root = manifest_path.resolve().parents[1]
    sample_results = []
    manifest_status = PASS

    for sample in manifest.get("samples", []):
        artifact = _sample_artifact(root, sample)
        status, checks = verify_artifact(artifact)
        observed_result = governance_result(artifact)
        expected_spe = sample.get("expected_spe_result")
        expected_result = sample.get("expected_governance_result")
        if expected_spe is None and "transition_case" in sample:
            expected_spe = sample["transition_case"].get("expected_spe_result")
        if expected_result is None and "transition_case" in sample:
            expected_result = sample["transition_case"].get("expected_governance_result")
        matches = status == expected_spe and observed_result == expected_result

        if status == FAIL or not matches:
            manifest_status = FAIL
        elif status == PARTIAL and manifest_status == PASS:
            manifest_status = PARTIAL

        exported = result_dict(artifact, status, checks)
        sample_results.append({
            "path": sample.get("path"),
            "test_id": artifact.get("test_id"),
            "route": sample.get("route"),
            "spe_result": status,
            "expected_spe_result": expected_spe,
            "governance_result": observed_result,
            "expected_governance_result": expected_result,
            "matches_expectation": matches,
            "artifact_hash": exported["hashes"]["artifact"],
            "artifact_type": exported["artifact_type"],
            "tt_transition_id": artifact.get("receipt", {}).get("tt_transition_id"),
            "tt_code_ref": artifact.get("commitment_candidate", {}).get("tt_code_ref"),
            "check_count": len(checks),
            "source": "path" if "path" in sample else "transition_case",
            "label": _sample_label(sample),
        })

    report = {
        "manifest_id": manifest.get("manifest_id"),
        "spe_result": manifest_status,
        "sample_count": len(sample_results),
        "samples": sample_results,
    }
    return manifest_status, report


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python spe/verify_manifest.py <manifest.json>", file=sys.stderr)
        return 2
    status, report = verify_manifest(Path(argv[1]))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if status in {PASS, PARTIAL} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
