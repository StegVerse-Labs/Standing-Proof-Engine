import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify_sdk_intake import verify_sdk_intake


class SdkIntakeVerifierTest(unittest.TestCase):
    def test_sdk_intake_receipt_binds_manifest_route(self):
        receipt_path = ROOT / "samples" / "sdk_intake_receipt_001.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

        status, checks = verify_sdk_intake(receipt, ROOT)
        check_map = {check.name: check.status for check in checks}

        self.assertEqual(status, "PASS")
        self.assertEqual(check_map["parse_sdk_intake"], "PASS")
        self.assertEqual(check_map["route_declaration"], "PASS")
        self.assertEqual(check_map["handoff_flags"], "PASS")
        self.assertEqual(check_map["manifest_hash_binding"], "PASS")
        self.assertEqual(check_map["manifest_result_binding"], "PASS")
        self.assertEqual(check_map["sample_count_binding"], "PASS")

    def test_sdk_intake_detects_expected_package_drift(self):
        receipt_path = ROOT / "samples" / "sdk_intake_receipt_001.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["expected_package_status"] = "PASS"

        status, checks = verify_sdk_intake(receipt, ROOT)

        self.assertEqual(status, "FAIL")
        self.assertTrue(any(check.name == "manifest_result_binding" and check.status == "FAIL" for check in checks))

    def test_sdk_intake_detects_manifest_hash_drift(self):
        receipt_path = ROOT / "samples" / "sdk_intake_receipt_001.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["manifest_sha256"] = "wrong"

        status, checks = verify_sdk_intake(receipt, ROOT)

        self.assertEqual(status, "FAIL")
        self.assertTrue(any(check.name == "manifest_hash_binding" and check.status == "FAIL" for check in checks))


if __name__ == "__main__":
    unittest.main()
