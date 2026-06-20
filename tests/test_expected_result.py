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

    def test_aegis_expected_result_fixture_checks_governance_result(self):
        fixture_path = ROOT / "expected_results" / "aegis_incident_standing_001.expected.json"
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))

        status, checks = verify_expected_result(fixture, ROOT)
        check_map = {check.name: check.status for check in checks}

        self.assertEqual(status, "PASS")
        self.assertEqual(check_map["expected_governance_result"], "PASS")

    def test_sdk_intake_expected_result_fixture_checks_binding_result(self):
        fixture_path = ROOT / "expected_results" / "sdk_intake_receipt_001.expected.json"
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))

        status, checks = verify_expected_result(fixture, ROOT)
        check_map = {check.name: check.status for check in checks}

        self.assertEqual(status, "PASS")
        self.assertEqual(check_map["expected_spe_result"], "PASS")
        self.assertEqual(check_map["expected_governance_result"], "PASS")
        self.assertEqual(check_map["expected_check:manifest_result_binding"], "PASS")

    def test_expected_result_detects_status_drift(self):
        fixture_path = ROOT / "expected_results" / "external_source_ref_stale_state_001.expected.json"
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        fixture["expected"]["spe_result"] = "FAIL"

        status, checks = verify_expected_result(fixture, ROOT)
        self.assertEqual(status, "FAIL")
        self.assertTrue(any(check.name == "expected_spe_result" and check.status == "FAIL" for check in checks))

    def test_expected_result_detects_governance_result_drift(self):
        fixture_path = ROOT / "expected_results" / "aegis_incident_standing_001.expected.json"
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        fixture["expected"]["governance_result"] = "DIFFERENT"

        status, checks = verify_expected_result(fixture, ROOT)
        self.assertEqual(status, "FAIL")
        self.assertTrue(any(check.name == "expected_governance_result" and check.status == "FAIL" for check in checks))


if __name__ == "__main__":
    unittest.main()
