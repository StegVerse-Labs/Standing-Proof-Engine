#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from spe.tt_full_snapshot import load_full_snapshot

MAP = {"reviewed_candidate_to_commit_attempt": "T-221"}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python spe/check_full_snapshot_cases.py <manifest.json>", file=sys.stderr)
        return 2
    manifest = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    transitions = load_full_snapshot().get("transition_requirements", {})
    rows = []
    for sample in manifest.get("samples", []):
        case = sample.get("transition_case", {})
        ref = case.get("tt_transition_id") or case.get("transition_id") or case.get("transition_cell")
        tid = MAP.get(ref, ref)
        entry = transitions.get(tid, {})
        ok = bool(entry) and entry.get("implementation_status") == "implemented" and isinstance(entry.get("code_ref"), str)
        rows.append({"test_id": case.get("test_id"), "tt_transition_id": tid, "code_ref": entry.get("code_ref"), "ok": ok})
    passed = bool(rows) and all(row["ok"] for row in rows)
    print(json.dumps({"result": "PASS" if passed else "FAIL", "sample_count": len(rows), "samples": rows}, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
