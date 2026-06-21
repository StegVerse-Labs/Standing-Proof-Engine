import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify_confirmation import verify_confirmation


class ConfirmationVerifierTest(unittest.TestCase):
    def test_confirmation_binds_pointer(self):
        confirmation_path = ROOT / "samples" / "master_records_confirmation_001.json"
        confirmation = json.loads(confirmation_path.read_text(encoding="utf-8"))

        status, checks = verify_confirmation(confirmation, ROOT)
        check_map = {check.name: check.status for check in checks}

        self.assertEqual(status, "PASS")
        self.assertEqual(check_map["parse_confirmation"], "PASS")
        self.assertEqual(check_map["confirmation_route"], "PASS")
        self.assertEqual(check_map["source_pointer_hash_binding"], "PASS")
        self.assertEqual(check_map["source_pointer_verifies"], "PASS")
        self.assertEqual(check_map["confirmation_result_binding"], "PASS")
        self.assertEqual(check_map["confirmation_target_binding"], "PASS")

    def test_confirmation_detects_pointer_hash_drift(self):
        confirmation_path = ROOT / "samples" / "master_records_confirmation_001.json"
        confirmation = json.loads(confirmation_path.read_text(encoding="utf-8"))
        confirmation["source_pointer_sha256"] = "wrong"

        status, checks = verify_confirmation(confirmation, ROOT)

        self.assertEqual(status, "FAIL")
        self.assertTrue(any(check.name == "source_pointer_hash_binding" and check.status == "FAIL" for check in checks))


if __name__ == "__main__":
    unittest.main()
