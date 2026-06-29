#!/usr/bin/env python3
"""Build a full SPE-consumable TT transition snapshot.

The canonical source remains Admissible-Existence/TT. This module merges the
SPE downstream consequence/reconstruction snapshot with the support-family
snapshot so runtime consumers can resolve one complete transition map.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY = ROOT / "data" / "tt" / "tt_transition_authority_manifest.json"
SUPPORT = ROOT / "data" / "tt" / "tt_support_transition_authority_manifest.json"


def _slug(value: str) -> str:
    return value.lower().replace("/", "").replace(" ", "-")


def _support_entry(row: list[str]) -> tuple[str, dict[str, Any]]:
    transition_id, transition_name, transition_family, module, function_name, required_field = row
    return transition_id, {
        "transition_name": transition_name,
        "transition_family": transition_family,
        "code_ref": f"engine/transition_handlers/{module}.py::{function_name}",
        "implementation_status": "implemented",
        "fixture_ref": f"fixtures/transition-elements/{transition_id.lower()}.{_slug(transition_name)}.json",
        "receipt_schema_ref": "schemas/transition-element-receipt.schema.json",
        "required_field": required_field,
        "fail_closed_when_missing": True,
    }


def load_full_snapshot() -> dict[str, Any]:
    authority = json.loads(AUTHORITY.read_text(encoding="utf-8"))
    support = json.loads(SUPPORT.read_text(encoding="utf-8"))
    transitions: dict[str, dict[str, Any]] = {}
    transitions.update(authority.get("transition_requirements", {}))
    for row in support.get("entries", []):
        transition_id, entry = _support_entry(row)
        transitions[transition_id] = entry
    return {
        "schema": "spe_tt_full_transition_snapshot.v0.1",
        "canonical_source": "Admissible-Existence/TT",
        "source_manifests": [
            "data/tt/tt_transition_authority_manifest.json",
            "data/tt/tt_support_transition_authority_manifest.json",
        ],
        "transition_count": len(transitions),
        "transition_requirements": dict(sorted(transitions.items())),
        "non_claims": [
            "This full snapshot is a downstream consumer view, not the canonical TT source.",
            "This full snapshot does not redefine TT semantics.",
            "This full snapshot does not grant commit-time permission.",
        ],
    }


def main() -> int:
    print(json.dumps(load_full_snapshot(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
