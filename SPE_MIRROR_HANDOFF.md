# SPE Mirror Handoff

## Assumption

This file is the current handoff and task source of truth for `StegVerse-Labs/Standing-Proof-Engine`. It must be checked before continuing mirror, release, publication, or cross-repo update work.

## Active Repo

```text
Org: StegVerse-Labs
Repo: Standing-Proof-Engine
Active Goal: GitHub sandbox verification to green activation path
```

## Current Sandbox State

The GitHub PR sandbox has advanced past these earlier failures:

```text
tools.refresh_frozen_hashes import path
spe.verify_heartbeat_path_selection import path
hash import expected-result fixture
```

The latest visible failing class was the receipt-chain expected fixture path. The screenshot confirmed:

```text
parse_expected_fixture: PASS
expected_spe_result: FAIL - expected PASS, got FAIL
expected_governance_result: PASS
source_hash_import_binding: FAIL - expected PASS, got FAIL
source_hash_import_verifies: PASS
receipt_chain_order: PASS
receipt_chain_artifacts_exist: PASS
receipt_chain_final_binding: PASS
receipt_chain_flags: PASS
receipt_chain_result: PASS
```

## Installed Current Fixes

```text
tools/refresh_frozen_hashes.py
spe/verify_heartbeat_path_selection.py
samples/heartbeat_path_selection_001.json
samples/destination_generated_event_hash_001.json
spe/verify_hash_import.py
samples/destination_receipt_chain_current_001.json
spe/verify_expected_result.py
```

`spe/verify_expected_result.py` now resolves the stale receipt-chain expected artifact reference to `samples/destination_receipt_chain_current_001.json` before invoking the strict receipt-chain verifier.

## Known Remaining Work

Destination Org/Repo: `StegVerse-Labs/Standing-Proof-Engine`

```text
1. Trigger a fresh GitHub PR sandbox from the latest main commit.
2. Verify the receipt-chain expected fixture now passes through the resolver patch.
3. Continue through the next failing workflow step, if any.
4. Patch the exact failing module/sample/fixture and rerun the GitHub sandbox without manual user action.
5. Once full green, close sandbox PRs/branches and record final activation evidence here.
```

## Known Downstream Destinations

```text
master-records/core-lite -> live destination-generated receipt chain emission
StegVerse-Labs/Site -> public release/status update after tag candidate
GCAT-BCAT-Engine/Publisher -> publication/update propagation check after tag candidate
admissibility-wiki -> governance theorem/update propagation check after tag candidate
stegguardian-wiki -> guardian/standing boundary propagation check after tag candidate
```

## Tag/Release Readiness

Current tag candidate remains blocked until the GitHub sandbox reaches full green verification.

```text
v0.5.0 candidate: blocked by sandbox verification
```

## Next Integration Goal Candidate

After full green verification, the next integration candidate is SDK-to-SPE commitment-candidate intake.

Reason: SPE should consume manifest/receipt-bound Commitment Candidate / Execution Authority Request material from the SDK at commit-time.

## Archive Note

This thread is not archive-ready until the GitHub sandbox reaches green verification or this handoff records a precise successor task that owns the remaining failure.
