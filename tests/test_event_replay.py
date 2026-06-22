import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify_event_replay import verify_event_replay


class EventReplayVerifierTest(unittest.TestCase):
    def test_event_replay_binds_source_event(self):
        replay_path = ROOT / "samples" / "event_replay_001.json"
        replay = json.loads(replay_path.read_text(encoding="utf-8"))

        status, checks = verify_event_replay(replay, ROOT)
        check_map = {check.name: check.status for check in checks}

        self.assertEqual(status, "PASS")
        self.assertEqual(check_map["parse_event_replay"], "PASS")
        self.assertEqual(check_map["source_event_hash_binding"], "PASS")
        self.assertEqual(check_map["source_event_verifies"], "PASS")
        self.assertEqual(check_map["replay_result_binding"], "PASS")
        self.assertEqual(check_map["replay_handoff_flags"], "PASS")

    def test_deferred_event_replay_binds_source_event(self):
        replay_path = ROOT / "samples" / "event_replay_deferred_001.json"
        replay = json.loads(replay_path.read_text(encoding="utf-8"))

        status, checks = verify_event_replay(replay, ROOT)
        check_map = {check.name: check.status for check in checks}

        self.assertEqual(status, "PASS")
        self.assertEqual(replay["observed_result"], "NOT_INSTALLED")
        self.assertEqual(check_map["replay_result_binding"], "PASS")

    def test_event_replay_detects_source_event_hash_drift(self):
        replay_path = ROOT / "samples" / "event_replay_001.json"
        replay = json.loads(replay_path.read_text(encoding="utf-8"))
        replay["source_event_sha256"] = "wrong"

        status, checks = verify_event_replay(replay, ROOT)

        self.assertEqual(status, "FAIL")
        self.assertTrue(any(check.name == "source_event_hash_binding" and check.status == "FAIL" for check in checks))


if __name__ == "__main__":
    unittest.main()
