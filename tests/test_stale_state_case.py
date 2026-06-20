import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify import PASS, verify_artifact


class StaleStateCaseTest(unittest.TestCase):
    def test_stale_state_case_reports_pass(self):
        artifact_path = ROOT / "samples" / "stale_state_review_commit_001.json"
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))

        status, checks = verify_artifact(artifact)
        check_map = {check.name: check for check in checks}

        self.assertEqual(status, PASS)
        for name in [
            "parse_proof",
            "review_artifact",
            "commit_state",
            "standing_rule",
            "standing_evaluation",
            "receipt",
            "formalism_expectation",
        ]:
            self.assertEqual(check_map[name].status, "PASS")


if __name__ == "__main__":
    unittest.main()
