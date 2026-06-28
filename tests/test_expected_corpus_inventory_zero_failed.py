from __future__ import annotations

import unittest
from unittest.mock import patch

from tools import expected_corpus_inventory


class ExpectedCorpusInventoryZeroFailedTests(unittest.TestCase):
    def test_zero_failed_count_with_multiple_passing_rows(self) -> None:
        first = expected_corpus_inventory.ROOT / "expected_results" / "a.expected.json"
        second = expected_corpus_inventory.ROOT / "expected_results" / "b.expected.json"
        third = expected_corpus_inventory.ROOT / "expected_results" / "c.expected.json"
        with patch.object(expected_corpus_inventory, "EXPECTED_RESULTS") as expected_results:
            expected_results.exists.return_value = True
            expected_results.glob.return_value = [first, second, third]
            with patch.object(expected_corpus_inventory, "_run_fixture") as run_fixture:
                run_fixture.side_effect = [
                    {"fixture": "expected_results/a.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "a-out", "stderr": ""},
                    {"fixture": "expected_results/b.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "b-out", "stderr": ""},
                    {"fixture": "expected_results/c.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "c-out", "stderr": ""},
                ]
                inventory = expected_corpus_inventory.build_inventory()

        self.assertEqual(inventory["spe_result"], "PASS")
        self.assertEqual(inventory["fixture_count"], 3)
        self.assertEqual(inventory["failed_fixture_count"], 0)
        self.assertEqual(inventory["failed_fixtures"], [])
        self.assertEqual(
            [(item["fixture"], item["passed"], item["stdout"]) for item in inventory["fixtures"]],
            [
                ("expected_results/a.expected.json", True, "a-out"),
                ("expected_results/b.expected.json", True, "b-out"),
                ("expected_results/c.expected.json", True, "c-out"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
