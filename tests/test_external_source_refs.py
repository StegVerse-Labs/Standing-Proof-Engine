import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify_external_refs import verify_external_ref_artifact


class ExternalSourceReferenceTest(unittest.TestCase):
    def test_external_source_ref_sample_passes(self):
        artifact_path = ROOT / "samples" / "external_source_ref_stale_state_001.json"
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))

        status, checks = verify_external_ref_artifact(artifact, ROOT)
        check_map = {check.name: check for check in checks}

        self.assertEqual(status, "PASS")
        self.assertEqual(check_map["source_object_refs"].status, "PASS")
        self.assertEqual(check_map["source_hash_bindings"].status, "PASS")

    def test_missing_external_ref_fails(self):
        artifact_path = ROOT / "samples" / "external_source_ref_stale_state_001.json"
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
        artifact["source_object_refs"]["review_artifact"] = "samples/source_objects/missing.json"

        status, checks = verify_external_ref_artifact(artifact, ROOT)
        check_map = {check.name: check for check in checks}

        self.assertEqual(status, "FAIL")
        self.assertEqual(check_map["source_object_refs"].status, "FAIL")


if __name__ == "__main__":
    unittest.main()
