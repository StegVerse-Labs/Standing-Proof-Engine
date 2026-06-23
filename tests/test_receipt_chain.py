import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify_receipt_chain import verify_receipt_chain


class ReceiptChainVerifierTest(unittest.TestCase):
    def test_receipt_chain_binds_hash_import(self):
        chain_path = ROOT / "samples" / "destination_receipt_chain_001.json"
        chain = json.loads(chain_path.read_text(encoding="utf-8"))

        status, checks = verify_receipt_chain(chain, ROOT)
        check_map = {check.name: check.status for check in checks}

        self.assertEqual(status, "PASS")
        self.assertEqual(check_map["parse_receipt_chain"], "PASS")
        self.assertEqual(check_map["receipt_chain_route"], "PASS")
        self.assertEqual(check_map["source_hash_import_binding"], "PASS")
        self.assertEqual(check_map["source_hash_import_verifies"], "PASS")
        self.assertEqual(check_map["receipt_chain_order"], "PASS")
        self.assertEqual(check_map["receipt_chain_artifacts_exist"], "PASS")
        self.assertEqual(check_map["receipt_chain_final_binding"], "PASS")
        self.assertEqual(check_map["receipt_chain_flags"], "PASS")
        self.assertEqual(check_map["receipt_chain_result"], "PASS")

    def test_receipt_chain_detects_hash_import_drift(self):
        chain_path = ROOT / "samples" / "destination_receipt_chain_001.json"
        chain = json.loads(chain_path.read_text(encoding="utf-8"))
        chain["source_hash_import_sha256"] = "wrong"

        status, checks = verify_receipt_chain(chain, ROOT)

        self.assertEqual(status, "FAIL")
        self.assertTrue(any(check.name == "source_hash_import_binding" and check.status == "FAIL" for check in checks))


if __name__ == "__main__":
    unittest.main()
