import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = REPO_ROOT / "docs" / "release_readiness_runner.md"


class ReleaseReadinessRunnerDocTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = DOC_PATH.read_text(encoding="utf-8")

    def test_primary_runner_is_declared(self) -> None:
        self.assertIn("python tools/run_repo_standing.py", self.text)
        self.assertIn("primary repo-standing runner", self.text)

    def test_release_readiness_command_is_declared(self) -> None:
        self.assertIn("python tools/write_release_readiness.py", self.text)
        self.assertIn("SPE RELEASE READINESS: READY", self.text)

    def test_generated_artifacts_are_declared(self) -> None:
        self.assertIn("reports/release_readiness.json", self.text)
        self.assertIn("reports/release_readiness.md", self.text)

    def test_non_claim_boundary_is_declared(self) -> None:
        self.assertIn("local SPE release readiness only", self.text)
        self.assertIn("does not claim downstream propagation", self.text)

    def test_manual_copying_posture_is_declared(self) -> None:
        self.assertIn("Manual internal release-readiness copying is not required", self.text)


if __name__ == "__main__":
    unittest.main()
