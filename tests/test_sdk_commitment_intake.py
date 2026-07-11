from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from spe.sdk_commitment_intake import (
    SDKCommitmentIntakeError,
    emit_spe_standing_receipt,
    validate_sdk_commitment_envelope,
)

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_ENVELOPE = ROOT / "samples" / "sdk_commitment_intake_envelope_001.json"
CANONICAL_RECEIPTS = ROOT / "samples" / "sdk_commitment_standing_receipts_001.json"


def stable_hash(value: object) -> str:
    rendered = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_envelope() -> dict:
    candidate_core = {
        "package_id": "transition.sdk.spe.test",
        "candidate_type": "COMMITMENT_CANDIDATE",
        "transition_id": "transition.sdk.spe.test",
        "run_id": "run-sdk-spe-test",
        "authorizing": False,
        "inherits_review_authority": False,
        "implies_standing": False,
        "requires_fresh_standing_determination": True,
        "bounded_scope": {"repository": "StegVerse-org/StegVerse-SDK"},
        "actor": "actor:test",
        "target": "target:test",
        "action": "evaluate_commit_time_standing",
        "review_ref": "review://sdk/spe/001",
        "evidence_refs": ["evidence://sdk/candidate/001"],
        "policy_context": {"refs": ["policy://sdk/spe-intake/v0.1"]},
        "delegation_context": {"refs": []},
        "validity_window": {"not_before": None, "not_after": None},
        "execution_context": {"mode": "evaluation_only"},
        "recoverability_profile": {"reconstructable": True},
        "source": {
            "repository_ref": "StegVerse-org/StegVerse-SDK",
            "task_ref": "task:spe-intake",
            "handoff_ref": "SDK_MIRROR_HANDOFF.md",
            "origin_manifest_id": "origin.sdk.run-sdk-spe-test",
        },
    }
    candidate = {**candidate_core, "candidate_hash": stable_hash(candidate_core)}
    envelope_core = {
        "schema_version": "stegverse.sdk.spe_commitment_intake.v0.1",
        "destination_repo": "StegVerse-Labs/Standing-Proof-Engine",
        "route_purpose": "FRESH_STANDING_DETERMINATION",
        "package_id": candidate["package_id"],
        "transition_id": candidate["transition_id"],
        "run_id": candidate["run_id"],
        "candidate_hash": candidate["candidate_hash"],
        "candidate": candidate,
        "authority": {
            "sdk_authorizing": False,
            "execution_authority_requested": False,
            "fresh_standing_determination_required": True,
        },
        "expected_result": ["ALLOW", "DENY", "FAIL_CLOSED"],
        "receipt_required": True,
    }
    return {**envelope_core, "envelope_hash": stable_hash(envelope_core)}


class SDKCommitmentIntakeTests(unittest.TestCase):
    def test_valid_envelope_and_allow_receipt(self) -> None:
        envelope = build_envelope()
        validate_sdk_commitment_envelope(envelope)
        receipt = emit_spe_standing_receipt(
            envelope,
            result="ALLOW",
            policy_refs=["policy://spe/standing/v0.5.0"],
            reasons=["standing requirements satisfied"],
        )
        self.assertEqual(receipt["standing_result"], "ALLOW")
        self.assertFalse(receipt["execution_authorized"])
        self.assertFalse(receipt["execution_performed"])
        self.assertEqual(receipt["transition_id"], envelope["transition_id"])
        self.assertTrue(receipt["receipt_hash"])

    def test_rejects_tampered_candidate(self) -> None:
        envelope = build_envelope()
        envelope["candidate"]["action"] = "tampered"
        with self.assertRaisesRegex(SDKCommitmentIntakeError, "candidate_hash mismatch"):
            validate_sdk_commitment_envelope(envelope)

    def test_rejects_execution_authority_request(self) -> None:
        envelope = build_envelope()
        envelope["authority"]["execution_authority_requested"] = True
        envelope_core = dict(envelope)
        envelope_core.pop("envelope_hash")
        envelope["envelope_hash"] = stable_hash(envelope_core)
        with self.assertRaisesRegex(SDKCommitmentIntakeError, "execution authority"):
            validate_sdk_commitment_envelope(envelope)

    def test_fail_closed_has_no_next_boundary(self) -> None:
        receipt = emit_spe_standing_receipt(build_envelope(), result="FAIL_CLOSED")
        self.assertIsNone(receipt["next_boundary"])
        self.assertFalse(receipt["master_record_installed"])

    def test_canonical_sdk_envelope_fixture(self) -> None:
        envelope = load_json(CANONICAL_ENVELOPE)
        validate_sdk_commitment_envelope(envelope)
        self.assertEqual(envelope["candidate_hash"], envelope["candidate"]["candidate_hash"])
        self.assertEqual(envelope["transition_id"], envelope["candidate"]["transition_id"])
        self.assertEqual(envelope["run_id"], envelope["candidate"]["run_id"])

    def test_canonical_receipt_examples_reconstruct(self) -> None:
        envelope = load_json(CANONICAL_ENVELOPE)
        expected = load_json(CANONICAL_RECEIPTS)
        reasons = {
            "ALLOW": ["standing requirements satisfied for progression only"],
            "DENY": ["standing requirements not satisfied"],
            "FAIL_CLOSED": ["required standing evidence unavailable or invalid"],
        }

        for result in ("ALLOW", "DENY", "FAIL_CLOSED"):
            with self.subTest(result=result):
                actual = emit_spe_standing_receipt(
                    envelope,
                    result=result,
                    policy_refs=["policy://sdk/spe-intake/v0.1"],
                    evidence_refs=["evidence://sdk/candidate/fixture/001"],
                    reasons=reasons[result],
                )
                self.assertEqual(actual, expected[result])
                self.assertFalse(actual["execution_authorized"])
                self.assertFalse(actual["execution_performed"])
                self.assertFalse(actual["master_record_installed"])


if __name__ == "__main__":
    unittest.main()
