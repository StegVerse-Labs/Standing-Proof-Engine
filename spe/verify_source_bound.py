#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.result_export import render_json
from spe.source_hashes import verify_source_hash_bindings
from spe.verify import FAIL, PARTIAL, PASS, render, verify_artifact


def verify_source_bound_artifact(artifact: dict):
    status, checks = verify_artifact(artifact)
    source_checks = verify_source_hash_bindings(artifact)
    all_checks = checks + source_checks
    if any(check.status == FAIL for check in all_checks):
        return FAIL, all_checks
    if any(check.status == PARTIAL for check in all_checks):
        return PARTIAL, all_checks
    return status, all_checks


def main(argv: list[str]) -> int:
    json_output = False
    args = argv[1:]
    if args and args[0] == "--json":
        json_output = True
        args = args[1:]

    if len(args) != 1:
        print("usage: python spe/verify_source_bound.py [--json] <artifact.json>", file=sys.stderr)
        return 2

    artifact_path = Path(args[0])
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    status, checks = verify_source_bound_artifact(artifact)
    if json_output:
        print(render_json(artifact, status, checks))
    else:
        print(render(status, checks))
    return 0 if status in {PASS, PARTIAL} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
