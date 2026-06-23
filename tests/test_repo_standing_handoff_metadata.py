import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PATH = REPO_ROOT / "reports" / "repo_standing_handoff.json"


class RepoStandingHandoffMetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(HANDOFF_PATH.read_text(encoding="utf-8"))

    def test_handoff_identity(self) -> None:
        self.assertEqual(self.data["handoff_id"], "spe_repo_standing_handoff_001")
        self.assertEqual(self.data["repo"], "StegVerse-Labs/Standing-Proof-Engine")

    def test_required_commands(self) -> None:
        self.assertEqual(self.data["repo_standing_command"], "python tools/run_repo_standing.py")
        self.assertEqual(self.data["repo_standing_json_command"], "python tools/run_repo_standing.py --json")
        self.assertEqual(self.data["automation_addendum_check"], "python tools/check_automation_addendum.py")
        self.assertEqual(self.data["automation_addendum_json_check"], "python tools/check_automation_addendum.py --json")
        self.assertEqual(self.data["test_discovery_command"], "python -m unittest discover -s tests -p 'test_*.py'")

    def test_expected_standing_values(self) -> None:
        self.assertEqual(self.data["expected_repo_standing"], "PASS")
        self.assertEqual(self.data["expected_mathematical_claim_standing"], "PARTIAL")
        self.assertEqual(self.data["pending_actions"], [])

    def test_referenced_artifacts_exist(self) -> None:
        display_to_actual = {
            "github/workflows/verify.yml": ".github/workflows/verify.yml",
        }
        for artifact_path in self.data["artifact_paths"]:
            actual_path = display_to_actual.get(artifact_path, artifact_path)
            with self.subTest(artifact_path=artifact_path):
                self.assertTrue((REPO_ROOT / actual_path).exists())


if __name__ == "__main__":
    unittest.main()
