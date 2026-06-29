#!/usr/bin/env python3
"""Check SPE downstream TT authority snapshot coverage."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "tt" / "tt_transition_authority_manifest.json"
SAMPLE = ROOT / "samples" / "tt_transition_authority_manifest_check.json"

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
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    sample = json.loads(SAMPLE.read_text(encoding="utf-8"))

    if manifest.get("schema") != sample.get("expected_schema"):
        fail("schema mismatch")
    if manifest.get("canonical_source") != sample.get("expected_canonical_source"):
        fail("canonical source mismatch")

    transitions = manifest.get("transition_requirements", {})
    if not isinstance(transitions, dict):
        fail("transition_requirements must be an object")

    missing_ids = [tid for tid in sample.get("required_transition_ids", []) if tid not in transitions]
    if missing_ids:
        fail("missing transition ids: " + ", ".join(missing_ids))

    for transition_id in sample.get("required_transition_ids", []):
        entry = transitions[transition_id]
        missing_fields = sorted(REQUIRED_ENTRY_FIELDS - set(entry))
        if missing_fields:
            fail(f"{transition_id} missing fields: " + ", ".join(missing_fields))
        if entry.get("implementation_status") != sample.get("expected_implementation_status"):
            fail(f"{transition_id} is not implemented")
        if entry.get("fail_closed_when_missing") is not True:
            fail(f"{transition_id} must fail closed when required field is missing")

    print("PASS: SPE TT authority manifest covers required consequence and reconstruction transitions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
