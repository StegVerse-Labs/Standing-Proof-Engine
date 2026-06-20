#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.verify import FAIL, PASS, Check, render
from spe.verify_manifest import verify_manifest


def verify_sdk_intake(receipt, repo_root):
    required = [
        "receipt_id",
        "receipt_type",
        "origin_repo",
        "destination_repo",
        "route",
        "artifact_package",
        "spe_route_package_id",
    ]
    missing = [key for key in required if not receipt.get(key)]
    if missing:
        return FAIL, [Check("parse_sdk_intake", FAIL, f"missing fields: {', '.join(missing)}")]

    checks = [Check("parse_sdk_intake", PASS, "SDK intake receipt parsed")]

    route_ok = (
        receipt.get("receipt_type") == "sdk_intake_receipt"
        and receipt.get("route") == "standing_proof_engine"
        and receipt.get("destination_repo") == "StegVerse-Labs/Standing-Proof-Engine"
    )
    checks.append(
        Check(
            "route_declaration",
            PASS if route_ok else FAIL,
            "receipt declares Standing-Proof-Engine route" if route_ok else "route declaration is not valid",
        )
    )

    handoff_ok = all(
        receipt.get(key) is True
        for key in ["ingested", "manifest_bound", "receipt_bound", "route_declared", "spe_evaluation_required"]
    )
    checks.append(
        Check(
            "handoff_flags",
            PASS if handoff_ok else FAIL,
            "handoff flags are all true" if handoff_ok else "handoff flags are incomplete",
        )
    )

    manifest_path = repo_root / receipt["artifact_package"]
    manifest_status, manifest_report = verify_manifest(manifest_path)
    expected_status = receipt.get("expected_package_status")
    manifest_ok = manifest_status == expected_status
    checks.append(
        Check(
            "manifest_result_binding",
            PASS if manifest_ok else FAIL,
            f"manifest status {manifest_status} matched expected {expected_status}"
            if manifest_ok
            else f"manifest status {manifest_status} did not match expected {expected_status}",
        )
    )

    sample_count = len(receipt.get("declared_samples", []))
    manifest_count = manifest_report.get("sample_count")
    samples_ok = sample_count == manifest_count
    checks.append(
        Check(
            "sample_count_binding",
            PASS if samples_ok else FAIL,
            f"receipt and manifest declare {sample_count} samples"
            if samples_ok
            else f"receipt declares {sample_count} samples but manifest declares {manifest_count}",
        )
    )

    if any(check.status == FAIL for check in checks):
        return FAIL, checks
    return PASS, checks


def main(argv):
    if len(argv) != 2:
        print("usage: python spe/verify_sdk_intake.py <sdk_intake_receipt.json>", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    receipt = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    status, checks = verify_sdk_intake(receipt, repo_root)
    print(render(status, checks))
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
