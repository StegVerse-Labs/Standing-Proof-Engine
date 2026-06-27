from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from tools.write_expected_corpus_failed_summary import main


class ExpectedCorpusFailedSummaryWriterTests(unittest.TestCase):
    def test_write_expected_corpus_failed_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            inventory = root / "inventory.json"
            summary_json = root / "failed.json"
            summary_md = root / "failed.md"

            inventory.write_text(
                json.dumps(
                    {
                        "failed_fixtures": [
                            {
                                "fixture": "expected_results/example.expected.json",
                                "failed_checks": ["spe_result", "decision"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            self.assertEqual(
                main([
                    "write_expected_corpus_failed_summary.py",
                    str(inventory),
                    str(summary_json),
                    str(summary_md),
                ]),
                0,
            )

            summary = json.loads(summary_json.read_text(encoding="utf-8"))
            self.assertEqual(summary["failed_fixture_count"], 1)
            self.assertEqual(summary["failed_fixtures"][0]["fixture"], "expected_results/example.expected.json")

            markdown = summary_md.read_text(encoding="utf-8")
            self.assertIn("# Expected Corpus Failed Fixtures", markdown)
            self.assertIn("Failed fixture count: 1", markdown)
            self.assertIn("`expected_results/example.expected.json`", markdown)
            self.assertIn("spe_result", markdown)
            self.assertIn("decision", markdown)

    def test_write_expected_corpus_failed_summary_no_failures(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            inventory = root / "inventory.json"
            summary_json = root / "failed.json"
            summary_md = root / "failed.md"

            inventory.write_text(json.dumps({"failed_fixtures": []}), encoding="utf-8")

            self.assertEqual(
                main([
                    "write_expected_corpus_failed_summary.py",
                    str(inventory),
                    str(summary_json),
                    str(summary_md),
                ]),
                0,
            )

            summary = json.loads(summary_json.read_text(encoding="utf-8"))
            self.assertEqual(summary, {"failed_fixture_count": 0, "failed_fixtures": []})
            self.assertIn("No failed fixtures reported.", summary_md.read_text(encoding="utf-8"))

    def test_write_expected_corpus_failed_summary_usage_error(self) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            result = main(["write_expected_corpus_failed_summary.py"])

        self.assertEqual(result, 2)
        self.assertIn("usage: python tools/write_expected_corpus_failed_summary.py", stderr.getvalue())

    def test_write_expected_corpus_failed_summary_malformed_inventory_fails_loudly(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            inventory = root / "inventory.json"
            summary_json = root / "failed.json"
            summary_md = root / "failed.md"

            inventory.write_text("{not-json", encoding="utf-8")

            with self.assertRaises(json.JSONDecodeError):
                main([
                    "write_expected_corpus_failed_summary.py",
                    str(inventory),
                    str(summary_json),
                    str(summary_md),
                ])

            self.assertFalse(summary_json.exists())
            self.assertFalse(summary_md.exists())

    def test_write_expected_corpus_failed_summary_rejects_non_object_inventory_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            inventory = root / "inventory.json"
            summary_json = root / "failed.json"
            summary_md = root / "failed.md"

            inventory.write_text(json.dumps([{"failed_fixtures": []}]), encoding="utf-8")

            with self.assertRaisesRegex(TypeError, "inventory root"):
                main([
                    "write_expected_corpus_failed_summary.py",
                    str(inventory),
                    str(summary_json),
                    str(summary_md),
                ])

            self.assertFalse(summary_json.exists())
            self.assertFalse(summary_md.exists())

    def test_write_expected_corpus_failed_summary_rejects_non_list_failed_fixtures(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            inventory = root / "inventory.json"
            summary_json = root / "failed.json"
            summary_md = root / "failed.md"

            inventory.write_text(json.dumps({"failed_fixtures": "not-a-list"}), encoding="utf-8")

            with self.assertRaisesRegex(TypeError, "failed_fixtures"):
                main([
                    "write_expected_corpus_failed_summary.py",
                    str(inventory),
                    str(summary_json),
                    str(summary_md),
                ])

            self.assertFalse(summary_json.exists())
            self.assertFalse(summary_md.exists())

    def test_write_expected_corpus_failed_summary_rejects_non_object_failed_fixture_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            inventory = root / "inventory.json"
            summary_json = root / "failed.json"
            summary_md = root / "failed.md"

            inventory.write_text(json.dumps({"failed_fixtures": ["not-an-object"]}), encoding="utf-8")

            with self.assertRaisesRegex(TypeError, r"failed_fixtures\[0\]"):
                main([
                    "write_expected_corpus_failed_summary.py",
                    str(inventory),
                    str(summary_json),
                    str(summary_md),
                ])

            self.assertFalse(summary_json.exists())
            self.assertFalse(summary_md.exists())


if __name__ == "__main__":
    unittest.main()
