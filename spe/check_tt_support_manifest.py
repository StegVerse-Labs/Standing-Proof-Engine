#!/usr/bin/env python3
"""Check SPE downstream TT support-family snapshot."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUPPORT = ROOT / "data" / "tt" / "tt_support_transition_authority_manifest.json"
EXPECTED_FAMILIES = {
    "Validation",
    "Classification",
    "Boundary",
    "Installation",
    "Execution",
    "Commit",
    "Quarantine/Failure",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    data = json.loads(SUPPORT.read_text(encoding="utf-8"))
    if data.get("canonical_source") != "Admissible-Existence/TT":
        fail("canonical source mismatch")
    entries = data.get("entries", [])
    if not isinstance(entries, list) or not entries:
        fail("entries must be a non-empty list")

    seen_ids = set()
    seen_families = set()
    for row in entries:
        if not isinstance(row, list) or len(row) != 6:
            fail("each entry must contain transition id, name, family, module, function, and required field")
        transition_id, transition_name, family, module, function_name, required_field = row
        if not str(transition_id).startswith("T-"):
            fail(f"invalid transition id: {transition_id}")
        if transition_id in seen_ids:
            fail(f"duplicate transition id: {transition_id}")
        if not all(isinstance(value, str) and value for value in row):
            fail(f"invalid entry values for {transition_id}")
        seen_ids.add(transition_id)
        seen_families.add(family)
        code_ref = f"engine/transition_handlers/{module}.py::{function_name}"
        fixture_ref = f"fixtures/transition-elements/{str(transition_id).lower()}.{transition_name.lower().replace('/', '').replace(' ', '-')}.json"
        if "::" not in code_ref or not fixture_ref.endswith(".json") or not required_field:
            fail(f"invalid binding for {transition_id}")

    missing_families = sorted(EXPECTED_FAMILIES - seen_families)
    if missing_families:
        fail("missing support families: " + ", ".join(missing_families))

    print(f"PASS: SPE support TT snapshot covers {len(seen_ids)} transitions across {len(seen_families)} families.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
