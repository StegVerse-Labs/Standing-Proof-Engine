#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.result_export import canonical_sha256
from spe.verify import FAIL, PASS, Check, render
from spe.verify_destination_event import verify_destination_event


def verify_event_replay(replay, repo_root):
    required = [
        "replay_id",
        "replay_type",
        "source_event",
        "source_event_sha256",
        "observed_result",
        "expected_result",
        "replay_result",
    ]
    missing = [key for key in required if not replay.get(key)]
    if missing:
        return FAIL, [Check("parse_event_replay", FAIL, f"missing fields: {', '.join(missing)}")]

    checks = [Check("parse_event_replay", PASS, "event replay parsed")]

    event_path = repo_root / replay["source_event"]
    event = json.loads(event_path.read_text(encoding="utf-8"))
    event_hash = canonical_sha256(event)
    hash_ok = event_hash == replay.get("source_event_sha256")
    checks.append(Check("source_event_hash_binding", PASS if hash_ok else FAIL, "source event hash checked"))

    event_status, _ = verify_destination_event(event, repo_root)
    checks.append(Check("source_event_verifies", PASS if event_status == PASS else FAIL, "source event verifier checked"))

    result_ok = replay.get("observed_result") == replay.get("expected_result") == event.get("event_result")
    checks.append(Check("replay_result_binding", PASS if result_ok else FAIL, "replay result checked"))

    handoff_ok = all(replay.get(key) is True for key in ["event_bound", "result_replayed", "final_state_known"])
    checks.append(Check("replay_handoff_flags", PASS if handoff_ok else FAIL, "replay handoff flags checked"))

    status = FAIL if any(check.status == FAIL for check in checks) else PASS
    return status, checks


def main(argv):
    if len(argv) != 2:
        print("usage: python spe/verify_event_replay.py <event_replay.json>", file=sys.stderr)
        return 2
    repo_root = Path(__file__).resolve().parents[1]
    replay = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    status, checks = verify_event_replay(replay, repo_root)
    print(render(status, checks))
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
