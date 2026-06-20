import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.report import render_report, select_verifier


class ReportTest(unittest.TestCase):
    def test_pressure_report_contains_partial_result(self):
        artifact_path = ROOT / "samples" / "pressure_demo_001.json"
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
        status, checks = select_verifier("default", artifact, ROOT)
        report = render_report("pressure-demo-001", str(artifact_path), "default", artifact, status, checks)

        self.assertIn("SPE Result: **PARTIAL**", report)
        self.assertIn("authority_context_proof", report)
        self.assertIn("Artifact SHA-256", report)

    def test_external_reference_report_contains_pass_result(self):
        artifact_path = ROOT / "samples" / "external_source_ref_stale_state_001.json"
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
        status, checks = select_verifier("external_refs", artifact, ROOT)
        report = render_report("external-source-ref", str(artifact_path), "external_refs", artifact, status, checks)

        self.assertIn("SPE Result: **PASS**", report)
        self.assertIn("source_object_refs", report)
        self.assertIn("source_hash_bindings", report)


if __name__ == "__main__":
    unittest.main()
