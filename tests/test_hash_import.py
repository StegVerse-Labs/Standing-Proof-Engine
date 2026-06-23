import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify_hash_import import verify_hash_import


class HashImportVerifierTest(unittest.TestCase):
    def test_hash_import_binds_destination_event(self):
        record_path = ROOT / "samples" / "destination_generated_event_hash_001.json"
        record = json.loads(record_path.read_text(encoding="utf-8"))

        status, checks = verify_hash_import(record, ROOT)
        check_map = {check.name: check.status for check in checks}

        self.assertEqual(status, "PASS")
        self.assertEqual(check_map["parse_hash_import"], "PASS")
        self.assertEqual(check_map["hash_import_route"], "PASS")
        self.assertEqual(check_map["source_event_hash_binding"], "PASS")
        self.assertEqual(check_map["destination_event_hash_binding"], "PASS")
        self.assertEqual(check_map["source_event_verifies"], "PASS")
        self.assertEqual(check_map["hash_result_binding"], "PASS")
        self.assertEqual(check_map["hash_import_flags"], "PASS")

    def test_hash_import_detects_destination_hash_drift(self):
        record_path = ROOT / "samples" / "destination_generated_event_hash_001.json"
        record = json.loads(record_path.read_text(encoding="utf-8"))
        record["destination_event_hash"] = "wrong"

        status, checks = verify_hash_import(record, ROOT)

        self.assertEqual(status, "FAIL")
        self.assertTrue(any(check.name == "destination_event_hash_binding" and check.status == "FAIL" for check in checks))


if __name__ == "__main__":
    unittest.main()
