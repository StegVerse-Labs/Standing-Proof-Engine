import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.result_export import artifact_type, canonical_sha256, result_dict, section_hashes
from spe.verify import verify_artifact


class ResultExportTest(unittest.TestCase):
    def test_canonical_hash_is_stable(self):
        left = {"b": 2, "a": 1}
        right = {"a": 1, "b": 2}
        self.assertEqual(canonical_sha256(left), canonical_sha256(right))

    def test_pressure_result_export_shape(self):
        artifact_path = ROOT / "samples" / "pressure_demo_001.json"
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
        status, checks = verify_artifact(artifact)
        exported = result_dict(artifact, status, checks)

        self.assertEqual(exported["spe_result"], "PARTIAL")
        self.assertEqual(exported["artifact_type"], "pressure_trace")
        self.assertIn("artifact", exported["hashes"])
        self.assertIn("baseline", exported["hashes"])
        self.assertTrue(exported["checks"])

    def test_stale_state_section_hashes(self):
        artifact_path = ROOT / "samples" / "stale_state_review_commit_001.json"
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
        hashes = section_hashes(artifact)

        self.assertEqual(artifact_type(artifact), "stale_state_proof")
        self.assertIn("review_time", hashes)
        self.assertIn("commit_time", hashes)
        self.assertIn("receipt", hashes)


if __name__ == "__main__":
    unittest.main()
