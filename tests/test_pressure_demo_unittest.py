import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify import PARTIAL, verify_trace


class PressureDemoFormalismTest(unittest.TestCase):
    def test_pressure_demo_reports_partial_authority_proof(self):
        trace_path = ROOT / "samples" / "pressure_demo_001.json"
        trace = json.loads(trace_path.read_text(encoding="utf-8"))

        status, checks = verify_trace(trace)
        check_map = {check.name: check for check in checks}

        self.assertEqual(status, PARTIAL)
        self.assertEqual(check_map["parse_trace"].status, "PASS")
        self.assertEqual(check_map["baseline_reconstruction"].status, "PASS")
        self.assertEqual(check_map["drift_observation"].status, "PASS")
        self.assertEqual(check_map["pressure_receipt"].status, "PASS")
        self.assertEqual(check_map["local_predicates"].status, "PASS")
        self.assertEqual(check_map["aggregate_admissibility"].status, "PASS")
        self.assertEqual(check_map["commit_boundary"].status, "PASS")
        self.assertEqual(check_map["replay_path"].status, "PASS")
        self.assertEqual(check_map["authority_context_proof"].status, "PARTIAL")


if __name__ == "__main__":
    unittest.main()
