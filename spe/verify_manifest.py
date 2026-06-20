#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Any

from spe.result_export import result_dict
from spe.verify import FAIL, PARTIAL, PASS, verify_artifact


def governance_result(artifact: dict[str, Any]) -> str | None:
    receipt = artifact.get("receipt", {})
    if isinstance(receipt, dict) and isinstance(receipt.get("decision"), str):
        return receipt["decision"]
    if isinstance(artifact.get("final_decision"), str):
        return artifact["final_decision"]
    return None


def verify_manifest(manifest_path: Path) -> tuple[str, dict[str, Any]]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    root = manifest_path.resolve().parents[1]
    sample_results = []
    manifest_status = PASS

    for sample in manifest.get("samples", []):
        sample_path = root / sample["path"]
        artifact = json.loads(sample_path.read_text(encoding="utf-8"))
        status, checks = verify_artifact(artifact)
        observed_result = governance_result(artifact)
        expected_spe = sample.get("expected_spe_result")
        expected_result = sample.get("expected_governance_result")
        matches = status == expected_spe and observed_result == expected_result

        if status == FAIL or not matches:
            manifest_status = FAIL
        elif status == PARTIAL and manifest_status == PASS:
            manifest_status = PARTIAL

        exported = result_dict(artifact, status, checks)
        sample_results.append({
            "path": sample["path"],
            "route": sample.get("route"),
            "spe_result": status,
            "expected_spe_result": expected_spe,
            "governance_result": observed_result,
            "expected_governance_result": expected_result,
            "matches_expectation": matches,
            "artifact_hash": exported["hashes"]["artifact"],
            "check_count": len(checks),
        })

    report = {
        "manifest_id": manifest.get("manifest_id"),
        "spe_result": manifest_status,
        "sample_count": len(sample_results),
        "samples": sample_results,
    }
    return manifest_status, report


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python spe/verify_manifest.py <manifest.json>", file=sys.stderr)
        return 2
    status, report = verify_manifest(Path(argv[1]))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if status in {PASS, PARTIAL} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
