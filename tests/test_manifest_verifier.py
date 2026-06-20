import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify_manifest import verify_manifest


class ManifestVerifierTest(unittest.TestCase):
    def test_sample_manifest_verifies_all_declared_routes(self):
        status, report = verify_manifest(ROOT / "samples" / "manifest.json")

        self.assertEqual(status, "PARTIAL")
        self.assertEqual(report["manifest_id"], "SPE-SAMPLE-MANIFEST-001")
        self.assertEqual(report["sample_count"], 3)
        self.assertTrue(all(item["matches_expectation"] for item in report["samples"]))

    def test_manifest_report_is_json_serializable(self):
        _, report = verify_manifest(ROOT / "samples" / "manifest.json")
        encoded = json.dumps(report, sort_keys=True)

        self.assertIn("pressure_receipt_trace", encoded)
        self.assertIn("stale_state_review_to_commit", encoded)
        self.assertIn("incident_standing_proof", encoded)


if __name__ == "__main__":
    unittest.main()
