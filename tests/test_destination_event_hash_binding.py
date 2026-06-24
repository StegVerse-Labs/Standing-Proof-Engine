import json
import unittest
from pathlib import Path

from spe.result_export import canonical_sha256
from spe.verify import PASS
from spe.verify_destination_event import verify_destination_event


REPO_ROOT = Path(__file__).resolve().parents[1]
EVENT_PATHS = (
    REPO_ROOT / "samples" / "destination_event_001.json",
    REPO_ROOT / "samples" / "destination_event_deferred_001.json",
)


class DestinationEventHashBindingTests(unittest.TestCase):
    def load_event_and_confirmation(self, event_path: Path):
        event = json.loads(event_path.read_text(encoding="utf-8"))
        confirmation_path = REPO_ROOT / event["source_confirmation"]
        confirmation = json.loads(confirmation_path.read_text(encoding="utf-8"))
        return event, confirmation

    def test_source_confirmation_hash_matches_canonical_confirmation_hash(self) -> None:
        for event_path in EVENT_PATHS:
            with self.subTest(event_path=str(event_path.relative_to(REPO_ROOT))):
                event, confirmation = self.load_event_and_confirmation(event_path)
                self.assertEqual(event["source_confirmation_sha256"], canonical_sha256(confirmation))

    def test_destination_events_verify(self) -> None:
        for event_path in EVENT_PATHS:
            with self.subTest(event_path=str(event_path.relative_to(REPO_ROOT))):
                event, _ = self.load_event_and_confirmation(event_path)
                status, checks = verify_destination_event(event, REPO_ROOT)
                self.assertEqual(status, PASS)
                failed = [check.check_id for check in checks if check.status != PASS]
                self.assertEqual(failed, [])


if __name__ == "__main__":
    unittest.main()
