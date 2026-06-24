import json
import unittest
from pathlib import Path

from spe.verify import PASS
from spe.verify_external_refs import verify_external_ref_artifact


REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_PATH = REPO_ROOT / "samples" / "external_source_ref_stale_state_001.json"


class ExternalSourceRefProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))

    def test_external_source_refs_project_to_core_stale_state_fields(self) -> None:
        status, checks = verify_external_ref_artifact(self.artifact, REPO_ROOT)
        self.assertEqual(status, PASS)
        failed = [check.name for check in checks if check.status != PASS]
        self.assertEqual(failed, [])

    def test_commit_state_passes_after_projection(self) -> None:
        _, checks = verify_external_ref_artifact(self.artifact, REPO_ROOT)
        commit_state = next(check for check in checks if check.name == "commit_state")
        self.assertEqual(commit_state.status, PASS)


if __name__ == "__main__":
    unittest.main()
