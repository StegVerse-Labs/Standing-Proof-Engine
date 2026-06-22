#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.report import render_report
from spe.verify_expected_result import governance_result, run_declared_verifier


def verifier_alias(verifier_path):
    if verifier_path == "spe/verify_external_refs.py":
        return "external_refs"
    if verifier_path == "spe/verify_source_bound.py":
        return "source_bound"
    if verifier_path == "spe/verify_sdk_intake.py":
        return "sdk_intake"
    if verifier_path == "spe/verify_pointer.py":
        return "pointer"
    if verifier_path == "spe/verify_confirmation.py":
        return "confirmation"
    return "default"


def render_fixture_report(fixture_path, fixture, repo_root):
    artifact_ref = fixture["artifact"]
    verifier_path = fixture["verifier"]
    expected = fixture.get("expected", {})
    artifact_path = repo_root / artifact_ref
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    actual_status, checks = run_declared_verifier(verifier_path, artifact, repo_root)
    expected_status = expected.get("spe_result")
    expected_governance = expected.get("governance_result")
    actual_governance = governance_result(artifact)

    title = fixture.get("fixture_id") or fixture_path.stem
    report = render_report(
        str(title),
        artifact_ref,
        verifier_alias(verifier_path),
        artifact,
        actual_status,
        checks,
    )

    spe_match = "YES" if actual_status == expected_status else "NO"
    if expected_governance is None:
        governance_match = "NOT DECLARED"
    else:
        governance_match = "YES" if actual_governance == expected_governance else "NO"

    appendix = [
        "",
        "## Expected Fixture",
        "",
        f"- Fixture: `{fixture_path}`",
        f"- Expected SPE Result: **{expected_status}**",
        f"- Actual SPE Result: **{actual_status}**",
        f"- SPE Result Match: **{spe_match}**",
        f"- Expected Governance Result: **{expected_governance}**",
        f"- Actual Governance Result: **{actual_governance}**",
        f"- Governance Result Match: **{governance_match}**",
        "",
    ]
    return report + "\n".join(appendix) + "\n"


def main(argv):
    if len(argv) not in (1, 3):
        print("usage: python spe/report_expected_corpus.py [expected_results_dir output_dir]", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    corpus_dir = repo_root / "expected_results"
    output_dir = repo_root / "reports" / "expected_corpus"
    if len(argv) == 3:
        corpus_dir = (repo_root / argv[1]).resolve()
        output_dir = (repo_root / argv[2]).resolve()

    output_dir.mkdir(parents=True, exist_ok=True)
    index_lines = [
        "# Expected Corpus Reviewer Reports",
        "",
        "This directory contains reviewer reports generated from expected-result fixtures.",
        "",
        "| Fixture | Expected SPE | Expected Governance | Report |",
        "|---|---:|---:|---|",
    ]

    for fixture_path in sorted(corpus_dir.glob("*.expected.json")):
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        report = render_fixture_report(fixture_path.relative_to(repo_root), fixture, repo_root)
        output_name = fixture_path.name.replace(".expected.json", ".report.md")
        output_path = output_dir / output_name
        output_path.write_text(report, encoding="utf-8")
        expected = fixture.get("expected", {})
        expected_status = expected.get("spe_result")
        expected_governance = expected.get("governance_result")
        index_lines.append(
            f"| `{fixture_path.name}` | **{expected_status}** | **{expected_governance}** | `{output_name}` |"
        )

    (output_dir / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"wrote expected corpus reports to {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
