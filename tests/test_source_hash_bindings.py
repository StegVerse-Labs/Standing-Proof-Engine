import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.source_hashes import resolved_hash_bindings, verify_source_hash_bindings
from spe.verify_source_bound import verify_source_bound_artifact


class SourceHashBindingTest(unittest.TestCase):
    def test_source_hash_bound_sample_passes(self):
        artifact_path = ROOT / "samples" / "source_hash_bound_stale_state_001.json"
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))

        status, checks = verify_source_bound_artifact(artifact)
        check_map = {check.name: check for check in checks}

        self.assertEqual(status, "PASS")
        self.assertEqual(check_map["source_hash_bindings"].status, "PASS")

    def test_resolved_hash_bindings_are_computed(self):
        artifact_path = ROOT / "samples" / "source_hash_bound_stale_state_001.json"
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
        bindings = resolved_hash_bindings(artifact)

        self.assertEqual(len(bindings), 7)
        for value in bindings.values():
            self.assertEqual(len(value), 64)

    def test_mismatched_declared_hash_fails(self):
        artifact_path = ROOT / "samples" / "source_hash_bound_stale_state_001.json"
        artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
        artifact["declared_hash_bindings"]["review_artifact_hash"] = "mismatch"

        checks = verify_source_hash_bindings(artifact)
        self.assertEqual(checks[0].status, "FAIL")


if __name__ == "__main__":
    unittest.main()
