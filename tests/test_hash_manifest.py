import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify_hash_manifest import verify_hash_manifest


class HashManifestTest(unittest.TestCase):
    def test_external_source_hash_manifest_passes(self):
        manifest_path = ROOT / "samples" / "hash_manifests" / "external_source_ref_stale_state_001.hashes.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        status, checks = verify_hash_manifest(manifest, ROOT)
        self.assertEqual(status, "PASS")
        self.assertTrue(all(check.status == "PASS" for check in checks))

    def test_hash_manifest_detects_changed_literal_hash(self):
        manifest_path = ROOT / "samples" / "hash_manifests" / "external_source_ref_stale_state_001.hashes.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["bindings"]["review_artifact_hash"]["sha256"] = "mismatch"

        status, checks = verify_hash_manifest(manifest, ROOT)
        self.assertEqual(status, "FAIL")
        self.assertTrue(any(check.status == "FAIL" for check in checks))


if __name__ == "__main__":
    unittest.main()
