from __future__ import annotations

import unittest
from unittest.mock import patch

from tools import expected_corpus_inventory


class ExpectedCorpusInventoryCleanRowTests(unittest.TestCase):
    def test_passing_rows_keep_empty_failed_checks(self) -> None:
        first = expected_corpus_inventory.ROOT / "expected_results" / "a.expected.json"
        second = expected_corpus_inventory.ROOT / "expected_results" / "b.expected.json"
        third = expected_corpus_inventory.ROOT / "expected_results" / "c.expected.json"
        with patch.object(expected_corpus_inventory, "EXPECTED_RESULTS") as expected_results:
            expected_results.exists.return_value = True
            expected_results.glob.return_value = [first, second, third]
            with patch.object(expected_corpus_inventory, "_run_fixture") as run_fixture:
                run_fixture.side_effect = [
                    {"fixture": "expected_results/a.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "", "stderr": ""},
                    {"fixture": "expected_results/b.expected.json", "passed": False, "returncode": 1, "failed_checks": ["decision"], "stdout": "", "stderr": "bad"},
                    {"fixture": "expected_results/c.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "", "stderr": ""},
                ]
                inventory = expected_corpus_inventory.build_inventory()

        passing_rows = [item for item in inventory["fixtures"] if item["passed"]]
        self.assertEqual(
            [(item["fixture"], item["failed_checks"]) for item in passing_rows],
            [("expected_results/a.expected.json", []), ("expected_results/c.expected.json", [])],
        )
        self.assertEqual(
            [(item["fixture"], item["failed_checks"]) for item in inventory["failed_fixtures"]],
            [("expected_results/b.expected.json", ["decision"])],
        )
        self.assertEqual(inventory["failed_fixture_count"], 1)
        self.assertEqual(inventory["spe_result"], "FAIL")


if __name__ == "__main__":
    unittest.main()
