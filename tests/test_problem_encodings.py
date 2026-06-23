import json
import subprocess
import sys
import unittest
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


class ProblemEncodingTests(unittest.TestCase):
    def run_command(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_research_standing_validator_passes(self) -> None:
        result = self.run_command("tools/validate_research_standing.py")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SPE RESEARCH STANDING: PASS", result.stdout)

    def test_problem_encoding_verifier_passes(self) -> None:
        result = self.run_command("spe/verify_problem_encodings.py")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SPE PROBLEM ENCODINGS: PASS", result.stdout)

    def test_problem_encoding_json_export_passes(self) -> None:
        result = self.run_command("spe/verify_problem_encodings.py", "--json")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["spe_result"], "PASS")
        self.assertEqual(data["mathematical_standing"], "PARTIAL")
        self.assertEqual(data["verified_problem_count"], 3)
        self.assertIn("does not prove", data["non_claim"])

    def test_problem_encodings_match_expected_results(self) -> None:
        for encoding_path, expected_path in PROBLEM_CASES:
            with self.subTest(encoding_path=encoding_path):
                encoding = load_json(encoding_path)
                expected = load_json(expected_path)

                self.assertEqual(encoding["problem_id"], expected["problem_id"])
                self.assertEqual(encoding["standing_status"], expected["expected_encoding_status"])
                self.assertGreaterEqual(
                    len(encoding["transitions"]),
                    expected["required_transition_count_min"],
                )
                self.assertGreaterEqual(
                    len(encoding["non_claims"]),
                    expected["required_non_claim_count_min"],
                )

                actual_cell_refs = {
                    cell_ref
                    for transition in encoding["transitions"]
                    for cell_ref in transition.get("cell_refs", [])
                }

                self.assertTrue(set(expected["required_cell_refs"]).issubset(actual_cell_refs))
                self.assertEqual(expected["expected_mathematical_standing"], "PARTIAL")
                self.assertIn("does not prove", expected["non_claim"])


if __name__ == "__main__":
    unittest.main()
