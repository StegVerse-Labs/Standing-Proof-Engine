#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.result_export import canonical_sha256
from spe.verify import FAIL, PASS, Check, render
from spe.verify_confirmation import verify_confirmation


def verify_destination_event(event, repo_root):
    required = [
        "event_id",
        "event_type",
        "origin_repo",
        "destination_repo",
        "source_confirmation",
        "source_confirmation_sha256",
        "event_result",
    ]
    missing = [key for key in required if not event.get(key)]
    if missing:
        return FAIL, [Check("parse_destination_event", FAIL, f"missing fields: {', '.join(missing)}")]

    checks = [Check("parse_destination_event", PASS, "destination event parsed")]

    route_ok = event.get("event_type") == "destination_confirmation_event"
    checks.append(Check("destination_event_route", PASS if route_ok else FAIL, "destination event route checked"))

    confirmation_path = repo_root / event["source_confirmation"]
    confirmation = json.loads(confirmation_path.read_text(encoding="utf-8"))
    confirmation_hash = canonical_sha256(confirmation)
    hash_ok = confirmation_hash == event.get("source_confirmation_sha256")
    checks.append(Check("source_confirmation_hash_binding", PASS if hash_ok else FAIL, "source confirmation hash checked"))

    confirmation_status, _ = verify_confirmation(confirmation, repo_root)
    checks.append(Check("source_confirmation_verifies", PASS if confirmation_status == PASS else FAIL, "source confirmation verifier checked"))

    result_ok = event.get("event_result") in {"INSTALLED", "NOT_INSTALLED"} and event.get("event_hash_declared") is True
    checks.append(Check("destination_event_result_binding", PASS if result_ok else FAIL, "destination event result checked"))

    target_ok = event.get("expected_package_status") == confirmation.get("expected_package_status")
    checks.append(Check("destination_event_target_binding", PASS if target_ok else FAIL, "destination event target checked"))

    status = FAIL if any(check.status == FAIL for check in checks) else PASS
    return status, checks


def main(argv):
    if len(argv) != 2:
        print("usage: python spe/verify_destination_event.py <destination_event.json>", file=sys.stderr)
        return 2
    repo_root = Path(__file__).resolve().parents[1]
    event = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    status, checks = verify_destination_event(event, repo_root)
    print(render(status, checks))
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
