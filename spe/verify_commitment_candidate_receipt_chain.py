#!/usr/bin/env python3
"""Verify TT-bound Commitment Candidate receipt chains."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from spe.verify_manifest import artifact_from_transition_case

ROOT = Path(__file__).resolve().parents[1]


def _get(data: dict[str, Any], dotted: str) -> Any:
    value: Any = data
    for part in dotted.split("."):
        if not isinstance(value, dict):
            return None
        value = value.get(part)
    return value


def _fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def verify_receipt_chain(expectation_path: Path) -> dict[str, Any]:
    expectation = json.loads(expectation_path.read_text(encoding="utf-8"))
    manifest_path = ROOT / expectation["manifest_path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    samples = []

    for sample in manifest.get("samples", []):
        case = sample.get("transition_case")
        if not isinstance(case, dict):
            continue
        artifact = artifact_from_transition_case(case)
        missing_chain = [field for field in expectation["required_chain_fields"] if _get(artifact, field) is None]
        tt_receipt = artifact.get("receipt", {}).get("tt_transition_receipt", {})
        missing_tt = [field for field in expectation["required_tt_receipt_fields"] if not isinstance(tt_receipt, dict) or field not in tt_receipt]
        aligned = (
            artifact.get("historical_review", {}).get("tt_transition_id")
            == artifact.get("commitment_candidate", {}).get("tt_transition_id")
            == artifact.get("receipt", {}).get("tt_transition_id")
            == tt_receipt.get("transition_id")
        )
        final_decision_ok = artifact.get("receipt", {}).get("decision") == expectation["expected_final_decision"]
        tt_receipt_ok = (
            tt_receipt.get("canonical_source") == expectation["expected_tt_source"]
            and tt_receipt.get("decision") == expectation["expected_tt_decision"]
            and tt_receipt.get("implementation_status") == "implemented"
            and tt_receipt.get("resolved") is True
        )
        ok = not missing_chain and not missing_tt and aligned and final_decision_ok and tt_receipt_ok
        samples.append({
            "test_id": artifact.get("test_id"),
            "tt_transition_id": artifact.get("receipt", {}).get("tt_transition_id"),
            "tt_code_ref": artifact.get("commitment_candidate", {}).get("tt_code_ref"),
            "final_decision": artifact.get("receipt", {}).get("decision"),
            "tt_receipt_decision": tt_receipt.get("decision"),
            "missing_chain_fields": missing_chain,
            "missing_tt_receipt_fields": missing_tt,
            "aligned": aligned,
            "receipt_chain_valid": ok,
        })

    expected_count = expectation.get("expected_sample_count")
    count_ok = len(samples) == expected_count
    result = count_ok and bool(samples) and all(sample["receipt_chain_valid"] for sample in samples)
    return {
        "expectation_id": expectation.get("expectation_id"),
        "manifest_path": expectation.get("manifest_path"),
        "sample_count": len(samples),
        "expected_sample_count": expected_count,
        "spe_commitment_candidate_receipt_chain_result": "PASS" if result else "FAIL",
        "samples": samples,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python spe/verify_commitment_candidate_receipt_chain.py <expectation.json>", file=sys.stderr)
        return 2
    report = verify_receipt_chain(Path(argv[1]))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["spe_commitment_candidate_receipt_chain_result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
