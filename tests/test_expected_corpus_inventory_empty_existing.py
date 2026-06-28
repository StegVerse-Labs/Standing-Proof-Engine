from __future__ import annotations

import unittest
from unittest.mock import patch

from tools import expected_corpus_inventory


class ExpectedCorpusInventoryExistingEmptyTests(unittest.TestCase):
    def test_existing_empty_expected_results_directory_does_not_run_fixtures(self) -> None:
        with patch.object(expected_corpus_inventory, "EXPECTED_RESULTS") as expected_results:
            expected_results.exists.return_value = True
            expected_results.glob.return_value = []
            with patch.object(expected_corpus_inventory, "_run_fixture") as run_fixture:
                inventory = expected_corpus_inventory.build_inventory()

        expected_results.glob.assert_called_once_with("*.expected.json")
        run_fixture.assert_not_called()
        self.assertEqual(inventory["spe_result"], "PASS")
        self.assertEqual(inventory["fixture_count"], 0)
        self.assertEqual(inventory["failed_fixture_count"], 0)
        self.assertEqual(inventory["fixtures"], [])
        self.assertEqual(inventory["failed_fixtures"], [])


if __name__ == "__main__":
    unittest.main()
