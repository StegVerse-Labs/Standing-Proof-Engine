#!/usr/bin/env python3
"""Verify factor-bound heartbeat path-selection receipts."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from spe.heartbeat_path_selection import factor_bound_receipt
from spe.verify import FAIL, PASS, Check, render


def verify_heartbeat_path_selection(artifact: dict[str, Any]) -> tuple[str, list[Check]]:
    checks: list[Check] = []

    if artifact.get("receipt_type") != "factor_bound_path_selection":
        return FAIL, [Check("receipt_type", FAIL, "expected factor_bound_path_selection")]
    checks.append(Check("receipt_type", PASS, "factor-bound path-selection receipt declared"))

    vector = artifact.get("state_vector")
    if not isinstance(vector, dict):
        return FAIL, checks + [Check("state_vector", FAIL, "state_vector missing or invalid")]
    checks.append(Check("state_vector", PASS, "state vector present"))

    computed = factor_bound_receipt(vector)

    expected_degradation = artifact.get("expected_degradation_state")
    if computed.get("degradation_state") == expected_degradation:
        checks.append(Check("degradation_state", PASS, f"{expected_degradation} matched"))
    else:
        checks.append(Check("degradation_state", FAIL, f"expected {expected_degradation}, got {computed.get('degradation_state')}"))

    expected_path = artifact.get("expected_selected_path")
    if computed.get("selected_path") == expected_path:
        checks.append(Check("selected_path", PASS, f"{expected_path} matched"))
    else:
        checks.append(Check("selected_path", FAIL, f"expected {expected_path}, got {computed.get('selected_path')}"))

    expected_rejected = artifact.get("expected_rejected_paths", {})
    computed_rejected = computed.get("rejected_paths", {})
    if isinstance(expected_rejected, dict) and all(computed_rejected.get(path) == reason for path, reason in expected_rejected.items()):
        checks.append(Check("rejected_paths", PASS, "expected rejected paths matched"))
    else:
        checks.append(Check("rejected_paths", FAIL, "expected rejected paths did not match computed receipt"))

    recorded = artifact.get("recorded_factors", [])
    if isinstance(recorded, list) and all(isinstance(item, str) and item in vector for item in recorded):
        checks.append(Check("recorded_factors", PASS, "recorded factors present in state vector"))
    else:
        checks.append(Check("recorded_factors", FAIL, "recorded factors missing from state vector"))

    if any(check.status == FAIL for check in checks):
        return FAIL, checks
    return PASS, checks


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python -m spe.verify_heartbeat_path_selection <artifact.json>", file=sys.stderr)
        return 2

    artifact = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    status, checks = verify_heartbeat_path_selection(artifact)
    print(render(status, checks))
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
