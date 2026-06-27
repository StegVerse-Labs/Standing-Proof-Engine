from __future__ import annotations

import unittest
from unittest.mock import patch

from tools import expected_corpus_inventory


class MixedExpectedCorpusInventoryTests(unittest.TestCase):
    def test_mixed_pass_and_multiple_failures_preserve_rows(self) -> None:
        first = expected_corpus_inventory.ROOT / "expected_results" / "a.expected.json"
        second = expected_corpus_inventory.ROOT / "expected_results" / "b.expected.json"
        third = expected_corpus_inventory.ROOT / "expected_results" / "c.expected.json"
        with patch.object(expected_corpus_inventory, "EXPECTED_RESULTS") as expected_results:
            expected_results.exists.return_value = True
            expected_results.glob.return_value = [first, second, third]
            with patch.object(expected_corpus_inventory, "_run_fixture") as run_fixture:
                run_fixture.side_effect = [
                    {"fixture": "expected_results/a.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "", "stderr": ""},
                    {"fixture": "expected_results/b.expected.json", "passed": False, "returncode": 1, "failed_checks": ["spe_result"], "stdout": "", "stderr": "bad-b"},
                    {"fixture": "expected_results/c.expected.json", "passed": False, "returncode": 1, "failed_checks": ["decision"], "stdout": "", "stderr": "bad-c"},
                ]
                inventory = expected_corpus_inventory.build_inventory()

        self.assertEqual(inventory["spe_result"], "FAIL")
        self.assertEqual(inventory["fixture_count"], 3)
        self.assertEqual(inventory["failed_fixture_count"], 2)
        self.assertEqual(
            [item["fixture"] for item in inventory["failed_fixtures"]],
            ["expected_results/b.expected.json", "expected_results/c.expected.json"],
        )
        self.assertEqual(
            [item["fixture"] for item in inventory["fixtures"]],
            ["expected_results/a.expected.json", "expected_results/b.expected.json", "expected_results/c.expected.json"],
        )


if __name__ == "__main__":
    unittest.main()
