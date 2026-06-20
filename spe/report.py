#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.result_export import canonical_sha256
from spe.verify import FAIL, PARTIAL, PASS, Check, verify_artifact
from spe.verify_external_refs import verify_external_ref_artifact
from spe.verify_source_bound import verify_source_bound_artifact


def select_verifier(verifier_name, artifact, repo_root):
    if verifier_name == "external_refs":
        return verify_external_ref_artifact(artifact, repo_root)
    if verifier_name == "source_bound":
        return verify_source_bound_artifact(artifact)
    return verify_artifact(artifact)


def status_label(status):
    if status == PASS:
        return "PASS"
    if status == PARTIAL:
        return "PARTIAL"
    if status == FAIL:
        return "FAIL"
    return str(status)


def render_report(title, artifact_path, verifier_name, artifact, status, checks):
    artifact_hash = canonical_sha256(artifact)
    lines = [
        f"# {title}",
        "",
        "## Summary",
        "",
        f"- Artifact: `{artifact_path}`",
        f"- Verifier: `{verifier_name}`",
        f"- SPE Result: **{status_label(status)}**",
        f"- Artifact SHA-256: `{artifact_hash}`",
        "",
        "## Check Results",
        "",
        "| Check | Status | Detail |",
        "|---|---:|---|",
    ]
    for check in checks:
        detail = check.detail.replace("|", "\\|")
        lines.append(f"| `{check.name}` | **{check.status}** | {detail} |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
        ]
    )
    if status == PASS:
        lines.append("This artifact proves its declared governance result from the available proof material.")
    elif status == PARTIAL:
        lines.append("This artifact reconstructs a governance result but contains at least one incomplete standing proof condition.")
    else:
        lines.append("This artifact does not support its claimed governance result under the selected verifier.")

    return "\n".join(lines) + "\n"


def main(argv):
    if len(argv) not in (3, 4):
        print("usage: python spe/report.py <artifact.json> <output.md> [default|source_bound|external_refs]", file=sys.stderr)
        return 2

    artifact_path = Path(argv[1])
    output_path = Path(argv[2])
    verifier_name = argv[3] if len(argv) == 4 else "default"
    repo_root = Path(__file__).resolve().parents[1]

    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    status, checks = select_verifier(verifier_name, artifact, repo_root)
    title = artifact.get("proof_id") or artifact.get("trace_id") or artifact_path.stem
    report = render_report(str(title), str(artifact_path), verifier_name, artifact, status, checks)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"wrote {output_path}")
    return 0 if status in {PASS, PARTIAL} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
