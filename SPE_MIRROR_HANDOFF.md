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

GitHub PR sandbox verification is green.

The latest main-branch sandbox sweep executed 47 workflow-equivalent commands. Forty-six passed. The only failure was a producer/consumer path mismatch:

```text
Producer: tools/expected_corpus_inventory.py
Consumer: tools/write_expected_corpus_failed_summary.py
Expected path: reports/expected_corpus_inventory.json
Observed state: producer printed JSON to stdout but did not persist the expected report file
```

The producer now writes `reports/expected_corpus_inventory.json` and continues emitting the inventory to stdout.

Repair commit:

```text
803b629a98c22bb2a5df58e7960c0677c4e33e38
```

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
SPE_MIRROR_HANDOFF.md
```

## TT Binding Repair

The existing `.github/workflows/spe-tt-binding.yml` remains the stable task surface. Its integration runner executes from the repository root as a module:

```text
python -m spe.run_tt_integration_checks
```

Every nested checker also executes as a module. The no-manual-task validator now requires the canonical module command and rejects the legacy direct-script invocation.

Relevant repair commits:

```text
e9a024090808d35e83f724c85c0c3d227cac4bd1
8c72090fa914c4eab6fb106c3643197675b064ac
803b629a98c22bb2a5df58e7960c0677c4e33e38
```

## Known Remaining Work

Destination Org/Repo: `StegVerse-Labs/Standing-Proof-Engine`

```text
1. Verify SPE Sandbox Sweep passes after the inventory persistence repair.
2. Verify SPE TT Binding passes on the same current main-branch state.
3. Record passing sandbox and TT binding results in a durable verification receipt.
4. Tag/release v0.5.0 only if all required checks are green.
5. Verify propagation/update targets after the tag candidate.
```

## Known Downstream Destinations

```text
master-records/core-lite -> live destination-generated receipt chain emission
StegVerse-Labs/Site -> public release/status update after tag candidate
GCAT-BCAT-Engine/Publisher -> publication/update propagation check after tag candidate
StegVerse-Labs/admissibility-wiki -> governance theorem/update propagation check after tag candidate
StegVerse-002/stegguardian-wiki -> guardian/standing boundary propagation check after tag candidate
StegVerse-org/StegVerse-SDK -> commitment-candidate intake integration after release handling
```

## Tag/Release Readiness

```text
v0.5.0 candidate: implementation complete; current-main verification pending
```

Do not tag or publish release readiness until Sandbox Sweep and TT Binding are green on the same current commit.

## Next Integration Goal Candidate

After tag/release handling, the next integration candidate is SDK-to-SPE commitment-candidate intake.

Reason: SPE should consume manifest/receipt-bound Commitment Candidate / Execution Authority Request material from the SDK at commit-time.

## Archive Note

This thread is ready for archive after current-main verification, release handling, and successor propagation work are recorded.
