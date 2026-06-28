from __future__ import annotations

import unittest
from unittest.mock import patch

from tools import expected_corpus_inventory


class ExpectedCorpusInventoryDiscoveryTests(unittest.TestCase):
    def test_existing_expected_results_directory_uses_expected_json_pattern(self) -> None:
        fixture = expected_corpus_inventory.ROOT / "expected_results" / "case.expected.json"
        with patch.object(expected_corpus_inventory, "EXPECTED_RESULTS") as expected_results:
            expected_results.exists.return_value = True
            expected_results.glob.return_value = [fixture]
            with patch.object(expected_corpus_inventory, "_run_fixture") as run_fixture:
                run_fixture.return_value = {
                    "fixture": "expected_results/case.expected.json",
                    "passed": True,
                    "returncode": 0,
                    "failed_checks": [],
                    "stdout": "ok",
                    "stderr": "",
                }
                inventory = expected_corpus_inventory.build_inventory()

        expected_results.glob.assert_called_once_with("*.expected.json")
        run_fixture.assert_called_once_with(fixture)
        self.assertEqual(inventory["spe_result"], "PASS")
        self.assertEqual(inventory["fixture_count"], 1)
        self.assertEqual(inventory["failed_fixture_count"], 0)
        self.assertEqual(inventory["failed_fixtures"], [])


if __name__ == "__main__":
    unittest.main()
