#!/usr/bin/env python3
"""Recompute or check frozen canonical-hash bindings in samples.

Several sample artifacts carry SHA-256 bindings that must equal the canonical
hash of another file. These values drift when referenced files change. This
checker centralizes the bindings and their dependency order.
"""
import json
import sys
from pathlib import Path

from spe.result_export import canonical_sha256

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load(rel):
    return json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))


def _save(rel, obj):
    (REPO_ROOT / rel).write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def compute_expected():
    import_rel = "samples/destination_generated_event_hash_001.json"
    chain_rel = "samples/destination_receipt_chain_001.json"

    import_record = _load(import_rel)
    event_rel = import_record["source_event"]
    event_hash = canonical_sha256(_load(event_rel))

    corrected_import = dict(import_record)
    corrected_import["source_event_sha256"] = event_hash
    corrected_import["destination_event_hash"] = event_hash
    import_hash = canonical_sha256(corrected_import)

    return [
        (import_rel, "source_event_sha256", event_hash),
        (import_rel, "destination_event_hash", event_hash),
        (chain_rel, "source_hash_import_sha256", import_hash),
    ]


def main(argv):
    write = "--write" in argv[1:]
    drift = []
    for rel, field, expected in compute_expected():
        obj = _load(rel)
        actual = obj.get(field)
        if actual != expected:
            drift.append((rel, field, actual, expected))
            if write:
                obj[field] = expected
                _save(rel, obj)

    if not drift:
        print("frozen hashes: OK (no drift)")
        return 0

    verb = "rewrote" if write else "stale"
    for rel, field, actual, expected in drift:
        print(f"{verb}: {rel} :: {field}")
        print(f"    was: {actual}")
        print(f"    now: {expected}")
    if write:
        print(f"{len(drift)} binding(s) refreshed")
        return 0
    print(f"{len(drift)} binding(s) drifted; run with --write to fix")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
