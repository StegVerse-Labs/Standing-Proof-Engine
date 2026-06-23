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

    def test_hash_import_expected_fixture_matches(self):
        fixture = json.loads((ROOT / "expected_results" / "hash_import_001.expected.json").read_text(encoding="utf-8"))
        record = json.loads((ROOT / fixture["artifact"]).read_text(encoding="utf-8"))
        status, checks = verify_hash_import(record, ROOT)
        check_map = {check.name: check.status for check in checks}
        expected = fixture["expected"]

        self.assertEqual(status, expected["spe_result"])
        self.assertEqual(record["expected_event_result"], expected["governance_result"])
        for check_name, check_status in expected["required_checks"].items():
            self.assertEqual(check_map[check_name], check_status)

    def test_hash_import_detects_destination_hash_drift(self):
        record_path = ROOT / "samples" / "destination_generated_event_hash_001.json"
        record = json.loads(record_path.read_text(encoding="utf-8"))
        record["destination_event_hash"] = "wrong"

        status, checks = verify_hash_import(record, ROOT)

        self.assertEqual(status, "FAIL")
        self.assertTrue(any(check.name == "destination_event_hash_binding" and check.status == "FAIL" for check in checks))


if __name__ == "__main__":
    unittest.main()
