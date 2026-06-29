#!/usr/bin/env python3
"""Verify SPE can consume a full TT transition snapshot."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from spe.tt_full_snapshot import load_full_snapshot

ROOT = Path(__file__).resolve().parents[1]
EXPECTATION = ROOT / "samples" / "tt_full_snapshot_expectation.json"
REQUIRED_ENTRY_FIELDS = {
    "transition_name",
    "transition_family",
    "code_ref",
    "implementation_status",
    "fixture_ref",
    "receipt_schema_ref",
    "required_field",
    "fail_closed_when_missing",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    expectation = json.loads(EXPECTATION.read_text(encoding="utf-8"))
    snapshot = load_full_snapshot()
    if snapshot.get("canonical_source") != expectation.get("expected_canonical_source"):
        fail("canonical source mismatch")
    if snapshot.get("transition_count") != expectation.get("expected_transition_count"):
        fail(f"transition count mismatch: {snapshot.get('transition_count')}")

    transitions = snapshot.get("transition_requirements", {})
    missing_ids = [tid for tid in expectation.get("required_transition_ids", []) if tid not in transitions]
    if missing_ids:
        fail("missing transition ids: " + ", ".join(missing_ids))

    families = {entry.get("transition_family") for entry in transitions.values() if isinstance(entry, dict)}
    missing_families = sorted(set(expectation.get("required_families", [])) - families)
    if missing_families:
        fail("missing families: " + ", ".join(missing_families))

    for transition_id, entry in transitions.items():
        missing_fields = sorted(REQUIRED_ENTRY_FIELDS - set(entry))
        if missing_fields:
            fail(f"{transition_id} missing fields: " + ", ".join(missing_fields))
        if entry.get("implementation_status") != "implemented":
            fail(f"{transition_id} not implemented")
        if entry.get("fail_closed_when_missing") is not True:
            fail(f"{transition_id} missing fail-closed rule")

    print("PASS: SPE consumes a full TT transition snapshot with all expected families and transitions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
