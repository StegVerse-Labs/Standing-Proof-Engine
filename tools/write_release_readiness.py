#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


REQUIRED_FILES = [
    "SPE_MIRROR_HANDOFF.md",
    "docs/release_snapshot_v0_3_0.md",
    "docs/propagation_verification_task_v0_3_0.md",
    "docs/destination_hash_import_binding.md",
    "samples/destination_generated_event_hash_001.json",
    "spe/verify_hash_import.py",
    "tests/test_hash_import.py",
    "expected_results/hash_import_001.expected.json",
]

REMAINING_EXTERNAL_TARGETS = [
    "master-records/core-lite -> destination-generated receipt chain",
    "StegVerse-Labs/Site -> public release/status update",
    "GCAT-BCAT-Engine/Publisher -> publication route update",
    "admissibility-wiki -> standing/admissibility update",
    "stegguardian-wiki -> guardian standing-boundary update",
]


def status_for(repo_root: Path) -> dict[str, object]:
    files = []
    for path in REQUIRED_FILES:
        exists = (repo_root / path).exists()
        files.append({"path": path, "present": exists})

    ready = all(item["present"] for item in files)
    return {
        "release_candidate": "v0.4.0",
        "spe_release_readiness": "READY" if ready else "NOT_READY",
        "required_files": files,
        "remaining_external_targets": REMAINING_EXTERNAL_TARGETS,
        "manual_internal_tasks": [],
        "manual_external_tasks": REMAINING_EXTERNAL_TARGETS,
        "non_claim": "Release readiness confirms local SPE artifacts only; it does not claim downstream propagation or destination-generated receipt-chain completion.",
    }


def render_markdown(payload: dict[str, object]) -> str:
    rows = [f"| `{item['path']}` | {'YES' if item['present'] else 'NO'} |" for item in payload["required_files"]]
    targets = [f"- {target}" for target in payload["remaining_external_targets"]]
    return "\n".join([
        "# Release Readiness Report",
        "",
        f"- Candidate: **{payload['release_candidate']}**",
        f"- SPE Release Readiness: **{payload['spe_release_readiness']}**",
        "- Manual Internal Tasks: **0**",
        "",
        "## Required Files",
        "",
        "| File | Present |",
        "|---|---:|",
        *rows,
        "",
        "## Remaining External Targets",
        "",
        *targets,
        "",
        "## Non-Claim",
        "",
        str(payload["non_claim"]),
        "",
    ])


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    reports_dir = repo_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    payload = status_for(repo_root)
    (reports_dir / "release_readiness.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (reports_dir / "release_readiness.md").write_text(render_markdown(payload), encoding="utf-8")
    print("SPE RELEASE READINESS:", payload["spe_release_readiness"])
    return 0 if payload["spe_release_readiness"] == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
