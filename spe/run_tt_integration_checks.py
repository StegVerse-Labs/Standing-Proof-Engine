#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys

CHECKS = [
    [sys.executable, "spe/check_tt_authority_manifest.py"],
    [sys.executable, "spe/check_tt_support_manifest.py"],
    [sys.executable, "spe/check_tt_full_snapshot.py"],
    [sys.executable, "spe/check_full_snapshot_cases.py", "samples/alane_commitment_candidate_manifest.json"],
    [sys.executable, "spe/verify_tt_support_cases.py", "samples/tt_support_transition_cases_manifest.json"],
    [sys.executable, "spe/verify_commitment_candidate_receipt_chain.py", "samples/commitment_candidate_receipt_chain_expectation.json"],
    [sys.executable, "spe/verify_tt_manifest.py", "samples/alane_commitment_candidate_manifest.json"],
    [sys.executable, "spe/verify_manifest.py", "samples/alane_commitment_candidate_manifest.json"],
    [sys.executable, "spe/check_spe_tt_activation_goal.py"],
    [sys.executable, "spe/write_tt_goal_status.py"],
    [sys.executable, "spe/check_no_manual_tt_tasks.py"],
]


def main() -> int:
    failed = []
    for command in CHECKS:
        label = " ".join(command)
        print(f"\n=== {label} ===")
        result = subprocess.run(command, text=True)
        if result.returncode != 0:
            failed.append(label)
    if failed:
        print("\nSPE TT INTEGRATION: FAIL")
        for item in failed:
            print(f"- {item}")
        return 1
    print("\nSPE TT INTEGRATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
