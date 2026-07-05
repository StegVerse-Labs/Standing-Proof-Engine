#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / "samples" / "spe_tt_downstream_propagation_targets.json"
REQUIRED = {"StegVerse-Labs/Site", "StegVerse-Labs/admissibility-wiki", "StegVerse-org/StegVerse-SDK"}


def main() -> int:
    data = json.loads(TARGETS.read_text(encoding="utf-8"))
    targets = data.get("targets", [])
    repos = {target.get("repository") for target in targets if isinstance(target, dict)}
    missing = sorted(REQUIRED - repos)
    if data.get("source_repository") != "StegVerse-Labs/Standing-Proof-Engine":
        print("FAIL: source repository mismatch", file=sys.stderr)
        return 1
    if data.get("canonical_transition_source") != "Admissible-Existence/TT":
        print("FAIL: canonical source mismatch", file=sys.stderr)
        return 1
    if missing:
        print("FAIL: missing targets: " + ", ".join(missing), file=sys.stderr)
        return 1
    if any(not target.get("required_artifacts") for target in targets):
        print("FAIL: required artifacts missing", file=sys.stderr)
        return 1
    print("PASS: SPE TT propagation targets are declared.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
