from __future__ import annotations

import unittest
from unittest.mock import patch

from tools import expected_corpus_inventory


class ExpectedCorpusInventoryPassFlagTests(unittest.TestCase):
    def test_pass_flags_remain_tied_to_fixture_rows(self) -> None:
        first = expected_corpus_inventory.ROOT / "expected_results" / "a.expected.json"
        second = expected_corpus_inventory.ROOT / "expected_results" / "b.expected.json"
        third = expected_corpus_inventory.ROOT / "expected_results" / "c.expected.json"
        with patch.object(expected_corpus_inventory, "EXPECTED_RESULTS") as expected_results:
            expected_results.exists.return_value = True
            expected_results.glob.return_value = [first, second, third]
            with patch.object(expected_corpus_inventory, "_run_fixture") as run_fixture:
                run_fixture.side_effect = [
                    {"fixture": "expected_results/a.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "", "stderr": ""},
                    {"fixture": "expected_results/b.expected.json", "passed": False, "returncode": 1, "failed_checks": ["spe_result"], "stdout": "", "stderr": ""},
                    {"fixture": "expected_results/c.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "", "stderr": ""},
                ]
                inventory = expected_corpus_inventory.build_inventory()

        self.assertEqual(
            [(item["fixture"], item["passed"]) for item in inventory["fixtures"]],
            [
                ("expected_results/a.expected.json", True),
                ("expected_results/b.expected.json", False),
                ("expected_results/c.expected.json", True),
            ],
        )
        self.assertEqual(
            [(item["fixture"], item["passed"]) for item in inventory["failed_fixtures"]],
            [("expected_results/b.expected.json", False)],
        )
        self.assertEqual(inventory["failed_fixture_count"], 1)
        self.assertEqual(inventory["spe_result"], "FAIL")


if __name__ == "__main__":
    unittest.main()
