from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

SPE_SDK_INTAKE_SCHEMA_VERSION = "stegverse.spe.sdk_commitment_intake.v0.1"
ALLOWED_RESULTS = {"ALLOW", "DENY", "FAIL_CLOSED"}


class SDKCommitmentIntakeError(ValueError):
    """Raised when an SDK commitment envelope cannot enter SPE evaluation."""


def _stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _stable_hash(value: Any) -> str:
    return hashlib.sha256(_stable_json(value).encode("utf-8")).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SDKCommitmentIntakeError(message)


def validate_sdk_commitment_envelope(envelope: Mapping[str, Any]) -> None:
    """Validate a transport-neutral SDK envelope without deciding standing."""

    _require(
        envelope.get("schema_version") == "stegverse.sdk.spe_commitment_intake.v0.1",
        "unsupported SDK commitment intake schema",
    )
    _require(
        envelope.get("destination_repo") == "StegVerse-Labs/Standing-Proof-Engine",
        "destination_repo mismatch",
    )
    _require(
        envelope.get("route_purpose") == "FRESH_STANDING_DETERMINATION",
        "route_purpose mismatch",
    )
    _require(envelope.get("receipt_required") is True, "receipt_required must be true")
    _require(envelope.get("expected_result") == ["ALLOW", "DENY", "FAIL_CLOSED"], "unexpected result contract")

    candidate = envelope.get("candidate")
    _require(isinstance(candidate, Mapping), "candidate must be an object")
    _require(candidate.get("candidate_type") == "COMMITMENT_CANDIDATE", "candidate_type mismatch")
    _require(candidate.get("authorizing") is False, "candidate must be non-authorizing")
    _require(candidate.get("inherits_review_authority") is False, "candidate must not inherit review authority")
    _require(candidate.get("implies_standing") is False, "candidate must not imply standing")
    _require(
        candidate.get("requires_fresh_standing_determination") is True,
        "candidate must require fresh standing determination",
    )

    package_id = str(envelope.get("package_id", ""))
    _require(bool(package_id), "package_id is required")
    _require(candidate.get("package_id") == package_id, "candidate package_id mismatch")
    _require(candidate.get("transition_id") == envelope.get("transition_id"), "transition_id mismatch")
    _require(candidate.get("run_id") == envelope.get("run_id"), "run_id mismatch")

    candidate_core = dict(candidate)
    claimed_candidate_hash = candidate_core.pop("candidate_hash", None)
    _require(bool(claimed_candidate_hash), "candidate_hash is required")
    _require(_stable_hash(candidate_core) == claimed_candidate_hash, "candidate_hash mismatch")
    _require(envelope.get("candidate_hash") == claimed_candidate_hash, "envelope candidate_hash mismatch")

    envelope_core = dict(envelope)
    claimed_envelope_hash = envelope_core.pop("envelope_hash", None)
    _require(bool(claimed_envelope_hash), "envelope_hash is required")
    _require(_stable_hash(envelope_core) == claimed_envelope_hash, "envelope_hash mismatch")

    authority = envelope.get("authority", {})
    _require(authority.get("sdk_authorizing") is False, "SDK must remain non-authorizing")
    _require(authority.get("execution_authority_requested") is False, "execution authority may not be requested")
    _require(
        authority.get("fresh_standing_determination_required") is True,
        "fresh standing determination must be required",
    )


def emit_spe_standing_receipt(
    envelope: Mapping[str, Any],
    *,
    result: str,
    policy_refs: list[str] | None = None,
    delegation_refs: list[str] | None = None,
    evidence_refs: list[str] | None = None,
    reasons: list[str] | None = None,
) -> dict[str, Any]:
    """Emit a deterministic SPE result receipt after external standing evaluation.

    The caller supplies the bounded standing result. This function validates the
    intake envelope and binds the result to its hashes; it does not execute the action.
    """

    validate_sdk_commitment_envelope(envelope)
    normalized_result = result.upper().strip()
    _require(normalized_result in ALLOWED_RESULTS, "result must be ALLOW, DENY, or FAIL_CLOSED")

    receipt_core = {
        "schema_version": SPE_SDK_INTAKE_SCHEMA_VERSION,
        "receipt_type": "SPE_STANDING_DETERMINATION",
        "source_repo": "StegVerse-org/StegVerse-SDK",
        "destination_repo": "StegVerse-Labs/Standing-Proof-Engine",
        "package_id": envelope["package_id"],
        "transition_id": envelope["transition_id"],
        "run_id": envelope["run_id"],
        "candidate_hash": envelope["candidate_hash"],
        "envelope_hash": envelope["envelope_hash"],
        "standing_result": normalized_result,
        "policy_refs": policy_refs or [],
        "delegation_refs": delegation_refs or [],
        "evidence_refs": evidence_refs or [],
        "reasons": reasons or [],
        "execution_authorized": False,
        "execution_performed": False,
        "master_record_installed": False,
        "next_boundary": "GOVERNED_EXECUTION_AUTHORITY" if normalized_result == "ALLOW" else None,
    }
    return {**receipt_core, "receipt_hash": _stable_hash(receipt_core)}


__all__ = [
    "ALLOWED_RESULTS",
    "SDKCommitmentIntakeError",
    "SPE_SDK_INTAKE_SCHEMA_VERSION",
    "emit_spe_standing_receipt",
    "validate_sdk_commitment_envelope",
]
