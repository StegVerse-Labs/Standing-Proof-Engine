#!/usr/bin/env python3
"""Standing-Proof-Engine verifier.

This first verifier intentionally stays small. It evaluates one trace artifact and
returns PASS, PARTIAL, or FAIL with reconstructable reasons.
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


def verify_trace(trace: dict[str, Any]) -> tuple[str, list[Check]]:
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


def render(status: str, checks: list[Check]) -> str:
    lines = [f"SPE RESULT: {status}", "", "Checks:"]
    for check in checks:
        lines.append(f"- {check.name}: {check.status} - {check.detail}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python spe/verify.py <trace.json>", file=sys.stderr)
        return 2

    trace_path = Path(argv[1])
    with trace_path.open("r", encoding="utf-8") as handle:
        trace = json.load(handle)

    status, checks = verify_trace(trace)
    print(render(status, checks))
    return 0 if status in {PASS, PARTIAL} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
