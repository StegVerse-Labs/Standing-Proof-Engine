import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify_pointer import verify_pointer


class PointerVerifierTest(unittest.TestCase):
    def test_pointer_binds_source_and_manifest(self):
        pointer_path = ROOT / "samples" / "master_records_pointer_001.json"
        pointer = json.loads(pointer_path.read_text(encoding="utf-8"))

        status, checks = verify_pointer(pointer, ROOT)
        check_map = {check.name: check.status for check in checks}

        self.assertEqual(status, "PASS")
        self.assertEqual(check_map["parse_pointer"], "PASS")
        self.assertEqual(check_map["source_hash_binding"], "PASS")
        self.assertEqual(check_map["manifest_hash_binding"], "PASS")
        self.assertEqual(check_map["target_binding"], "PASS")

    def test_pointer_detects_manifest_hash_drift(self):
        pointer_path = ROOT / "samples" / "master_records_pointer_001.json"
        pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
        pointer["route_manifest_sha256"] = "wrong"

        status, checks = verify_pointer(pointer, ROOT)

        self.assertEqual(status, "FAIL")
        self.assertTrue(any(check.name == "manifest_hash_binding" and check.status == "FAIL" for check in checks))


if __name__ == "__main__":
    unittest.main()
