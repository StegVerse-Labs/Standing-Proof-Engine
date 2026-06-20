#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.result_export import render_json
from spe.source_hashes import verify_source_hash_bindings, with_resolved_source_refs
from spe.verify import FAIL, PARTIAL, PASS, render, verify_artifact


def combined_status(base_status, checks):
    if any(check.status == FAIL for check in checks):
        return FAIL
    if base_status == PARTIAL or any(check.status == PARTIAL for check in checks):
        return PARTIAL
    return base_status


def verify_external_ref_artifact(artifact, repo_root):
    resolved_artifact, ref_checks = with_resolved_source_refs(artifact, repo_root)
    status, checks = verify_artifact(resolved_artifact)
    source_checks = verify_source_hash_bindings(resolved_artifact)
    all_checks = ref_checks + checks + source_checks
    return combined_status(status, all_checks), all_checks


def main(argv):
    json_output = False
    args = argv[1:]
    if args and args[0] == "--json":
        json_output = True
        args = args[1:]

    if len(args) != 1:
        print("usage: python spe/verify_external_refs.py [--json] <artifact.json>", file=sys.stderr)
        return 2

    artifact_path = Path(args[0])
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    repo_root = Path(__file__).resolve().parents[1]
    status, checks = verify_external_ref_artifact(artifact, repo_root)

    if json_output:
        print(render_json(artifact, status, checks))
    else:
        print(render(status, checks))

    return 0 if status in {PASS, PARTIAL} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
