import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.write_release_readiness import REQUIRED_FILES, status_for


class ReleaseReadinessTest(unittest.TestCase):
    def test_release_readiness_required_files_are_present(self):
        payload = status_for(ROOT)

        self.assertEqual(payload["release_candidate"], "v0.4.0")
        self.assertEqual(payload["spe_release_readiness"], "READY")
        self.assertTrue(all(item["present"] for item in payload["required_files"]))
        self.assertEqual(payload["manual_internal_tasks"], [])

    def test_release_readiness_detects_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for path in REQUIRED_FILES[:-1]:
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("x", encoding="utf-8")

            payload = status_for(root)

        self.assertEqual(payload["spe_release_readiness"], "NOT_READY")
        self.assertTrue(any(not item["present"] for item in payload["required_files"]))


if __name__ == "__main__":
    unittest.main()
