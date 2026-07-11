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

GitHub PR sandbox verification is now green.

Sandbox PR:

```text
PR: #11
Head SHA: db74d7e18e3f5db512a7bea9e4665e5f04c04767
Expected Corpus Inventory: success
Verify Standing Proof: success
Sandbox PR state: closed unmerged, not intended for merge
```

The prior receipt-chain expected fixture failure was resolved by the current artifact resolver patch in `spe/verify_expected_result.py`.

## Installed Current Fixes

```text
tools/refresh_frozen_hashes.py
spe/verify_heartbeat_path_selection.py
samples/heartbeat_path_selection_001.json
samples/destination_generated_event_hash_001.json
spe/verify_hash_import.py
samples/destination_receipt_chain_current_001.json
spe/verify_expected_result.py
spe/run_tt_integration_checks.py
SPE_MIRROR_HANDOFF.md
```

## TT Binding Repair

The existing `.github/workflows/spe-tt-binding.yml` remains the stable task surface. Its integration runner executes from the repository root as a module:

```text
python -m spe.run_tt_integration_checks
```

The integration runner now also invokes every nested checker as a module, for example:

```text
python -m spe.check_tt_full_snapshot
```

This removes the remaining `ModuleNotFoundError: No module named 'spe'` failure caused by nested direct-script execution. No additional workflow was added.

Repair commit:

```text
e9a024090808d35e83f724c85c0c3d227cac4bd1
```

## Known Remaining Work

Destination Org/Repo: `StegVerse-Labs/Standing-Proof-Engine`

```text
1. Verify SPE TT Binding passes after the nested module-path repair.
2. Record the passing TT binding result in the current handoff or verification receipt.
3. Tag/release v0.5.0 if release tooling is available and all required checks are green.
4. Verify propagation/update targets after tag candidate.
5. Close or delete any remaining sandbox branches if branch-delete tooling is available.
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

Current tag candidate:

```text
v0.5.0 candidate: sandbox verified green; TT binding verification pending
```

Do not tag or publish release readiness until the repaired TT binding workflow is observed green.

## Next Integration Goal Candidate

After tag/release handling, the next integration candidate is SDK-to-SPE commitment-candidate intake.

Reason: SPE should consume manifest/receipt-bound Commitment Candidate / Execution Authority Request material from the SDK at commit-time.

## Archive Note

This thread is ready for archive after TT binding verification, tag/release availability checking, and successor propagation work are recorded.
