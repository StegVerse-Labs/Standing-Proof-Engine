import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ADDENDUM_PATH = REPO_ROOT / "research" / "automation_addendum.json"


class AutomationAddendumMetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(ADDENDUM_PATH.read_text(encoding="utf-8"))

    def test_addendum_identity(self) -> None:
        self.assertEqual(self.data["addendum_id"], "spe_research_automation_addendum_001")
        self.assertEqual(self.data["repo"], "StegVerse-Labs/Standing-Proof-Engine")
        self.assertEqual(self.data["status"], "PASS")

    def test_runner_metadata(self) -> None:
        runner = self.data["automation_runner"]
        self.assertEqual(runner["path"], "tools/run_repo_standing.py")
        self.assertTrue((REPO_ROOT / runner["path"]).exists())
        self.assertEqual(runner["text_command"], "python tools/run_repo_standing.py")
        self.assertEqual(runner["json_command"], "python tools/run_repo_standing.py --json")

    def test_ci_route_metadata(self) -> None:
        ci_route = self.data["ci_route"]
        self.assertEqual(ci_route["display_path"], "github/workflows/verify.yml")
        self.assertTrue((REPO_ROOT / ".github" / "workflows" / "verify.yml").exists())
        self.assertIn("python tools/run_repo_standing.py", ci_route["required_steps"])
        self.assertIn("python tools/run_repo_standing.py --json", ci_route["required_steps"])

    def test_component_checks_are_declared(self) -> None:
        component_checks = set(self.data["component_checks"])
        required = {
            "python tools/validate_research_standing.py",
            "python spe/verify_problem_encodings.py",
            "python spe/verify_problem_encodings.py --json",
            "python -m unittest tests.test_problem_encodings",
            "python -m unittest discover -s tests -p 'test_*.py'",
        }
        self.assertTrue(required.issubset(component_checks))


if __name__ == "__main__":
    unittest.main()
