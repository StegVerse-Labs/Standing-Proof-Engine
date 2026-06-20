import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify_expected_result import verify_expected_result


class ExpectedResultFixtureTest(unittest.TestCase):
    def test_expected_result_fixture_passes(self):
        fixture_path = ROOT / "expected_results" / "external_source_ref_stale_state_001.expected.json"
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))

        status, checks = verify_expected_result(fixture, ROOT)
        self.assertEqual(status, "PASS")
        self.assertTrue(all(check.status == "PASS" for check in checks))

    def test_expected_result_detects_status_drift(self):
        fixture_path = ROOT / "expected_results" / "external_source_ref_stale_state_001.expected.json"
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        fixture["expected"]["spe_result"] = "FAIL"

        status, checks = verify_expected_result(fixture, ROOT)
        self.assertEqual(status, "FAIL")
        self.assertTrue(any(check.name == "expected_spe_result" and check.status == "FAIL" for check in checks))


if __name__ == "__main__":
    unittest.main()
