import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify_destination_event import verify_destination_event


class DestinationEventVerifierTest(unittest.TestCase):
    def test_destination_event_binds_confirmation(self):
        event_path = ROOT / "samples" / "destination_event_001.json"
        event = json.loads(event_path.read_text(encoding="utf-8"))

        status, checks = verify_destination_event(event, ROOT)
        check_map = {check.name: check.status for check in checks}

        self.assertEqual(status, "PASS")
        self.assertEqual(check_map["parse_destination_event"], "PASS")
        self.assertEqual(check_map["destination_event_route"], "PASS")
        self.assertEqual(check_map["source_confirmation_hash_binding"], "PASS")
        self.assertEqual(check_map["source_confirmation_verifies"], "PASS")
        self.assertEqual(check_map["destination_event_result_binding"], "PASS")
        self.assertEqual(check_map["destination_event_target_binding"], "PASS")

    def test_deferred_destination_event_binds_confirmation(self):
        event_path = ROOT / "samples" / "destination_event_deferred_001.json"
        event = json.loads(event_path.read_text(encoding="utf-8"))

        status, checks = verify_destination_event(event, ROOT)
        check_map = {check.name: check.status for check in checks}

        self.assertEqual(status, "PASS")
        self.assertEqual(event["event_result"], "NOT_INSTALLED")
        self.assertEqual(check_map["destination_event_result_binding"], "PASS")

    def test_destination_event_detects_confirmation_hash_drift(self):
        event_path = ROOT / "samples" / "destination_event_001.json"
        event = json.loads(event_path.read_text(encoding="utf-8"))
        event["source_confirmation_sha256"] = "wrong"

        status, checks = verify_destination_event(event, ROOT)

        self.assertEqual(status, "FAIL")
        self.assertTrue(any(check.name == "source_confirmation_hash_binding" and check.status == "FAIL" for check in checks))


if __name__ == "__main__":
    unittest.main()
