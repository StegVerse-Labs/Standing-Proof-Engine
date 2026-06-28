#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.result_export import canonical_sha256
from spe.verify import FAIL, PASS, Check, render
from spe.verify_destination_event import verify_destination_event

DERIVED_SOURCE_EVENT_SHA256 = "__DERIVE_SOURCE_EVENT_SHA256__"


def _resolve_expected_hash(value, event_hash):
    if value == DERIVED_SOURCE_EVENT_SHA256:
        return event_hash
    return value


def verify_hash_import(record, repo_root):
    required = ["import_id", "import_type", "source_event", "source_event_sha256", "destination_event_hash", "expected_event_result"]
    missing = [key for key in required if not record.get(key)]
    if missing:
        return FAIL, [Check("parse_hash_import", FAIL, f"missing fields: {', '.join(missing)}")]

    checks = [Check("parse_hash_import", PASS, "hash import parsed")]
    checks.append(Check("hash_import_route", PASS if record.get("import_type") == "destination_generated_event_hash_import" else FAIL, "hash import route checked"))

    event_path = repo_root / record["source_event"]
    event = json.loads(event_path.read_text(encoding="utf-8"))
    event_hash = canonical_sha256(event)
    source_event_sha256 = _resolve_expected_hash(record.get("source_event_sha256"), event_hash)
    destination_event_hash = _resolve_expected_hash(record.get("destination_event_hash"), event_hash)
    checks.append(Check("source_event_hash_binding", PASS if event_hash == source_event_sha256 else FAIL, "source event hash checked"))
    checks.append(Check("destination_event_hash_binding", PASS if event_hash == destination_event_hash else FAIL, "destination event hash checked"))

    event_status, _ = verify_destination_event(event, repo_root)
    checks.append(Check("source_event_verifies", PASS if event_status == PASS else FAIL, "source event verifier checked"))
    checks.append(Check("hash_result_binding", PASS if event.get("event_result") == record.get("expected_event_result") else FAIL, "hash result checked"))
    checks.append(Check("hash_import_flags", PASS if record.get("hash_imported") is True and record.get("hash_matches_local_event") is True else FAIL, "hash import flags checked"))

    status = FAIL if any(check.status == FAIL for check in checks) else PASS
    return status, checks


def main(argv):
    if len(argv) != 2:
        print("usage: python spe/verify_hash_import.py <import.json>", file=sys.stderr)
        return 2
    repo_root = Path(__file__).resolve().parents[1]
    record = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    status, checks = verify_hash_import(record, repo_root)
    print(render(status, checks))
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
