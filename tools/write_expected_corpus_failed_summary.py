#!/usr/bin/env python3
"""Write focused expected-corpus failure summaries from an inventory file."""
from __future__ import annotations

import json
import sys
from pathlib import Path

Scalar = str | int | float | bool | None


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
    if not isinstance(data, dict):
        raise TypeError("expected inventory root to be an object")

    failed = data.get("failed_fixtures") or []
    if not isinstance(failed, list):
        raise TypeError("expected 'failed_fixtures' to be a list")
    for index, item in enumerate(failed):
        if not isinstance(item, dict):
            raise TypeError(f"expected failed_fixtures[{index}] to be an object")
        failed_checks = item.get("failed_checks") or []
        if not isinstance(failed_checks, list):
            raise TypeError(f"expected failed_fixtures[{index}].failed_checks to be a list")
        for check_index, check in enumerate(failed_checks):
            if not isinstance(check, (str, int, float, bool)) and check is not None:
                raise TypeError(
                    f"expected failed_fixtures[{index}].failed_checks[{check_index}] to be scalar"
                )

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
            name = item.get("fixture") or item.get("path") or "<unknown fixture>"
            lines.append(f"- `{name}`")
            for check in item.get("failed_checks") or []:
                lines.append(f"  - {check}")
    else:
        lines.append("No failed fixtures reported.")

    summary_md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
