from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify_manifest import verify_manifest


class CommitmentCandidateManifestTest(unittest.TestCase):
    def test_alane_edge_manifest_is_data_driven(self):
        status, report = verify_manifest(ROOT / "samples" / "alane_commitment_candidate_manifest.json")

        self.assertEqual(status, "PASS")
        self.assertEqual(report["manifest_id"], "SPE-ALANE-COMMITMENT-CANDIDATE-001")
        self.assertEqual(report["sample_count"], 6)
        self.assertTrue(all(item["source"] == "transition_case" for item in report["samples"]))
        self.assertTrue(all(item["artifact_type"] == "commitment_candidate_test" for item in report["samples"]))
        self.assertTrue(all(item["governance_result"] == "FAIL_CLOSED" for item in report["samples"]))
        self.assertTrue(all(item["matches_expectation"] for item in report["samples"]))


if __name__ == "__main__":
    unittest.main()
