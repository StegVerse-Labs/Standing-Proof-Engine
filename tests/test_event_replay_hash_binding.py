import json
import unittest
from pathlib import Path

from spe.result_export import canonical_sha256
from spe.verify import PASS
from spe.verify_event_replay import verify_event_replay


REPO_ROOT = Path(__file__).resolve().parents[1]
REPLAY_PATHS = (
    REPO_ROOT / "samples" / "event_replay_001.json",
    REPO_ROOT / "samples" / "event_replay_deferred_001.json",
)


class EventReplayHashBindingTests(unittest.TestCase):
    def load_replay_and_event(self, replay_path: Path):
        replay = json.loads(replay_path.read_text(encoding="utf-8"))
        event_path = REPO_ROOT / replay["source_event"]
        event = json.loads(event_path.read_text(encoding="utf-8"))
        return replay, event

    def test_source_event_hash_matches_canonical_event_hash(self) -> None:
        for replay_path in REPLAY_PATHS:
            with self.subTest(replay_path=str(replay_path.relative_to(REPO_ROOT))):
                replay, event = self.load_replay_and_event(replay_path)
                self.assertEqual(replay["source_event_sha256"], canonical_sha256(event))

    def test_event_replays_verify(self) -> None:
        for replay_path in REPLAY_PATHS:
            with self.subTest(replay_path=str(replay_path.relative_to(REPO_ROOT))):
                replay, _ = self.load_replay_and_event(replay_path)
                status, checks = verify_event_replay(replay, REPO_ROOT)
                self.assertEqual(status, PASS)
                failed = [check.check_id for check in checks if check.status != PASS]
                self.assertEqual(failed, [])


if __name__ == "__main__":
    unittest.main()
