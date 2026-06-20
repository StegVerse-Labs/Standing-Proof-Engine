import json
from pathlib import Path
from typing import Any

from spe.result_export import canonical_sha256
from spe.verify import FAIL, PASS, Check


BINDING_TO_SOURCE_OBJECT = {
    "review_artifact_hash": "review_artifact",
    "evidence_packet_hash": "evidence_packet",
    "authority_state_review_hash": "authority_state_review",
    "authority_state_commit_hash": "authority_state_commit",
    "policy_state_review_hash": "policy_state_review",
    "policy_state_commit_hash": "policy_state_commit",
    "context_state_hash": "context_state",
}


def load_source_objects_from_refs(artifact: dict[str, Any], repo_root: Path) -> tuple[dict[str, Any], list[str]]:
    refs = artifact.get("source_object_refs", {})
    if not isinstance(refs, dict):
        return {}, ["source_object_refs is not an object"]

    loaded: dict[str, Any] = {}
    errors: list[str] = []
    for object_name, ref_path in refs.items():
        if not isinstance(ref_path, str):
            errors.append(f"{object_name} ref is not a string")
            continue

        candidate = (repo_root / ref_path).resolve()
        try:
            candidate.relative_to(repo_root.resolve())
        except ValueError:
            errors.append(f"{object_name} ref escapes repo root")
            continue

        if candidate.suffix != ".json":
            errors.append(f"{object_name} ref is not json")
            continue

        try:
            loaded[object_name] = json.loads(candidate.read_text(encoding="utf-8"))
        except FileNotFoundError:
            errors.append(f"{object_name} ref not found")
        except json.JSONDecodeError:
            errors.append(f"{object_name} ref is not valid json")

    return loaded, errors


def with_resolved_source_refs(artifact: dict[str, Any], repo_root: Path) -> tuple[dict[str, Any], list[Check]]:
    loaded, errors = load_source_objects_from_refs(artifact, repo_root)
    if errors:
        return artifact, [Check("source_object_refs", FAIL, "; ".join(errors))]

    resolved = dict(artifact)
    resolved["source_objects"] = loaded
    return resolved, [Check("source_object_refs", PASS, f"{len(loaded)} local source object refs resolved")]


def resolved_hash_bindings(artifact: dict[str, Any]) -> dict[str, str]:
    source_objects = artifact.get("source_objects", {})
    declared = artifact.get("declared_hash_bindings", {})
    resolved: dict[str, str] = {}

    for binding_name, object_name in BINDING_TO_SOURCE_OBJECT.items():
        source_object = source_objects.get(object_name)
        if not isinstance(source_object, dict):
            continue

        computed = canonical_sha256(source_object)
        declared_value = declared.get(binding_name)
        if declared_value in (None, "AUTO"):
            resolved[binding_name] = computed
        else:
            resolved[binding_name] = declared_value

    return resolved


def verify_source_hash_bindings(artifact: dict[str, Any]) -> list[Check]:
    source_objects = artifact.get("source_objects")
    declared = artifact.get("declared_hash_bindings")
    if not isinstance(source_objects, dict) or not isinstance(declared, dict):
        return [Check("source_hash_bindings", FAIL, "source_objects or declared_hash_bindings missing")]

    failures: list[str] = []
    verified = 0
    for binding_name, object_name in BINDING_TO_SOURCE_OBJECT.items():
        source_object = source_objects.get(object_name)
        if not isinstance(source_object, dict):
            failures.append(f"missing source object {object_name}")
            continue

        declared_value = declared.get(binding_name)
        computed = canonical_sha256(source_object)
        if declared_value not in (computed, "AUTO"):
            failures.append(f"{binding_name} does not match computed canonical hash")
        else:
            verified += 1

    if failures:
        return [Check("source_hash_bindings", FAIL, "; ".join(failures))]

    return [Check("source_hash_bindings", PASS, f"{verified} source hash bindings verified")]
