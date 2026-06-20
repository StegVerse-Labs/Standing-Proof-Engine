#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.result_export import render_json
from spe.verify import FAIL, PARTIAL, PASS, verify_artifact


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python spe/verify_json.py <artifact.json>", file=sys.stderr)
        return 2

    artifact_path = Path(argv[1])
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    status, checks = verify_artifact(artifact)
    print(render_json(artifact, status, checks))
    return 0 if status in {PASS, PARTIAL} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
