import hashlib
import json
from dataclasses import asdict
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def artifact_type(artifact: dict[str, Any]) -> str:
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


def result_dict(artifact: dict[str, Any], status: str, checks: list[Any]) -> dict[str, Any]:
    return {
        "spe_result": status,
        "artifact_type": artifact_type(artifact),
        "hashes": section_hashes(artifact),
        "checks": [asdict(check) for check in checks],
    }


def render_json(artifact: dict[str, Any], status: str, checks: list[Any]) -> str:
    return json.dumps(result_dict(artifact, status, checks), indent=2, sort_keys=True)
