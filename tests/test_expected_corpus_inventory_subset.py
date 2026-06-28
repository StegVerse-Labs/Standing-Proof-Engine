from __future__ import annotations

import unittest
from unittest.mock import patch

from tools import expected_corpus_inventory


class ExpectedCorpusInventorySubsetTests(unittest.TestCase):
    def test_failed_fixtures_are_filtered_fixture_rows(self) -> None:
        first = expected_corpus_inventory.ROOT / "expected_results" / "a.expected.json"
        second = expected_corpus_inventory.ROOT / "expected_results" / "b.expected.json"
        third = expected_corpus_inventory.ROOT / "expected_results" / "c.expected.json"
        with patch.object(expected_corpus_inventory, "EXPECTED_RESULTS") as expected_results:
            expected_results.exists.return_value = True
            expected_results.glob.return_value = [first, second, third]
            with patch.object(expected_corpus_inventory, "_run_fixture") as run_fixture:
                run_fixture.side_effect = [
                    {"fixture": "expected_results/a.expected.json", "passed": False, "returncode": 1, "failed_checks": ["spe_result"], "stdout": "a-out", "stderr": "a-err"},
                    {"fixture": "expected_results/b.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "b-out", "stderr": ""},
                    {"fixture": "expected_results/c.expected.json", "passed": False, "returncode": 2, "failed_checks": ["decision"], "stdout": "c-out", "stderr": "c-err"},
                ]
                inventory = expected_corpus_inventory.build_inventory()

        filtered = [item for item in inventory["fixtures"] if not item["passed"]]
        self.assertEqual(inventory["failed_fixtures"], filtered)
        self.assertEqual(inventory["failed_fixture_count"], len(filtered))
        self.assertEqual(
            [(item["fixture"], item["returncode"], item["failed_checks"], item["stdout"], item["stderr"]) for item in inventory["failed_fixtures"]],
            [
                ("expected_results/a.expected.json", 1, ["spe_result"], "a-out", "a-err"),
                ("expected_results/c.expected.json", 2, ["decision"], "c-out", "c-err"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
