#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys

CHECKS = [
    [sys.executable, "-m", "spe.check_tt_authority_manifest"],
    [sys.executable, "-m", "spe.check_tt_support_manifest"],
    [sys.executable, "-m", "spe.check_tt_full_snapshot"],
    [
        sys.executable,
        "-m",
        "spe.check_full_snapshot_cases",
        "samples/alane_commitment_candidate_manifest.json",
    ],
    [
        sys.executable,
        "-m",
        "spe.verify_tt_support_cases",
        "samples/tt_support_transition_cases_manifest.json",
    ],
    [
        sys.executable,
        "-m",
        "spe.verify_commitment_candidate_receipt_chain",
        "samples/commitment_candidate_receipt_chain_expectation.json",
    ],
    [
        sys.executable,
        "-m",
        "spe.verify_tt_manifest",
        "samples/alane_commitment_candidate_manifest.json",
    ],
    [
        sys.executable,
        "-m",
        "spe.verify_manifest",
        "samples/alane_commitment_candidate_manifest.json",
    ],
    [sys.executable, "-m", "spe.check_spe_tt_activation_goal"],
    [sys.executable, "-m", "spe.write_tt_goal_status"],
    [sys.executable, "-m", "spe.check_no_manual_tt_tasks"],
    [sys.executable, "-m", "spe.check_propagation_targets"],
]


def main() -> int:
    failed: list[str] = []
    for command in CHECKS:
        label = " ".join(command)
        print(f"\n=== {label} ===", flush=True)
        result = subprocess.run(command, text=True, check=False)
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
