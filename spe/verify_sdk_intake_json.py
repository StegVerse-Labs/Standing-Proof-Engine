#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.result_export import render_json
from spe.verify import PASS
from spe.verify_sdk_intake import verify_sdk_intake


def main(argv):
    if len(argv) != 2:
        print("usage: python spe/verify_sdk_intake_json.py <sdk_intake_receipt.json>", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    artifact = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    status, checks = verify_sdk_intake(artifact, repo_root)
    print(render_json(artifact, status, checks))
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
