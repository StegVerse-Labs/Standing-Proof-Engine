#!/usr/bin/env python3
"""Validate Standing-Proof-Engine research standing artifacts.

This validator checks structural repository standing for research artifacts.
It does not prove any mathematical open problem.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable

VALID_STATUSES = {"PASS", "PARTIAL", "FAIL"}

REQUIRED_FILES = [
    "research/stegverse_formalisms_unsolved_mathematics.md",
    "research/formalism_propagation_process.md",
    "research/research_manifest.json",
    "docs/repo_validation.md",
    "docs/testing_protocols.md",
    "tools/validate_research_standing.py",
]

REQUIRED_PROCESS_REFERENCES = [
    "research/",
    "research/research_manifest.json",
    "docs/repo_validation.md",
    "docs/testing_protocols.md",
    "tools/validate_research_standing.py",
    "tests/",
    "expected_results/",
    "samples/",
]

REQUIRED_REPORT_PHRASES = [
    "This report does not claim to solve any listed open problem.",
    "This report does not claim that an encoding, analogy, or transition table cell is a proof.",
]


def fail(message: str) -> None:
    print(f"SPE RESEARCH STANDING: FAIL - {message}")
    raise SystemExit(1)


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing required file: {path.as_posix()}")


def require_files(repo_root: Path, paths: Iterable[str]) -> None:
    for relative_path in paths:
        path = repo_root / relative_path
        if not path.exists():
            fail(f"missing required file: {relative_path}")
        if path.is_file() and path.stat().st_size == 0:
            fail(f"required file is empty: {relative_path}")


def load_manifest(repo_root: Path) -> dict:
    manifest_path = repo_root / "research/research_manifest.json"
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"manifest is not valid JSON: {exc}")


def validate_status(value: str, context: str) -> None:
    if value not in VALID_STATUSES:
        fail(f"invalid status {value!r} in {context}; expected one of {sorted(VALID_STATUSES)}")


def validate_manifest(repo_root: Path, manifest: dict) -> None:
    validate_status(str(manifest.get("status", "")), "manifest.status")

    artifacts = manifest.get("research_artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        fail("manifest must include non-empty research_artifacts list")

    for artifact in artifacts:
        artifact_id = artifact.get("artifact_id", "<missing artifact_id>")
        path_value = artifact.get("path")
        if not path_value:
            fail(f"artifact {artifact_id} is missing path")
        if not (repo_root / path_value).exists():
            fail(f"artifact {artifact_id} points to missing path: {path_value}")
        validate_status(str(artifact.get("standing_status", "")), f"artifact {artifact_id}")

    tracks = manifest.get("formalism_tracks")
    if not isinstance(tracks, list) or not tracks:
        fail("manifest must include non-empty formalism_tracks list")

    for track in tracks:
        track_id = track.get("track_id", "<missing track_id>")
        validate_status(str(track.get("standing_status", "")), f"track {track_id}")
        if not track.get("problems"):
            fail(f"track {track_id} must list problems")
        if not track.get("next_required_artifacts"):
            fail(f"track {track_id} must list next_required_artifacts")

    non_claims = manifest.get("non_claims")
    if not isinstance(non_claims, list) or len(non_claims) < 3:
        fail("manifest must include at least three non-claims")


def validate_report(repo_root: Path) -> None:
    report_text = load_text(repo_root / "research/stegverse_formalisms_unsolved_mathematics.md")
    for phrase in REQUIRED_REPORT_PHRASES:
        if phrase not in report_text:
            fail(f"research report missing required phrase: {phrase}")

    if "[SR-1]" not in report_text or "[SR-4]" not in report_text:
        fail("research report must include source-report citations [SR-1] through [SR-4]")


def validate_process(repo_root: Path) -> None:
    process_text = load_text(repo_root / "research/formalism_propagation_process.md")
    for reference in REQUIRED_PROCESS_REFERENCES:
        if reference not in process_text:
            fail(f"formalism propagation process missing required reference: {reference}")


def validate_docs(repo_root: Path) -> None:
    validation_text = load_text(repo_root / "docs/repo_validation.md")
    testing_text = load_text(repo_root / "docs/testing_protocols.md")

    if "python tools/validate_research_standing.py" not in validation_text:
        fail("repo validation doc missing research-standing command")
    if "python tools/validate_research_standing.py" not in testing_text:
        fail("testing protocols doc missing research-standing command")
    if "does not prove an open mathematical problem" not in testing_text:
        fail("testing protocols must state that structural testing does not prove an open problem")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    require_files(repo_root, REQUIRED_FILES)
    manifest = load_manifest(repo_root)
    validate_manifest(repo_root, manifest)
    validate_report(repo_root)
    validate_process(repo_root)
    validate_docs(repo_root)
    print("SPE RESEARCH STANDING: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
