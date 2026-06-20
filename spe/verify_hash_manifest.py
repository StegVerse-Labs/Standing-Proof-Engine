#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.result_export import canonical_sha256
from spe.verify import FAIL, PASS, Check, render


def verify_hash_manifest(manifest, repo_root):
    bindings = manifest.get("bindings")
    if not isinstance(bindings, dict):
        return FAIL, [Check("parse_manifest", FAIL, "bindings section missing")]

    checks = [Check("parse_manifest", PASS, "hash manifest contains bindings")]
    for binding_name, binding in bindings.items():
        if not isinstance(binding, dict):
            checks.append(Check(binding_name, FAIL, "binding is not an object"))
            continue

        source_ref = binding.get("source_ref")
        expected_hash = binding.get("sha256")
        if not isinstance(source_ref, str) or not isinstance(expected_hash, str):
            checks.append(Check(binding_name, FAIL, "source_ref or sha256 missing"))
            continue

        source_path = (repo_root / source_ref).resolve()
        try:
            source_path.relative_to(repo_root.resolve())
        except ValueError:
            checks.append(Check(binding_name, FAIL, "source_ref escapes repo root"))
            continue

        try:
            source_object = json.loads(source_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            checks.append(Check(binding_name, FAIL, "source_ref not found"))
            continue
        except json.JSONDecodeError:
            checks.append(Check(binding_name, FAIL, "source_ref is not valid json"))
            continue

        actual_hash = canonical_sha256(source_object)
        if actual_hash != expected_hash:
            checks.append(Check(binding_name, FAIL, f"expected {expected_hash}, got {actual_hash}"))
        else:
            checks.append(Check(binding_name, PASS, "literal hash matches canonical source object"))

    if any(check.status == FAIL for check in checks):
        return FAIL, checks
    return PASS, checks


def main(argv):
    if len(argv) != 2:
        print("usage: python spe/verify_hash_manifest.py <manifest.json>", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    manifest_path = Path(argv[1])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    status, checks = verify_hash_manifest(manifest, repo_root)
    print(render(status, checks))
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
