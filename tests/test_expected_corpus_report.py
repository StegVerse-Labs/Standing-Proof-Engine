import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.report_expected_corpus import render_fixture_report


class ExpectedCorpusReportTest(unittest.TestCase):
    def test_aegis_fixture_report_includes_governance_result(self):
        fixture_path = ROOT / "expected_results" / "aegis_incident_standing_001.expected.json"
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))

        report = render_fixture_report(fixture_path.relative_to(ROOT), fixture, ROOT)

        self.assertIn("Expected Governance Result", report)
        self.assertIn("Actual Governance Result", report)
        self.assertIn("Governance Result Match: **YES**", report)
        self.assertIn("**DENY**", report)


if __name__ == "__main__":
    unittest.main()
