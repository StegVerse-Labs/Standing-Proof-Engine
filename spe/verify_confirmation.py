#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.result_export import canonical_sha256
from spe.verify import FAIL, PASS, Check, render
from spe.verify_pointer import verify_pointer


def verify_confirmation(confirmation, repo_root):
    required = [
        "confirmation_id",
        "confirmation_type",
        "origin_repo",
        "destination_repo",
        "source_pointer",
        "source_pointer_sha256",
        "confirmation_result",
    ]
    missing = [key for key in required if not confirmation.get(key)]
    if missing:
        return FAIL, [Check("parse_confirmation", FAIL, f"missing fields: {', '.join(missing)}")]

    checks = [Check("parse_confirmation", PASS, "confirmation parsed")]

    route_ok = (
        confirmation.get("confirmation_type") == "master_records_pointer_confirmation"
        and confirmation.get("origin_repo") == "master-records/core-lite"
        and confirmation.get("destination_repo") == "StegVerse-Labs/Standing-Proof-Engine"
    )
    checks.append(Check("confirmation_route", PASS if route_ok else FAIL, "confirmation route checked"))

    pointer_path = repo_root / confirmation["source_pointer"]
    pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
    pointer_hash = canonical_sha256(pointer)
    hash_ok = pointer_hash == confirmation.get("source_pointer_sha256")
    checks.append(Check("source_pointer_hash_binding", PASS if hash_ok else FAIL, "source pointer hash checked"))

    pointer_status, _ = verify_pointer(pointer, repo_root)
    checks.append(Check("source_pointer_verifies", PASS if pointer_status == PASS else FAIL, "source pointer verifier checked"))

    accepted = (
        confirmation.get("confirmation_result") == "ACCEPTED_FOR_RECONSTRUCTION"
        and confirmation.get("installed") is True
        and confirmation.get("reconstruction_available") is True
    )
    checks.append(Check("confirmation_result_binding", PASS if accepted else FAIL, "confirmation result checked"))

    target = pointer.get("reconstruction_target", {})
    target_ok = (
        confirmation.get("expected_package_status") == target.get("expected_package_status")
        and confirmation.get("expected_sample_count") == target.get("expected_sample_count")
    )
    checks.append(Check("confirmation_target_binding", PASS if target_ok else FAIL, "confirmation target checked"))

    status = FAIL if any(check.status == FAIL for check in checks) else PASS
    return status, checks


def main(argv):
    if len(argv) != 2:
        print("usage: python spe/verify_confirmation.py <confirmation.json>", file=sys.stderr)
        return 2
    repo_root = Path(__file__).resolve().parents[1]
    confirmation = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    status, checks = verify_confirmation(confirmation, repo_root)
    print(render(status, checks))
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
