from __future__ import annotations

import unittest
from unittest.mock import patch

from tools import expected_corpus_inventory


class ExpectedCorpusInventoryTests(unittest.TestCase):
    def test_build_inventory_empty_directory_shape(self) -> None:
        with patch.object(expected_corpus_inventory, "EXPECTED_RESULTS") as expected_results:
            expected_results.exists.return_value = False

            inventory = expected_corpus_inventory.build_inventory()

        self.assertEqual(inventory["spe_result"], "PASS")
        self.assertEqual(inventory["fixture_count"], 0)
        self.assertEqual(inventory["failed_fixture_count"], 0)
        self.assertEqual(inventory["failed_fixtures"], [])
        self.assertEqual(inventory["fixtures"], [])

    def test_build_inventory_records_failed_fixture(self) -> None:
        fixture = expected_corpus_inventory.ROOT / "expected_results" / "example.expected.json"
        with patch.object(expected_corpus_inventory, "EXPECTED_RESULTS") as expected_results:
            expected_results.exists.return_value = True
            expected_results.glob.return_value = [fixture]
            with patch.object(expected_corpus_inventory, "_run_fixture") as run_fixture:
                run_fixture.return_value = {
                    "fixture": "expected_results/example.expected.json",
                    "passed": False,
                    "returncode": 1,
                    "failed_checks": ["verify_expected_result"],
                    "stdout": "",
                    "stderr": "boom",
                }
                inventory = expected_corpus_inventory.build_inventory()

        self.assertEqual(inventory["spe_result"], "FAIL")
        self.assertEqual(inventory["fixture_count"], 1)
        self.assertEqual(inventory["failed_fixture_count"], 1)
        self.assertEqual(inventory["failed_fixtures"], inventory["fixtures"])
        self.assertEqual(inventory["failed_fixtures"][0]["fixture"], "expected_results/example.expected.json")


if __name__ == "__main__":
    unittest.main()
