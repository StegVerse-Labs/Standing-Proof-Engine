#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from spe.result_export import canonical_sha256
from spe.verify import FAIL, PASS, Check, render
from spe.verify_hash_import import verify_hash_import


def verify_receipt_chain(chain, repo_root):
    required = [
        "chain_id",
        "chain_type",
        "source_hash_import",
        "source_hash_import_sha256",
        "chain_result",
        "receipt_chain",
        "chain_flags",
    ]
    missing = [key for key in required if not chain.get(key)]
    if missing:
        return FAIL, [Check("parse_receipt_chain", FAIL, f"missing fields: {', '.join(missing)}")]

    checks = [Check("parse_receipt_chain", PASS, "receipt chain parsed")]

    route_ok = chain.get("chain_type") == "destination_generated_receipt_chain"
    checks.append(Check("receipt_chain_route", PASS if route_ok else FAIL, "receipt chain route checked"))

    import_path = repo_root / chain["source_hash_import"]
    import_record = json.loads(import_path.read_text(encoding="utf-8"))
    import_hash = canonical_sha256(import_record)
    checks.append(Check("source_hash_import_binding", PASS if import_hash == chain.get("source_hash_import_sha256") else FAIL, "source hash import checked"))

    import_status, _ = verify_hash_import(import_record, repo_root)
    checks.append(Check("source_hash_import_verifies", PASS if import_status == PASS else FAIL, "source hash import verifier checked"))

    receipts = chain.get("receipt_chain", [])
    receipt_types = [receipt.get("receipt_type") for receipt in receipts]
    expected_types = ["confirmation", "destination_event", "destination_hash_import"]
    checks.append(Check("receipt_chain_order", PASS if receipt_types == expected_types else FAIL, "receipt chain order checked"))

    artifacts_exist = all((repo_root / receipt.get("artifact", "")).exists() for receipt in receipts)
    checks.append(Check("receipt_chain_artifacts_exist", PASS if artifacts_exist else FAIL, "receipt chain artifacts checked"))

    final_matches = bool(receipts) and receipts[-1].get("artifact") == chain.get("source_hash_import")
    checks.append(Check("receipt_chain_final_binding", PASS if final_matches else FAIL, "receipt chain final binding checked"))

    flags = chain.get("chain_flags", {})
    flags_ok = all(flags.get(key) is True for key in ["hash_import_bound", "ordered_receipts_present", "final_receipt_matches_source", "downstream_chain_declared"])
    checks.append(Check("receipt_chain_flags", PASS if flags_ok else FAIL, "receipt chain flags checked"))

    result_ok = chain.get("chain_result") == "CHAIN_BOUND"
    checks.append(Check("receipt_chain_result", PASS if result_ok else FAIL, "receipt chain result checked"))

    status = FAIL if any(check.status == FAIL for check in checks) else PASS
    return status, checks


def main(argv):
    if len(argv) != 2:
        print("usage: python spe/verify_receipt_chain.py <chain.json>", file=sys.stderr)
        return 2
    repo_root = Path(__file__).resolve().parents[1]
    chain = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    status, checks = verify_receipt_chain(chain, repo_root)
    print(render(status, checks))
    return 0 if status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
