import hashlib
import json
from dataclasses import asdict
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def artifact_type(artifact: dict[str, Any]) -> str:
    declared_type = artifact.get("artifact_type")
    if isinstance(declared_type, str):
        return declared_type
    if artifact.get("receipt_type") == "sdk_intake_receipt":
        return "sdk_intake_receipt"
    if "execution_trace" in artifact:
        return "pressure_trace"
    if "review_time" in artifact and "commit_time" in artifact:
        return "stale_state_proof"
    return "unsupported"


def section_hashes(artifact: dict[str, Any]) -> dict[str, str]:
    hashes = {"artifact": canonical_sha256(artifact)}
    for key, value in artifact.items():
        if isinstance(value, (dict, list)):
            hashes[key] = canonical_sha256(value)
    return hashes


def governance_summary(artifact: dict[str, Any]) -> dict[str, Any]:
    receipt = artifact.get("receipt", {})
    evaluation = artifact.get("standing_evaluation", {})
    summary: dict[str, Any] = {}

    for key in [
        "artifact_id",
        "title",
        "receipt_id",
        "receipt_type",
        "origin_repo",
        "destination_repo",
        "route",
        "artifact_package",
        "spe_route_package_id",
        "expected_package_status",
    ]:
        if key in artifact:
            summary[key] = artifact[key]

    if isinstance(receipt, dict):
        for key in ["receipt_id", "decision", "commit_allowed", "prior_review_replayable"]:
            if key in receipt:
                summary[key] = receipt[key]

    if isinstance(evaluation, dict):
        for key in ["aggregate_standing", "result"]:
            if key in evaluation:
                summary[key] = evaluation[key]

    return summary


def result_dict(artifact: dict[str, Any], status: str, checks: list[Any]) -> dict[str, Any]:
    return {
        "spe_result": status,
        "artifact_type": artifact_type(artifact),
        "governance_summary": governance_summary(artifact),
        "hashes": section_hashes(artifact),
        "checks": [asdict(check) for check in checks],
    }


def render_json(artifact: dict[str, Any], status: str, checks: list[Any]) -> str:
    return json.dumps(result_dict(artifact, status, checks), indent=2, sort_keys=True)
