from __future__ import annotations

import contextlib
import io
import json
import subprocess
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

    def test_build_inventory_sorts_fixture_paths(self) -> None:
        first = expected_corpus_inventory.ROOT / "expected_results" / "a.expected.json"
        second = expected_corpus_inventory.ROOT / "expected_results" / "b.expected.json"
        with patch.object(expected_corpus_inventory, "EXPECTED_RESULTS") as expected_results:
            expected_results.exists.return_value = True
            expected_results.glob.return_value = [second, first]
            with patch.object(expected_corpus_inventory, "_run_fixture") as run_fixture:
                run_fixture.side_effect = [
                    {"fixture": "expected_results/a.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "", "stderr": ""},
                    {"fixture": "expected_results/b.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "", "stderr": ""},
                ]
                inventory = expected_corpus_inventory.build_inventory()

        self.assertEqual([item["fixture"] for item in inventory["fixtures"]], ["expected_results/a.expected.json", "expected_results/b.expected.json"])

    def test_build_inventory_counts_match_fixture_rows(self) -> None:
        first = expected_corpus_inventory.ROOT / "expected_results" / "a.expected.json"
        second = expected_corpus_inventory.ROOT / "expected_results" / "b.expected.json"
        with patch.object(expected_corpus_inventory, "EXPECTED_RESULTS") as expected_results:
            expected_results.exists.return_value = True
            expected_results.glob.return_value = [first, second]
            with patch.object(expected_corpus_inventory, "_run_fixture") as run_fixture:
                run_fixture.side_effect = [
                    {"fixture": "expected_results/a.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "", "stderr": ""},
                    {"fixture": "expected_results/b.expected.json", "passed": False, "returncode": 1, "failed_checks": ["verify_expected_result"], "stdout": "", "stderr": "bad"},
                ]
                inventory = expected_corpus_inventory.build_inventory()

        self.assertEqual(inventory["fixture_count"], len(inventory["fixtures"]))
        self.assertEqual(inventory["failed_fixture_count"], len(inventory["failed_fixtures"]))
        self.assertEqual(inventory["failed_fixtures"], [item for item in inventory["fixtures"] if not item["passed"]])
        self.assertEqual(inventory["spe_result"], "FAIL")

    def test_build_inventory_reports_pass_when_all_fixtures_pass(self) -> None:
        first = expected_corpus_inventory.ROOT / "expected_results" / "a.expected.json"
        second = expected_corpus_inventory.ROOT / "expected_results" / "b.expected.json"
        with patch.object(expected_corpus_inventory, "EXPECTED_RESULTS") as expected_results:
            expected_results.exists.return_value = True
            expected_results.glob.return_value = [first, second]
            with patch.object(expected_corpus_inventory, "_run_fixture") as run_fixture:
                run_fixture.side_effect = [
                    {"fixture": "expected_results/a.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "", "stderr": ""},
                    {"fixture": "expected_results/b.expected.json", "passed": True, "returncode": 0, "failed_checks": [], "stdout": "", "stderr": ""},
                ]
                inventory = expected_corpus_inventory.build_inventory()

        self.assertEqual(inventory["spe_result"], "PASS")
        self.assertEqual(inventory["fixture_count"], 2)
        self.assertEqual(inventory["failed_fixture_count"], 0)
        self.assertEqual(inventory["failed_fixtures"], [])

    def test_run_fixture_records_passing_result_row(self) -> None:
        fixture = expected_corpus_inventory.ROOT / "expected_results" / "example.expected.json"
        completed = subprocess.CompletedProcess(args=[], returncode=0, stdout="ok\n", stderr="")

        with patch.object(expected_corpus_inventory.subprocess, "run", return_value=completed):
            result = expected_corpus_inventory._run_fixture(fixture)

        self.assertEqual(result["fixture"], "expected_results/example.expected.json")
        self.assertEqual(result["passed"], True)
        self.assertEqual(result["returncode"], 0)
        self.assertEqual(result["failed_checks"], [])
        self.assertEqual(result["stdout"], "ok")
        self.assertEqual(result["stderr"], "")

    def test_run_fixture_records_failing_result_row(self) -> None:
        fixture = expected_corpus_inventory.ROOT / "expected_results" / "example.expected.json"
        completed = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="bad\n")

        with patch.object(expected_corpus_inventory.subprocess, "run", return_value=completed):
            result = expected_corpus_inventory._run_fixture(fixture)

        self.assertEqual(result["fixture"], "expected_results/example.expected.json")
        self.assertEqual(result["passed"], False)
        self.assertEqual(result["returncode"], 1)
        self.assertEqual(result["failed_checks"], ["verify_expected_result"])
        self.assertEqual(result["stdout"], "")
        self.assertEqual(result["stderr"], "bad")

    def test_main_prints_parseable_inventory_json(self) -> None:
        stdout = io.StringIO()
        payload = {
            "spe_result": "PASS",
            "fixture_count": 0,
            "failed_fixture_count": 0,
            "failed_fixtures": [],
            "fixtures": [],
        }
        with patch.object(expected_corpus_inventory, "build_inventory", return_value=payload):
            with contextlib.redirect_stdout(stdout):
                result = expected_corpus_inventory.main()

        self.assertEqual(result, 0)
        self.assertEqual(json.loads(stdout.getvalue()), payload)


if __name__ == "__main__":
    unittest.main()
