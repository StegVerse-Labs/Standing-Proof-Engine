import json
import unittest
from pathlib import Path

from spe.verify import PASS
from spe.verify_heartbeat_path_selection import verify_heartbeat_path_selection


class HeartbeatPathSelectionSampleTests(unittest.TestCase):
    def test_sample_receipt_passes(self):
        artifact = json.loads(Path("samples/heartbeat_path_selection_001.json").read_text(encoding="utf-8"))
        status, checks = verify_heartbeat_path_selection(artifact)
        self.assertEqual(status, PASS)
        self.assertTrue(all(check.status == PASS for check in checks))


if __name__ == "__main__":
    unittest.main()
