import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify import PASS, verify_artifact


class AegisIncidentCaseTest(unittest.TestCase):
    def test_aegis_incident_case_reports_pass_for_denial(self):
        artifact_path = ROOT / "samples" / "aegis_incident_standing_001.json"
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))

        status, checks = verify_artifact(artifact)
        check_map = {check.name: check for check in checks}

        self.assertEqual(status, PASS)
        self.assertEqual(artifact["standing_evaluation"]["result"], "DENY")
        self.assertFalse(artifact["receipt"]["commit_allowed"])

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
