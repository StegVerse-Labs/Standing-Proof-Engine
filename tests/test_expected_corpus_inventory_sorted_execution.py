from __future__ import annotations

import unittest
from unittest.mock import patch

from tools import expected_corpus_inventory


class ExpectedCorpusInventorySortedExecutionTests(unittest.TestCase):
    def test_discovered_fixtures_are_sorted_before_execution(self) -> None:
        first = expected_corpus_inventory.ROOT / "expected_results" / "a.expected.json"
        second = expected_corpus_inventory.ROOT / "expected_results" / "b.expected.json"
        third = expected_corpus_inventory.ROOT / "expected_results" / "c.expected.json"
        with patch.object(expected_corpus_inventory, "EXPECTED_RESULTS") as expected_results:
            expected_results.exists.return_value = True
            expected_results.glob.return_value = [third, first, second]
            with patch.object(expected_corpus_inventory, "_run_fixture") as run_fixture:
                run_fixture.side_effect = [
                    {"fixture": "expected_results/a.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "a", "stderr": ""},
                    {"fixture": "expected_results/b.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "b", "stderr": ""},
                    {"fixture": "expected_results/c.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "c", "stderr": ""},
                ]
                inventory = expected_corpus_inventory.build_inventory()

        self.assertEqual([call.args[0] for call in run_fixture.call_args_list], [first, second, third])
        self.assertEqual(
            [item["fixture"] for item in inventory["fixtures"]],
            ["expected_results/a.expected.json", "expected_results/b.expected.json", "expected_results/c.expected.json"],
        )
        self.assertEqual(inventory["spe_result"], "PASS")
        self.assertEqual(inventory["fixture_count"], 3)


if __name__ == "__main__":
    unittest.main()
