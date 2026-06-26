#!/usr/bin/env python3
"""Write focused expected-corpus failure summaries from an inventory file."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(
            "usage: python tools/write_expected_corpus_failed_summary.py "
            "<inventory_json> <summary_json> <summary_md>",
            file=sys.stderr,
        )
        return 2

    inventory_path = Path(argv[1])
    summary_json_path = Path(argv[2])
    summary_md_path = Path(argv[3])

    data = json.loads(inventory_path.read_text(encoding="utf-8"))
    failed = data.get("failed_fixtures") or []

    summary = {
        "failed_fixture_count": len(failed),
        "failed_fixtures": failed,
    }
    summary_json_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = ["# Expected Corpus Failed Fixtures", "", f"Failed fixture count: {len(failed)}", ""]
    if failed:
        for item in failed:
            if isinstance(item, dict):
                name = item.get("fixture") or item.get("path") or "<unknown fixture>"
                lines.append(f"- `{name}`")
                for check in item.get("failed_checks") or []:
                    lines.append(f"  - {check}")
            else:
                lines.append(f"- `{item}`")
    else:
        lines.append("No failed fixtures reported.")

    summary_md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
