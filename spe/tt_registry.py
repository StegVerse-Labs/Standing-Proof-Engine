#!/usr/bin/env python3
"""TT registry consumer helpers for Standing-Proof-Engine.

SPE consumes a checked-in downstream TT authority manifest. The canonical source
remains Admissible-Existence/TT; this module only validates that SPE artifacts
reference known, implemented TT transition entries before standing is evaluated.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_MANIFEST = ROOT / "data" / "tt" / "tt_transition_authority_manifest.json"


@dataclass(frozen=True)
class TTResolution:
    transition_id: str | None
    transition_name: str | None
    code_ref: str | None
    implementation_status: str | None
    fixture_ref: str | None
    receipt_schema_ref: str | None
    required_field: str | None
    resolved: bool
    reason: str

    def as_receipt(self) -> dict[str, Any]:
        return {
            "receipt_type": "tt_transition_resolution_receipt",
            "canonical_source": "Admissible-Existence/TT",
            "transition_id": self.transition_id,
            "transition_name": self.transition_name,
            "code_ref": self.code_ref,
            "implementation_status": self.implementation_status,
            "fixture_ref": self.fixture_ref,
            "receipt_schema_ref": self.receipt_schema_ref,
            "required_field": self.required_field,
            "resolved": self.resolved,
            "decision": "ALLOW" if self.resolved else "FAIL_CLOSED",
            "reason": self.reason,
        }


def load_authority_manifest(path: Path = AUTHORITY_MANIFEST) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_transition(reference: str | None, manifest: dict[str, Any] | None = None) -> TTResolution:
    if manifest is None:
        manifest = load_authority_manifest()
    if not reference:
        return TTResolution(None, None, None, None, None, None, None, False, "Missing TT transition reference.")

    aliases = manifest.get("legacy_transition_cell_aliases", {})
    transition_id = aliases.get(reference, reference)
    transitions = manifest.get("transition_requirements", {})
    entry = transitions.get(transition_id)
    if not isinstance(entry, dict):
        return TTResolution(transition_id, None, None, None, None, None, None, False, "Unknown TT transition reference.")

    required_fields = ["transition_name", "code_ref", "implementation_status", "fixture_ref", "receipt_schema_ref"]
    missing = [field for field in required_fields if not entry.get(field)]
    if missing:
        return TTResolution(
            transition_id,
            entry.get("transition_name"),
            entry.get("code_ref"),
            entry.get("implementation_status"),
            entry.get("fixture_ref"),
            entry.get("receipt_schema_ref"),
            entry.get("required_field"),
            False,
            "TT transition entry is incomplete: " + ", ".join(missing),
        )

    if entry.get("implementation_status") != "implemented":
        return TTResolution(
            transition_id,
            entry.get("transition_name"),
            entry.get("code_ref"),
            entry.get("implementation_status"),
            entry.get("fixture_ref"),
            entry.get("receipt_schema_ref"),
            entry.get("required_field"),
            False,
            "TT transition handler is not implemented.",
        )

    return TTResolution(
        transition_id,
        entry.get("transition_name"),
        entry.get("code_ref"),
        entry.get("implementation_status"),
        entry.get("fixture_ref"),
        entry.get("receipt_schema_ref"),
        entry.get("required_field"),
        True,
        "TT transition resolved to an implemented canonical handler reference.",
    )
