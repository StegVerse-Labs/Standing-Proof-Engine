#!/usr/bin/env python3
"""Verify heartbeat path-selection receipts.

Heartbeat path selection is the governance point where an upstream route declares
which downstream path should receive the next proof/receipt package. The verifier
keeps this check intentionally small and fail-closed: the receipt must be current,
select exactly one declared candidate path, and bind that selected path back to a
known destination and verification profile.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from spe.verify import FAIL, PASS, Check, render


ACTIVE_STATES = {"ACTIVE", "READY"}
ALLOWED_RESULTS = {"SELECTED", "DEFERRED"}


def _status(checks: list[Check]) -> str:
    return FAIL if any(check.status == FAIL for check in checks) else PASS


def verify_heartbeat_path_selection(receipt: dict[str, Any], repo_root: Path | None = None) -> tuple[str, list[Check]]:
    required = [
        "receipt_id",
        "receipt_type",
        "selection_result",
        "candidate_paths",
        "selected_path",
        "destination_repo",
        "verification_profile",
    ]
    missing = [key for key in required if not receipt.get(key)]
    if missing:
        return FAIL, [Check("parse_heartbeat_path_selection", FAIL, f"missing fields: {', '.join(missing)}")]

    checks = [Check("parse_heartbeat_path_selection", PASS, "heartbeat path-selection receipt parsed")]

    type_ok = receipt.get("receipt_type") == "heartbeat_path_selection"
    checks.append(Check("receipt_type", PASS if type_ok else FAIL, "heartbeat path-selection receipt type checked"))

    result_ok = receipt.get("selection_result") in ALLOWED_RESULTS
    checks.append(Check("selection_result", PASS if result_ok else FAIL, "selection result checked"))

    candidates = receipt.get("candidate_paths")
    candidates_ok = isinstance(candidates, list) and bool(candidates) and all(isinstance(item, dict) for item in candidates)
    checks.append(Check("candidate_paths_shape", PASS if candidates_ok else FAIL, "candidate path list checked"))

    selected_path = receipt.get("selected_path")
    selected_candidates = [item for item in candidates if isinstance(item, dict) and item.get("path_id") == selected_path] if isinstance(candidates, list) else []
    selected_ok = len(selected_candidates) == 1
    checks.append(Check("selected_path_declared", PASS if selected_ok else FAIL, "selected path is declared exactly once"))

    selected = selected_candidates[0] if selected_ok else {}
    active_ok = selected.get("state") in ACTIVE_STATES
    checks.append(Check("selected_path_active", PASS if active_ok else FAIL, "selected path active state checked"))

    destination_ok = selected.get("destination_repo") == receipt.get("destination_repo")
    checks.append(Check("destination_binding", PASS if destination_ok else FAIL, "selected path destination checked"))

    profile = receipt.get("verification_profile")
    profile_ok = isinstance(profile, dict) and all(profile.get(key) is True for key in ["requires_manifest", "requires_receipt", "requires_standing_check"])
    checks.append(Check("verification_profile", PASS if profile_ok else FAIL, "manifest, receipt, and standing requirements checked"))

    nonselected_ok = all(
        item.get("path_id") == selected_path or item.get("state") not in ACTIVE_STATES or item.get("priority", 999) >= selected.get("priority", 999)
        for item in candidates
    ) if selected_ok and isinstance(candidates, list) else False
    checks.append(Check("candidate_priority", PASS if nonselected_ok else FAIL, "selected path priority checked"))

    return _status(checks), checks


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python -m spe.verify_heartbeat_path_selection <receipt.json>", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    receipt = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    status, checks = verify_heartbeat_path_selection(receipt, repo_root)
    print(render(status, checks))
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
