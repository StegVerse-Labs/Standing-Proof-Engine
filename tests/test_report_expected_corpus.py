from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spe.report_expected_corpus import main


class ExpectedCorpusReportTest(unittest.TestCase):
    def test_expected_corpus_report_generation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            exit_code = main(["report_expected_corpus.py", "expected_results", tmpdir])
            output_dir = Path(tmpdir)
            self.assertEqual(exit_code, 0)
            self.assertTrue((output_dir / "README.md").exists())
            self.assertTrue(any(output_dir.glob("*.report.md")))


if __name__ == "__main__":
    unittest.main()
