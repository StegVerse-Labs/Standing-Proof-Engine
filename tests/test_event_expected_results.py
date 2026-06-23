import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify_destination_event import verify_destination_event
from spe.verify_event_replay import verify_event_replay


class EventExpectedResultFixtureTest(unittest.TestCase):
    def check_fixture(self, name):
        fixture = json.loads((ROOT / "expected_results" / name).read_text(encoding="utf-8"))
        artifact = json.loads((ROOT / fixture["artifact"]).read_text(encoding="utf-8"))
        if fixture["verifier"] == "spe/verify_destination_event.py":
            status, checks = verify_destination_event(artifact, ROOT)
            actual_result = artifact["event_result"]
        else:
            status, checks = verify_event_replay(artifact, ROOT)
            actual_result = artifact["observed_result"]
        check_map = {check.name: check.status for check in checks}
        expected = fixture["expected"]
        self.assertEqual(status, expected["spe_result"])
        self.assertEqual(actual_result, expected["governance_result"])
        for check_name, check_status in expected["required_checks"].items():
            self.assertEqual(check_map[check_name], check_status)

    def test_destination_event_expected_fixture(self):
        self.check_fixture("destination_event_001.expected.json")

    def test_destination_event_deferred_expected_fixture(self):
        self.check_fixture("destination_event_deferred_001.expected.json")

    def test_event_replay_expected_fixture(self):
        self.check_fixture("event_replay_001.expected.json")

    def test_event_replay_deferred_expected_fixture(self):
        self.check_fixture("event_replay_deferred_001.expected.json")


if __name__ == "__main__":
    unittest.main()
