import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

PROBLEM_CASES = [
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


def load_json(relative_path: str) -> dict:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_research_standing_validator_passes():
    result = subprocess.run(
        [sys.executable, "tools/validate_research_standing.py"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "SPE RESEARCH STANDING: PASS" in result.stdout


def test_problem_encoding_verifier_passes():
    result = subprocess.run(
        [sys.executable, "spe/verify_problem_encodings.py"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "SPE PROBLEM ENCODINGS: PASS" in result.stdout


def test_problem_encoding_json_export_passes():
    result = subprocess.run(
        [sys.executable, "spe/verify_problem_encodings.py", "--json"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert data["spe_result"] == "PASS"
    assert data["mathematical_standing"] == "PARTIAL"
    assert data["verified_problem_count"] == 3
    assert "does not prove" in data["non_claim"]


def test_problem_encodings_match_expected_results():
    for encoding_path, expected_path in PROBLEM_CASES:
        encoding = load_json(encoding_path)
        expected = load_json(expected_path)

        assert encoding["problem_id"] == expected["problem_id"]
        assert encoding["standing_status"] == expected["expected_encoding_status"]
        assert len(encoding["transitions"]) >= expected["required_transition_count_min"]
        assert len(encoding["non_claims"]) >= expected["required_non_claim_count_min"]

        actual_cell_refs = {
            cell_ref
            for transition in encoding["transitions"]
            for cell_ref in transition.get("cell_refs", [])
        }

        assert set(expected["required_cell_refs"]).issubset(actual_cell_refs)
        assert expected["expected_mathematical_standing"] == "PARTIAL"
        assert "does not prove" in expected["non_claim"]
