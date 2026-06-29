#!/usr/bin/env python3
"""Verify that Commitment Candidate manifest samples resolve through TT."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from spe.verify_manifest import artifact_from_transition_case


def _fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def verify_tt_manifest(path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    samples = manifest.get("samples", [])
    results = []
    for sample in samples:
        case = sample.get("transition_case")
        if not isinstance(case, dict):
            continue
        artifact = artifact_from_transition_case(case)
        candidate = artifact.get("commitment_candidate", {})
        receipt = artifact.get("receipt", {})
        tt_receipt = receipt.get("tt_transition_receipt", {})
        resolved = (
            candidate.get("tt_transition_id") == receipt.get("tt_transition_id") == tt_receipt.get("transition_id")
            and tt_receipt.get("canonical_source") == "Admissible-Existence/TT"
            and tt_receipt.get("implementation_status") == "implemented"
            and tt_receipt.get("resolved") is True
            and isinstance(candidate.get("tt_code_ref"), str)
        )
        results.append({
            "test_id": artifact.get("test_id"),
            "tt_transition_id": candidate.get("tt_transition_id"),
            "tt_code_ref": candidate.get("tt_code_ref"),
            "tt_receipt_decision": tt_receipt.get("decision"),
            "resolved": resolved,
        })
    all_resolved = bool(results) and all(item["resolved"] for item in results)
    return {
        "manifest_id": manifest.get("manifest_id"),
        "sample_count": len(results),
        "spe_tt_binding_result": "PASS" if all_resolved else "FAIL",
        "samples": results,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python spe/verify_tt_manifest.py <manifest.json>", file=sys.stderr)
        return 2
    report = verify_tt_manifest(Path(argv[1]))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["spe_tt_binding_result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
