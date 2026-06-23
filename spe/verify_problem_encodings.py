#!/usr/bin/env python3
"""Verify StegVerse mathematical problem encodings.

This verifier checks that calibration problem encodings match their expected
structural standing fixtures. It does not prove any open mathematical problem.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_CASES = [
    (
        "samples/problems/collatz_encoding.json",
        "expected_results/problems/collatz_encoding_expected.json",
    ),
    (
        "samples/problems/jacobian_encoding.json",
        "expected_results/problems/jacobian_encoding_expected.json",
    ),
    (
        "samples/problems/caccetta_haggkvist_encoding.json",
        "expected_results/problems/caccetta_haggkvist_encoding_expected.json",
    ),
]


class VerificationError(Exception):
    """Raised when a problem encoding fails standing verification."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise VerificationError(f"missing file: {path.as_posix()}") from exc
    except json.JSONDecodeError as exc:
        raise VerificationError(f"invalid JSON in {path.as_posix()}: {exc}") from exc


def collect_cell_refs(encoding: dict[str, Any]) -> set[str]:
    cell_refs: set[str] = set()
    for transition in encoding.get("transitions", []):
        for cell_ref in transition.get("cell_refs", []):
            cell_refs.add(str(cell_ref))
    return cell_refs


def verify_case(repo_root: Path, encoding_path: str, expected_path: str) -> dict[str, Any]:
    encoding = load_json(repo_root / encoding_path)
    expected = load_json(repo_root / expected_path)

    problem_id = encoding.get("problem_id")
    if problem_id != expected.get("problem_id"):
        raise VerificationError(
            f"problem_id mismatch for {encoding_path}: "
            f"{problem_id!r} != {expected.get('problem_id')!r}"
        )

    if encoding.get("standing_status") != expected.get("expected_encoding_status"):
        raise VerificationError(
            f"standing_status mismatch for {problem_id}: "
            f"{encoding.get('standing_status')!r} != {expected.get('expected_encoding_status')!r}"
        )

    transitions = encoding.get("transitions")
    if not isinstance(transitions, list):
        raise VerificationError(f"transitions must be a list for {problem_id}")

    required_transition_count = int(expected.get("required_transition_count_min", 0))
    if len(transitions) < required_transition_count:
        raise VerificationError(
            f"too few transitions for {problem_id}: {len(transitions)} < {required_transition_count}"
        )

    non_claims = encoding.get("non_claims")
    if not isinstance(non_claims, list):
        raise VerificationError(f"non_claims must be a list for {problem_id}")

    required_non_claim_count = int(expected.get("required_non_claim_count_min", 0))
    if len(non_claims) < required_non_claim_count:
        raise VerificationError(
            f"too few non_claims for {problem_id}: {len(non_claims)} < {required_non_claim_count}"
        )

    actual_cell_refs = collect_cell_refs(encoding)
    required_cell_refs = {str(value) for value in expected.get("required_cell_refs", [])}
    missing_cell_refs = sorted(required_cell_refs - actual_cell_refs)
    if missing_cell_refs:
        raise VerificationError(
            f"missing required transition-cell refs for {problem_id}: {missing_cell_refs}"
        )

    if expected.get("expected_mathematical_standing") != "PARTIAL":
        raise VerificationError(
            f"expected mathematical standing must remain PARTIAL for calibration encoding {problem_id}"
        )

    expected_non_claim = str(expected.get("non_claim", ""))
    if "does not prove" not in expected_non_claim:
        raise VerificationError(f"expected result non-claim must state does not prove for {problem_id}")

    return {
        "problem_id": problem_id,
        "encoding_path": encoding_path,
        "expected_path": expected_path,
        "structural_standing": expected.get("expected_structural_standing"),
        "mathematical_standing": expected.get("expected_mathematical_standing"),
        "encoding_status": encoding.get("standing_status"),
        "transition_count": len(transitions),
        "cell_ref_count": len(actual_cell_refs),
    }


def verify_all(repo_root: Path) -> list[dict[str, Any]]:
    return [verify_case(repo_root, encoding_path, expected_path) for encoding_path, expected_path in DEFAULT_CASES]


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify StegVerse problem encodings.")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]

    try:
        results = verify_all(repo_root)
    except VerificationError as exc:
        if args.json:
            print(json.dumps({"spe_result": "FAIL", "error": str(exc)}, indent=2, sort_keys=True))
        else:
            print(f"SPE PROBLEM ENCODINGS: FAIL - {exc}")
        return 1

    if args.json:
        print(
            json.dumps(
                {
                    "spe_result": "PASS",
                    "mathematical_standing": "PARTIAL",
                    "verified_problem_count": len(results),
                    "results": results,
                    "non_claim": "This verifier checks encoding structure only; it does not prove any open mathematical problem.",
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print("SPE PROBLEM ENCODINGS: PASS")
        for result in results:
            print(
                f"- {result['problem_id']}: "
                f"encoding={result['encoding_status']} "
                f"math={result['mathematical_standing']} "
                f"transitions={result['transition_count']} "
                f"cell_refs={result['cell_ref_count']}"
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
