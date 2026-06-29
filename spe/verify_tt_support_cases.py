#!/usr/bin/env python3
"""Verify runtime support-family TT cases for SPE."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SUPPORT = ROOT / "data" / "tt" / "tt_support_transition_authority_manifest.json"


DECISION_BY_TRANSITION_AND_VALUE = {
    "T-024": {True: "QUARANTINE", False: "ALLOW"},
    "T-041": {"low": "ALLOW", "medium": "ALLOW", "high": "REPAIR_REQUIRED", "critical": "QUARANTINE", "unknown": "QUARANTINE"},
    "T-107": {True: "QUARANTINE", False: "ALLOW"},
    "T-260": {True: "FAIL_CLOSED", False: "DENY"},
    "T-261": {True: "QUARANTINE", False: "ALLOW"},
    "T-262": {True: "REPAIR_REQUIRED", False: "ALLOW"},
    "T-265": {True: "ALLOW", False: "REPAIR_REQUIRED"},
}


def _fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def _entries() -> dict[str, dict[str, str]]:
    data = json.loads(SUPPORT.read_text(encoding="utf-8"))
    entries: dict[str, dict[str, str]] = {}
    for row in data.get("entries", []):
        transition_id, transition_name, family, module, function_name, required_field = row
        entries[transition_id] = {
            "transition_name": transition_name,
            "transition_family": family,
            "code_ref": f"engine/transition_handlers/{module}.py::{function_name}",
            "required_field": required_field,
        }
    return entries


def _decision(transition_id: str, value: Any) -> str:
    special = DECISION_BY_TRANSITION_AND_VALUE.get(transition_id)
    if special is not None:
        normalized = value.lower() if isinstance(value, str) else value
        return special.get(normalized, "QUARANTINE")
    if value is True:
        return "ALLOW"
    if value is False:
        return "DENY"
    if isinstance(value, str) and value:
        return "ALLOW"
    return "FAIL_CLOSED"


def verify_cases(path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    entries = _entries()
    results = []
    for sample in manifest.get("samples", []):
        transition_id = sample.get("tt_transition_id")
        entry = entries.get(transition_id)
        if not entry:
            results.append({"test_id": sample.get("test_id"), "resolved": False, "decision": "FAIL_CLOSED"})
            continue
        field_matches = sample.get("field") == entry.get("required_field")
        decision = _decision(transition_id, sample.get("value"))
        matches = field_matches and decision == sample.get("expected_decision")
        results.append({
            "test_id": sample.get("test_id"),
            "tt_transition_id": transition_id,
            "transition_name": entry.get("transition_name"),
            "tt_code_ref": entry.get("code_ref"),
            "required_field": entry.get("required_field"),
            "observed_decision": decision,
            "expected_decision": sample.get("expected_decision"),
            "resolved": matches,
        })
    return {
        "manifest_id": manifest.get("manifest_id"),
        "sample_count": len(results),
        "spe_tt_support_case_result": "PASS" if results and all(item["resolved"] for item in results) else "FAIL",
        "samples": results,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python spe/verify_tt_support_cases.py <manifest.json>", file=sys.stderr)
        return 2
    report = verify_cases(Path(argv[1]))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["spe_tt_support_case_result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
