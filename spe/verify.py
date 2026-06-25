#!/usr/bin/env python3
"""Standing-Proof-Engine verifier.

This verifier evaluates small governance artifacts and returns PASS, PARTIAL,
or FAIL with reconstructable reasons.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PASS = "PASS"
PARTIAL = "PARTIAL"
FAIL = "FAIL"
FAIL_CLOSED = "FAIL_CLOSED"
DENY = "DENY"


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    detail: str


def _status(checks: list[Check]) -> str:
    statuses = {check.status for check in checks}
    if FAIL in statuses:
        return FAIL
    if PARTIAL in statuses:
        return PARTIAL
    return PASS


def _step(trace: dict[str, Any], index: int) -> dict[str, Any] | None:
    for item in trace.get("execution_trace", []):
        if item.get("step_index") == index:
            return item
    return None


def _result_denies_consequence(result: Any) -> bool:
    return result in {DENY, FAIL_CLOSED}


def verify_pressure_trace(trace: dict[str, Any]) -> tuple[str, list[Check]]:
    checks: list[Check] = []

    baseline = trace.get("baseline")
    execution_trace = trace.get("execution_trace")
    if not isinstance(baseline, dict) or not isinstance(execution_trace, list):
        return FAIL, [Check("parse_trace", FAIL, "missing baseline or execution_trace")]

    checks.append(Check("parse_trace", PASS, "trace contains baseline and execution_trace"))

    step0 = _step(trace, 0)
    step1 = _step(trace, 1)
    step2 = _step(trace, 2)
    step3 = _step(trace, 3)

    if not all([step0, step1, step2, step3]):
        checks.append(Check("required_steps", FAIL, "expected steps 0, 1, 2, and 3"))
        return _status(checks), checks

    checks.append(Check("required_steps", PASS, "authorization, drift, receipt, and commit steps found"))

    step0_meta = step0.get("metadata", {})
    baseline_matches_step0 = (
        baseline.get("policy_version") == step0_meta.get("policy_version")
        and baseline.get("delegation_chain") == step0_meta.get("delegation_chain")
        and baseline.get("observer_identity_hash") == step0.get("observer_identity_hash")
        and baseline.get("reference_frame_hash") == step0.get("reference_frame_hash")
    )
    checks.append(
        Check(
            "baseline_reconstruction",
            PASS if baseline_matches_step0 else FAIL,
            "baseline matches authorization step" if baseline_matches_step0 else "baseline does not match authorization step",
        )
    )

    step1_meta = step1.get("metadata", {})
    policy_changed = step0_meta.get("policy_version") != step1_meta.get("policy_version")
    delegation_changed = step0_meta.get("delegation_chain") != step1_meta.get("delegation_chain")
    pressure_entered = step1_meta.get("pressure_region_entered") is True
    drift_observed = policy_changed or delegation_changed
    checks.append(
        Check(
            "drift_observation",
            PASS if drift_observed and pressure_entered else FAIL,
            "policy/delegation drift observed and pressure region entered"
            if drift_observed and pressure_entered
            else "drift or pressure-region evidence missing",
        )
    )

    receipt_meta = step2.get("metadata", {})
    receipt_present = receipt_meta.get("receipt_type") == "pressure_receipt"
    checks.append(
        Check(
            "pressure_receipt",
            PASS if receipt_present else FAIL,
            "pressure receipt recorded" if receipt_present else "pressure receipt missing",
        )
    )

    predicates = receipt_meta.get("local_predicate_states", {})
    predicate_shape_valid = all(
        key in predicates
        for key in ["identity_valid", "policy_valid", "delegation_valid", "evidence_fresh"]
    )
    expected_predicates = (
        predicates.get("identity_valid") is True
        and predicates.get("policy_valid") is False
        and predicates.get("delegation_valid") is False
        and predicates.get("evidence_fresh") is True
    )
    checks.append(
        Check(
            "local_predicates",
            PASS if predicate_shape_valid and expected_predicates else FAIL,
            "identity/evidence remain valid while policy/delegation fail"
            if predicate_shape_valid and expected_predicates
            else "local predicate state is incomplete or inconsistent",
        )
    )

    aggregate_denied = receipt_meta.get("aggregate_admissibility") is False
    checks.append(
        Check(
            "aggregate_admissibility",
            PASS if aggregate_denied else FAIL,
            "aggregate admissibility is false" if aggregate_denied else "aggregate admissibility did not resolve false",
        )
    )

    commit_denied = (
        step3.get("decision") == "DENY"
        and step3.get("metadata", {}).get("commit_allowed") is False
        and step3.get("metadata", {}).get("pressure_receipt_reference") == "step_index_2"
    )
    checks.append(
        Check(
            "commit_boundary",
            PASS if commit_denied else FAIL,
            "commit denied and linked to pressure receipt" if commit_denied else "commit denial is missing or not linked",
        )
    )

    replay = trace.get("replay_path", {})
    replay_valid = (
        replay.get("policy_v1", {}).get("decision") == "ADMIT"
        and replay.get("policy_v2", {}).get("decision") == "DENY"
        and trace.get("final_decision") == "DENY"
    )
    checks.append(
        Check(
            "replay_path",
            PASS if replay_valid else FAIL,
            "replay shows v1 ADMIT, v2 DENY, final DENY" if replay_valid else "replay path is incomplete or inconsistent",
        )
    )

    baseline_hashes = receipt_meta.get("baseline_hashes", {})
    current_hashes = receipt_meta.get("current_hashes_at_pressure_boundary", {})
    baseline_reference_hash = baseline_hashes.get("reference_frame_hash")
    current_reference_hash = current_hashes.get("reference_frame_hash")
    drift_claim = receipt_meta.get("drift_detected")

    if drift_claim == "reference_frame_changed" and baseline_reference_hash == current_reference_hash:
        checks.append(
            Check(
                "authority_context_proof",
                PARTIAL,
                "metadata shows policy/delegation drift, but reference_frame_hash did not change",
            )
        )
    elif drift_claim and baseline_reference_hash != current_reference_hash:
        checks.append(
            Check(
                "authority_context_proof",
                PASS,
                "reference-frame drift is cryptographically distinguishable",
            )
        )
    else:
        checks.append(
            Check(
                "authority_context_proof",
                FAIL,
                "authority-context drift is not supported",
            )
        )

    return _status(checks), checks


def verify_stale_state_proof(proof: dict[str, Any]) -> tuple[str, list[Check]]:
    checks: list[Check] = []

    required_sections = [
        "review_time",
        "commit_time",
        "standing_rule",
        "standing_evaluation",
        "receipt",
    ]
    missing = [section for section in required_sections if not isinstance(proof.get(section), dict)]
    if missing:
        return FAIL, [Check("parse_proof", FAIL, f"missing sections: {', '.join(missing)}")]

    checks.append(Check("parse_proof", PASS, "proof contains review, commit, rule, evaluation, and receipt sections"))

    review = proof["review_time"]
    commit = proof["commit_time"]
    rule = proof["standing_rule"]
    evaluation = proof["standing_evaluation"]
    receipt = proof["receipt"]

    same_cell = review.get("transition_cell_id") == commit.get("transition_cell_id") == receipt.get("transition_cell_id")
    review_replayable = review.get("replayable") is True and evaluation.get("review_artifact_replayable") is True
    checks.append(
        Check(
            "review_artifact",
            PASS if same_cell and review_replayable else FAIL,
            "same transition cell remains replayable from review artifact"
            if same_cell and review_replayable
            else "review artifact is not tied to the same replayable transition cell",
        )
    )

    authority_changed = review.get("authority_state_hash") != commit.get("authority_state_hash")
    policy_changed = review.get("policy_hash") != commit.get("policy_hash")
    evidence_same_but_stale = (
        review.get("evidence_packet_hash") == commit.get("evidence_packet_hash")
        and commit.get("evidence_status") == "STALE"
    )
    commit_requested = commit.get("commit_requested") is True
    checks.append(
        Check(
            "commit_state",
            PASS if authority_changed and policy_changed and evidence_same_but_stale and commit_requested else FAIL,
            "commit-time authority/policy changed and retained evidence is stale"
            if authority_changed and policy_changed and evidence_same_but_stale and commit_requested
            else "commit-time stale or changed condition is incomplete",
        )
    )

    required_rule = rule.get("requires", {})
    rule_complete = all(
        key in required_rule
        for key in ["authority_state", "policy_state", "evidence_state", "context_state"]
    )
    checks.append(
        Check(
            "standing_rule",
            PASS if rule_complete else FAIL,
            "standing rule binds authority, policy, evidence, and context"
            if rule_complete
            else "standing rule does not bind all required state dimensions",
        )
    )

    expected_false_conditions = [
        evaluation.get("authority_current_or_reauthorized") is False,
        evaluation.get("policy_current_or_reauthorized") is False,
        evaluation.get("evidence_fresh_or_revalidated") is False,
    ]
    expected_true_conditions = [
        evaluation.get("review_artifact_replayable") is True,
        evaluation.get("evidence_packet_useful") is True,
        evaluation.get("context_current_or_reauthorized") is True,
    ]
    evaluation_denies = evaluation.get("aggregate_standing") is False and _result_denies_consequence(evaluation.get("result"))
    evaluation_valid = all(expected_false_conditions) and all(expected_true_conditions) and evaluation_denies
    checks.append(
        Check(
            "standing_evaluation",
            PASS if evaluation_valid else FAIL,
            "review remains useful while aggregate commit-time standing is false"
            if evaluation_valid
            else "standing evaluation does not support DENY or FAIL_CLOSED",
        )
    )

    receipt_decision = receipt.get("decision")
    receipt_valid = (
        receipt.get("receipt_type") == "commit_time_standing_receipt"
        and receipt.get("prior_review_replayable") is True
        and receipt.get("commit_allowed") is False
        and _result_denies_consequence(receipt_decision)
        and receipt_decision == evaluation.get("result")
    )
    checks.append(
        Check(
            "receipt",
            PASS if receipt_valid else FAIL,
            "receipt records replayable prior review and commit-time denial"
            if receipt_valid
            else "standing receipt is incomplete or inconsistent",
        )
    )

    expected = proof.get("formalism_expectation", {})
    expected_status = expected.get("expected_spe_status")
    if expected_status:
        actual_status = _status(checks)
        checks.append(
            Check(
                "formalism_expectation",
                PASS if actual_status == expected_status else FAIL,
                f"actual status {actual_status} matches expectation {expected_status}"
                if actual_status == expected_status
                else f"actual status {actual_status} differs from expectation {expected_status}",
            )
        )

    return _status(checks), checks


def verify_commitment_candidate_test(test: dict[str, Any]) -> tuple[str, list[Check]]:
    checks: list[Check] = []
    required_sections = [
        "historical_review",
        "commitment_candidate",
        "current_state",
        "standing_rule",
        "standing_evaluation",
        "receipt",
    ]
    missing = [section for section in required_sections if not isinstance(test.get(section), dict)]
    if missing:
        return FAIL, [Check("parse_commitment_candidate_test", FAIL, f"missing sections: {', '.join(missing)}")]

    checks.append(Check("parse_commitment_candidate_test", PASS, "commitment-candidate test sections parsed"))

    review = test["historical_review"]
    candidate = test["commitment_candidate"]
    current = test["current_state"]
    rule = test["standing_rule"]
    evaluation = test["standing_evaluation"]
    receipt = test["receipt"]

    same_cell = (
        review.get("transition_cell_id")
        == candidate.get("transition_cell_id")
        == receipt.get("transition_cell_id")
    )
    review_replayable = review.get("replayable") is True and evaluation.get("historical_review_replayable") is True
    checks.append(
        Check(
            "historical_review",
            PASS if same_cell and review_replayable else FAIL,
            "historical review is replayable and tied to the proposed transition cell"
            if same_cell and review_replayable
            else "historical review is missing replayability or transition-cell binding",
        )
    )

    non_authorizing = (
        candidate.get("candidate_type") == "commitment_candidate"
        and candidate.get("carries_execution_authority") is False
        and candidate.get("inherits_review_authority") is False
        and candidate.get("commit_requested") is True
    )
    checks.append(
        Check(
            "candidate_non_authorizing",
            PASS if non_authorizing else FAIL,
            "candidate presents the proposed crossing without carrying authority"
            if non_authorizing
            else "candidate appears to authorize execution or lacks commit request binding",
        )
    )

    required_dimensions = rule.get("requires", [])
    if not isinstance(required_dimensions, list):
        required_dimensions = []
    dimension_states = evaluation.get("dimension_current_or_rebound", {})
    if not isinstance(dimension_states, dict):
        dimension_states = {}
    required_complete = bool(required_dimensions) and all(dimension in dimension_states for dimension in required_dimensions)
    checks.append(
        Check(
            "standing_rule",
            PASS if required_complete else FAIL,
            "standing rule declares and evaluates every required dimension"
            if required_complete
            else "standing rule is incomplete or missing dimension evaluations",
        )
    )

    mismatches = []
    bindings = current.get("bindings", {})
    if isinstance(bindings, dict):
        for dimension in required_dimensions:
            binding = bindings.get(dimension, {})
            if isinstance(binding, dict) and binding.get("matches_candidate") is False:
                mismatches.append(dimension)

    failed_dimensions = [dimension for dimension, state in dimension_states.items() if state is False]
    failed_dimensions = [dimension for dimension in required_dimensions if dimension in failed_dimensions]
    mismatches_complete = set(mismatches).issubset(set(failed_dimensions)) and set(failed_dimensions).issubset(set(required_dimensions))
    checks.append(
        Check(
            "commit_time_rebinding",
            PASS if failed_dimensions and mismatches_complete else FAIL,
            f"commit-time standing failed for: {', '.join(failed_dimensions)}"
            if failed_dimensions and mismatches_complete
            else "commit-time rebinding did not identify a deterministic standing failure",
        )
    )

    aggregate_false = evaluation.get("aggregate_standing") is False
    fail_closed = evaluation.get("result") == FAIL_CLOSED
    checks.append(
        Check(
            "standing_evaluation",
            PASS if aggregate_false and fail_closed else FAIL,
            "aggregate standing is false and result is FAIL_CLOSED"
            if aggregate_false and fail_closed
            else "standing evaluation does not resolve FAIL_CLOSED",
        )
    )

    receipt_valid = (
        receipt.get("receipt_type") == "commit_time_standing_receipt"
        and receipt.get("candidate_carries_authority") is False
        and receipt.get("commit_allowed") is False
        and receipt.get("decision") == FAIL_CLOSED
        and receipt.get("failed_dimensions") == failed_dimensions
    )
    checks.append(
        Check(
            "receipt",
            PASS if receipt_valid else FAIL,
            "receipt records non-authorizing candidate, failed dimensions, and FAIL_CLOSED"
            if receipt_valid
            else "receipt does not bind candidate non-authority, failed dimensions, and FAIL_CLOSED",
        )
    )

    return _status(checks), checks


def verify_artifact(artifact: dict[str, Any]) -> tuple[str, list[Check]]:
    if artifact.get("artifact_type") == "commitment_candidate_test":
        return verify_commitment_candidate_test(artifact)
    if "execution_trace" in artifact:
        return verify_pressure_trace(artifact)
    if "review_time" in artifact and "commit_time" in artifact:
        return verify_stale_state_proof(artifact)
    return FAIL, [Check("detect_artifact_type", FAIL, "unsupported SPE artifact type")]


# Backward-compatible name used by the first test file.
def verify_trace(trace: dict[str, Any]) -> tuple[str, list[Check]]:
    return verify_artifact(trace)


def render(status: str, checks: list[Check]) -> str:
    lines = [f"SPE RESULT: {status}", "", "Checks:"]
    for check in checks:
        lines.append(f"- {check.name}: {check.status} - {check.detail}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python spe/verify.py <artifact.json>", file=sys.stderr)
        return 2

    artifact_path = Path(argv[1])
    with artifact_path.open("r", encoding="utf-8") as handle:
        artifact = json.load(handle)

    status, checks = verify_artifact(artifact)
    print(render(status, checks))
    return 0 if status in {PASS, PARTIAL} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
