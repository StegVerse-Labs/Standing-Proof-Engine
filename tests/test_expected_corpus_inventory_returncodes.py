from __future__ import annotations

import unittest
from unittest.mock import patch

from tools import expected_corpus_inventory


class ExpectedCorpusInventoryReturnCodeTests(unittest.TestCase):
    def test_return_codes_remain_tied_to_fixture_rows(self) -> None:
        first = expected_corpus_inventory.ROOT / "expected_results" / "a.expected.json"
        second = expected_corpus_inventory.ROOT / "expected_results" / "b.expected.json"
        with patch.object(expected_corpus_inventory, "EXPECTED_RESULTS") as expected_results:
            expected_results.exists.return_value = True
            expected_results.glob.return_value = [first, second]
            with patch.object(expected_corpus_inventory, "_run_fixture") as run_fixture:
                run_fixture.side_effect = [
                    {"fixture": "expected_results/a.expected.json", "passed": False, "returncode": 1, "failed_checks": ["spe_result"], "stdout": "", "stderr": ""},
                    {"fixture": "expected_results/b.expected.json", "passed": False, "returncode": 2, "failed_checks": ["decision"], "stdout": "", "stderr": ""},
                ]
                inventory = expected_corpus_inventory.build_inventory()

        self.assertEqual(
            [(item["fixture"], item["returncode"]) for item in inventory["failed_fixtures"]],
            [("expected_results/a.expected.json", 1), ("expected_results/b.expected.json", 2)],
        )
        self.assertEqual(inventory["failed_fixture_count"], 2)
        self.assertEqual(inventory["spe_result"], "FAIL")


if __name__ == "__main__":
    unittest.main()
