import json
import unittest
from pathlib import Path

from spe.result_export import canonical_sha256
from spe.verify import PASS
from spe.verify_destination_event import verify_destination_event


REPO_ROOT = Path(__file__).resolve().parents[1]
EVENT_PATH = REPO_ROOT / "samples" / "destination_event_001.json"


class DestinationEventHashBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.event = json.loads(EVENT_PATH.read_text(encoding="utf-8"))
        confirmation_path = REPO_ROOT / self.event["source_confirmation"]
        self.confirmation = json.loads(confirmation_path.read_text(encoding="utf-8"))

    def test_source_confirmation_hash_matches_canonical_confirmation_hash(self) -> None:
        self.assertEqual(self.event["source_confirmation_sha256"], canonical_sha256(self.confirmation))

    def test_destination_event_verifies(self) -> None:
        status, checks = verify_destination_event(self.event, REPO_ROOT)
        self.assertEqual(status, PASS)
        failed = [check.check_id for check in checks if check.status != PASS]
        self.assertEqual(failed, [])


if __name__ == "__main__":
    unittest.main()
