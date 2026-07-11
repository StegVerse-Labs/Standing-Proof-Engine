# SPE Mirror Handoff

## Assumption

This file is the current handoff and task source of truth for `StegVerse-Labs/Standing-Proof-Engine`. It must be checked before continuing mirror, release, publication, or cross-repo update work.

## Active Repo

```text
Org: StegVerse-Labs
Repo: Standing-Proof-Engine
Active Goal: v0.5.0 release handling and downstream propagation
```

## Current Verification State

Repository operator manually dispatched both required workflows against current `main` and reported both green:

```text
Verified head: 60f3ce987b43c8021dd9ad662ac002ed2744bc13
SPE TT Binding: PASS
SPE Sandbox Sweep: PASS
```

Durable verification receipt:

```text
receipts/SPE-TT-v0.5.0-verification.json
```

The receipt records verification evidence and does not itself assert tag or release creation authority.

## Installed Current Fixes

```text
tools/refresh_frozen_hashes.py
tools/expected_corpus_inventory.py
spe/verify_heartbeat_path_selection.py
samples/heartbeat_path_selection_001.json
samples/destination_generated_event_hash_001.json
spe/verify_hash_import.py
samples/destination_receipt_chain_current_001.json
spe/verify_expected_result.py
spe/run_tt_integration_checks.py
spe/check_no_manual_tt_tasks.py
receipts/SPE-TT-v0.5.0-verification.json
SPE_MIRROR_HANDOFF.md
```

## Verification Contract

The stable TT task surface remains `.github/workflows/spe-tt-binding.yml` and executes:

```text
python -m spe.run_tt_integration_checks
```

Every nested checker executes as a module. The no-manual-task validator requires the canonical module command and rejects the legacy direct-script invocation.

Relevant repair commits:

```text
e9a024090808d35e83f724c85c0c3d227cac4bd1
8c72090fa914c4eab6fb106c3643197675b064ac
803b629a98c22bb2a5df58e7960c0677c4e33e38
```

Verification receipt commit:

```text
6d45ea518f21fa252dc4f1d041dd6caf732f2278
```

## Known Remaining Work

Destination Org/Repo: `StegVerse-Labs/Standing-Proof-Engine`

```text
1. Create tag/release v0.5.0 if release tooling or an existing declared release task is available.
2. Verify propagation/update targets after release handling.
3. Begin SDK-to-SPE commitment-candidate intake as the successor integration goal.
```

## Known Downstream Destinations

```text
master-records/core-lite -> live destination-generated receipt chain emission
StegVerse-Labs/Site -> public release/status update
GCAT-BCAT-Engine/Publisher -> publication/update propagation check
StegVerse-Labs/admissibility-wiki -> governance theorem/update propagation check
StegVerse-002/stegguardian-wiki -> guardian/standing boundary propagation check
StegVerse-org/StegVerse-SDK -> commitment-candidate intake integration
```

## Tag/Release Readiness

```text
v0.5.0 candidate: VERIFIED
TT Binding: PASS
Sandbox Sweep: PASS
Durable receipt: RECORDED
Git tag/release: NOT YET RECORDED
```

Do not claim that the Git tag or GitHub release exists until repository evidence confirms creation.

## Next Integration Goal Candidate

The successor integration goal is SDK-to-SPE commitment-candidate intake.

SPE should consume manifest/receipt-bound Commitment Candidate / Execution Authority Request material from the SDK at commit-time without treating SDK discovery or packet construction as execution authority.

## Archive Note

The SPE verification thread is complete and ready for archive. Release handling and SDK-to-SPE integration can continue entirely from this handoff and the durable verification receipt.
