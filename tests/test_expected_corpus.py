from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.verify_expected_corpus import verify_expected_corpus


class ExpectedCorpusTest(unittest.TestCase):
    def test_expected_corpus_passes(self):
        status, checks = verify_expected_corpus(ROOT / "expected_results", ROOT)
        self.assertEqual(status, "PASS")
        self.assertTrue(all(check.status == "PASS" for check in checks))

    def test_empty_expected_corpus_fails(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            status, checks = verify_expected_corpus(Path(tmpdir), ROOT)
        self.assertEqual(status, "FAIL")
        self.assertTrue(any(check.status == "FAIL" for check in checks))


if __name__ == "__main__":
    unittest.main()
