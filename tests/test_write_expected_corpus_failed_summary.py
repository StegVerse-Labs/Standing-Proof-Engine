from __future__ import annotations

import json
from pathlib import Path

from tools.write_expected_corpus_failed_summary import main


def test_write_expected_corpus_failed_summary(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.json"
    summary_json = tmp_path / "failed.json"
    summary_md = tmp_path / "failed.md"

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

    assert main(["write_expected_corpus_failed_summary.py", str(inventory), str(summary_json), str(summary_md)]) == 0

    summary = json.loads(summary_json.read_text(encoding="utf-8"))
    assert summary["failed_fixture_count"] == 1
    assert summary["failed_fixtures"][0]["fixture"] == "expected_results/example.expected.json"

    markdown = summary_md.read_text(encoding="utf-8")
    assert "# Expected Corpus Failed Fixtures" in markdown
    assert "Failed fixture count: 1" in markdown
    assert "`expected_results/example.expected.json`" in markdown
    assert "spe_result" in markdown
    assert "decision" in markdown


def test_write_expected_corpus_failed_summary_no_failures(tmp_path: Path) -> None:
    inventory = tmp_path / "inventory.json"
    summary_json = tmp_path / "failed.json"
    summary_md = tmp_path / "failed.md"

    inventory.write_text(json.dumps({"failed_fixtures": []}), encoding="utf-8")

    assert main(["write_expected_corpus_failed_summary.py", str(inventory), str(summary_json), str(summary_md)]) == 0

    summary = json.loads(summary_json.read_text(encoding="utf-8"))
    assert summary == {"failed_fixture_count": 0, "failed_fixtures": []}
    assert "No failed fixtures reported." in summary_md.read_text(encoding="utf-8")
