#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.result_export import canonical_sha256
from spe.verify import FAIL, PASS, Check, render
from spe.verify_manifest import verify_manifest


def verify_pointer(pointer, repo_root):
    checks = []
    required = ["pointer_id", "pointer_type", "source_receipt", "source_receipt_sha256", "route_manifest", "route_manifest_sha256"]
    missing = [key for key in required if not pointer.get(key)]
    if missing:
        return FAIL, [Check("parse_pointer", FAIL, f"missing fields: {', '.join(missing)}")]

    checks.append(Check("parse_pointer", PASS, "pointer parsed"))

    source = json.loads((repo_root / pointer["source_receipt"]).read_text(encoding="utf-8"))
    source_ok = canonical_sha256(source) == pointer["source_receipt_sha256"]
    checks.append(Check("source_hash_binding", PASS if source_ok else FAIL, "source hash checked"))

    manifest_path = repo_root / pointer["route_manifest"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_ok = canonical_sha256(manifest) == pointer["route_manifest_sha256"]
    checks.append(Check("manifest_hash_binding", PASS if manifest_ok else FAIL, "manifest hash checked"))

    target = pointer.get("reconstruction_target", {})
    manifest_status, manifest_report = verify_manifest(manifest_path)
    target_ok = target.get("expected_package_status") == manifest_status and target.get("expected_sample_count") == manifest_report.get("sample_count")
    checks.append(Check("target_binding", PASS if target_ok else FAIL, "target checked"))

    status = FAIL if any(check.status == FAIL for check in checks) else PASS
    return status, checks


def main(argv):
    if len(argv) != 2:
        print("usage: python spe/verify_pointer.py <pointer.json>", file=sys.stderr)
        return 2
    repo_root = Path(__file__).resolve().parents[1]
    pointer = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    status, checks = verify_pointer(pointer, repo_root)
    print(render(status, checks))
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
