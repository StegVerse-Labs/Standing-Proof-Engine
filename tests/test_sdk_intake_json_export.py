import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.result_export import result_dict
from spe.verify_sdk_intake import verify_sdk_intake


class SdkIntakeJsonExportTest(unittest.TestCase):
    def test_sdk_intake_export_contains_route_binding_summary(self):
        artifact_path = ROOT / "samples" / "sdk_intake_receipt_001.json"
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))

        status, checks = verify_sdk_intake(artifact, ROOT)
        exported = result_dict(artifact, status, checks)
        summary = exported["governance_summary"]

        self.assertEqual(exported["spe_result"], "PASS")
        self.assertEqual(exported["artifact_type"], "sdk_intake_receipt")
        self.assertEqual(summary["receipt_id"], "SDK-INTAKE-SPE-001")
        self.assertEqual(summary["destination_repo"], "StegVerse-Labs/Standing-Proof-Engine")
        self.assertEqual(summary["expected_package_status"], "PARTIAL")
        self.assertTrue(any(check["name"] == "manifest_result_binding" for check in exported["checks"]))


if __name__ == "__main__":
    unittest.main()
