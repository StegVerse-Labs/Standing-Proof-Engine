import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.result_export import result_dict
from spe.verify_confirmation import verify_confirmation


class ConfirmationJsonExportTest(unittest.TestCase):
    def test_confirmation_export_contains_result_summary(self):
        artifact_path = ROOT / "samples" / "master_records_confirmation_001.json"
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))

        status, checks = verify_confirmation(artifact, ROOT)
        exported = result_dict(artifact, status, checks)
        summary = exported["governance_summary"]

        self.assertEqual(exported["spe_result"], "PASS")
        self.assertEqual(exported["artifact_type"], "master_records_pointer_confirmation")
        self.assertEqual(summary["confirmation_id"], "MR-SPE-CONFIRM-001")
        self.assertEqual(summary["confirmation_result"], "ACCEPTED_FOR_RECONSTRUCTION")
        self.assertTrue(summary["installed"])
        self.assertTrue(summary["reconstruction_available"])
        self.assertTrue(any(check["name"] == "source_pointer_hash_binding" for check in exported["checks"]))


if __name__ == "__main__":
    unittest.main()
