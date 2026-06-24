import json
import unittest
from pathlib import Path

from spe.result_export import canonical_sha256
from spe.verify import PASS
from spe.verify_confirmation import verify_confirmation


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIRMATION_PATH = REPO_ROOT / "samples" / "master_records_confirmation_001.json"


class ConfirmationHashBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.confirmation = json.loads(CONFIRMATION_PATH.read_text(encoding="utf-8"))
        pointer_path = REPO_ROOT / self.confirmation["source_pointer"]
        self.pointer = json.loads(pointer_path.read_text(encoding="utf-8"))

    def test_source_pointer_hash_matches_canonical_pointer_hash(self) -> None:
        self.assertEqual(self.confirmation["source_pointer_sha256"], canonical_sha256(self.pointer))

    def test_confirmation_verifies(self) -> None:
        status, checks = verify_confirmation(self.confirmation, REPO_ROOT)
        self.assertEqual(status, PASS)
        failed = [check.check_id for check in checks if check.status != PASS]
        self.assertEqual(failed, [])


if __name__ == "__main__":
    unittest.main()
