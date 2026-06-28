#!/usr/bin/env python3
"""Run the SPE workflow-equivalent command sweep and report all failures."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports" / "sandbox-sweep"

COMMANDS = [
    [sys.executable, "-m", "spe.verify", "samples/pressure_demo_001.json"],
    [sys.executable, "-m", "spe.verify", "samples/stale_state_review_commit_001.json"],
    [sys.executable, "-m", "spe.verify", "samples/aegis_incident_standing_001.json"],
    [sys.executable, "-m", "spe.verify_manifest", "samples/manifest.json"],
    [sys.executable, "-m", "spe.verify_manifest", "samples/alane_commitment_candidate_manifest.json"],
    [sys.executable, "-m", "spe.verify_sdk_intake", "samples/sdk_intake_receipt_001.json"],
    [sys.executable, "-m", "spe.verify_sdk_intake", "samples/sdk_intake_cc_001.json"],
    [sys.executable, "-m", "spe.verify_pointer", "samples/master_records_pointer_001.json"],
    [sys.executable, "-m", "spe.verify_confirmation", "samples/master_records_confirmation_001.json"],
    [sys.executable, "-m", "spe.verify_destination_event", "samples/destination_event_001.json"],
    [sys.executable, "-m", "spe.verify_destination_event", "samples/destination_event_deferred_001.json"],
    [sys.executable, "-m", "spe.verify_event_replay", "samples/event_replay_001.json"],
    [sys.executable, "-m", "spe.verify_event_replay", "samples/event_replay_deferred_001.json"],
    [sys.executable, "-m", "spe.verify_source_bound", "samples/source_hash_bound_stale_state_001.json"],
    [sys.executable, "-m", "spe.verify_external_refs", "samples/external_source_ref_stale_state_001.json"],
    [sys.executable, "-m", "spe.verify_hash_manifest", "samples/hash_manifests/external_source_ref_stale_state_001.hashes.json"],
    [sys.executable, "-m", "tools.refresh_frozen_hashes", "--check"],
    [sys.executable, "-m", "spe.verify_heartbeat_path_selection", "samples/heartbeat_path_selection_001.json"],
    [sys.executable, "-m", "spe.verify_expected_corpus", "--json"],
    [sys.executable, "tools/run_repo_standing.py"],
    [sys.executable, "tools/run_repo_standing.py", "--json"],
    [sys.executable, "tools/expected_corpus_inventory.py"],
    [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
]


def run() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    rows = []
    for index, command in enumerate(COMMANDS, start=1):
        completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
        prefix = f"{index:03d}"
        command_text = " ".join(command)
        (REPORTS / f"{prefix}.command.txt").write_text(command_text + "\n", encoding="utf-8")
        (REPORTS / f"{prefix}.stdout.txt").write_text(completed.stdout, encoding="utf-8")
        (REPORTS / f"{prefix}.stderr.txt").write_text(completed.stderr, encoding="utf-8")
        (REPORTS / f"{prefix}.returncode.txt").write_text(f"{completed.returncode}\n", encoding="utf-8")
        rows.append(
            {
                "index": index,
                "command": command_text,
                "returncode": completed.returncode,
                "stdout_tail": completed.stdout[-2000:],
                "stderr_tail": completed.stderr[-2000:],
            }
        )
        print(f"{'PASS' if completed.returncode == 0 else 'FAIL'} {completed.returncode}: {command_text}")
    summary = {
        "command_count": len(rows),
        "failed_count": sum(1 for row in rows if row["returncode"] != 0),
        "failures": [row for row in rows if row["returncode"] != 0],
    }
    (REPORTS / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["failed_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(run())
