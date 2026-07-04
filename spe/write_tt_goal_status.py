#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_MD = ROOT / "docs" / "SPE_TT_GOAL_STATUS.md"
OUT_JSON = ROOT / "docs" / "SPE_TT_GOAL_STATUS.json"
GOAL = ROOT / "samples" / "spe_tt_activation_goal.json"


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def main() -> int:
    goal = json.loads(GOAL.read_text(encoding="utf-8"))
    docs = goal.get("required_docs", [])
    scripts = goal.get("required_scripts", [])
    checks = goal.get("required_checks", [])
    doc_results = {path: exists(path) for path in docs}
    script_results = {path: exists(path) for path in scripts}
    ready = all(doc_results.values()) and all(script_results.values()) and len(checks) >= 8
    status = {
        "schema": "spe_tt_goal_status.v0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "StegVerse-Labs/Standing-Proof-Engine",
        "goal_id": goal.get("goal_id"),
        "ready": ready,
        "required_check_count": len(checks),
        "docs": doc_results,
        "scripts": script_results,
        "boundary": "Readiness records repo integration checks only. Source transition semantics remain in Admissible-Existence/TT.",
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# SPE TT Goal Status",
        "",
        "## Current State",
        "",
        f"ready: {str(ready).lower()}",
        f"required_check_count: {len(checks)}",
        "",
        "## Docs",
        "",
    ]
    for path, ok in doc_results.items():
        lines.append(f"- {'PASS' if ok else 'MISSING'}: `{path}`")
    lines.extend(["", "## Scripts", ""])
    for path, ok in script_results.items():
        lines.append(f"- {'PASS' if ok else 'MISSING'}: `{path}`")
    lines.extend([
        "",
        "## Boundary",
        "",
        "This status record verifies repository integration readiness only. It does not redefine TT semantics, grant commit-time permission, or make a Commitment Candidate authorizing.",
        "",
    ])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"SPE TT goal status ready={ready}")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
