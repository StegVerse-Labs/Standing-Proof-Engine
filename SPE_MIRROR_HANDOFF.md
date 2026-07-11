# SPE Mirror Handoff

## Assumption

This file is the current handoff and task source of truth for `StegVerse-Labs/Standing-Proof-Engine`. It must be checked before continuing mirror, release, publication, or cross-repo update work.

## Active Repo

```text
Org: StegVerse-Labs
Repo: Standing-Proof-Engine
Active Goal: SDK-to-SPE commitment-candidate intake and receipt-bound standing return
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

## Installed SDK-to-SPE Integration

```text
spe/sdk_commitment_intake.py
tests/test_sdk_commitment_intake.py
docs/SDK_COMMITMENT_INTAKE.md
SPE_MIRROR_HANDOFF.md
```

The SPE consumer validates the SDK envelope contract, independently reconstructs `candidate_hash` and `envelope_hash`, preserves `package_id`, `transition_id`, and `run_id`, and rejects any envelope that requests execution authority or implies inherited standing.

The return receipt is bounded to:

```text
standing_result: ALLOW | DENY | FAIL_CLOSED
execution_authorized: false
execution_performed: false
master_record_installed: false
```

An `ALLOW` result advances only to the next governed execution-authority boundary.

Implementation commits:

```text
a842545d130764add8bc0eab415d3ecf09085e14
99c82c20390285650776066b1db6f071cd4be724
831b077ae6d0d33296284b78aaef604e5a5f4ee4
```

## Verification Contract

Existing TT verification remains:

```text
python -m spe.run_tt_integration_checks
```

SDK intake verification:

```text
python -m unittest tests.test_sdk_commitment_intake
```

No new workflow was added. The new test should be consumed by the existing repository verification and sandbox surfaces.

## Known Remaining Work

Destination Org/Repo: `StegVerse-Labs/Standing-Proof-Engine`

```text
1. Verify the new SDK commitment intake tests pass on current main.
2. Add a canonical SDK-generated envelope fixture for cross-repo compatibility verification.
3. Record a receipt-bound ALLOW, DENY, and FAIL_CLOSED example set.
4. Preserve transition_id and run_id into master-records/orchestration lifecycle evidence.
5. Create tag/release v0.5.0 if release tooling or an existing declared release task becomes available.
```

## Known Downstream Destinations

```text
StegVerse-org/StegVerse-SDK -> envelope producer
master-records/orchestration -> lifecycle, custody, and final receipt preservation
StegVerse-Labs/Ecosystem-Delegation -> governed execution-authority evaluation after SPE ALLOW
StegVerse-Labs/Site -> public status update after verified integration
GCAT-BCAT-Engine/Publisher -> publication/update propagation check
StegVerse-Labs/admissibility-wiki -> governance theorem/update propagation check
StegVerse-002/stegguardian-wiki -> guardian/standing boundary propagation check
```

## Tag/Release Readiness

```text
v0.5.0 verification milestone: COMPLETE
SDK-to-SPE integration implementation: INSTALLED
SDK-to-SPE integration verification: PENDING
Git tag/release: NOT YET RECORDED
```

Do not claim that the Git tag or GitHub release exists until repository evidence confirms creation.

## Next Integration Goal Candidate

After SDK envelope compatibility is verified, the next integration goal is preserving the SPE standing receipt through `master-records/orchestration` and into the governed execution-authority boundary without converting `ALLOW` into execution.

## Archive Note

The prior SPE verification thread is complete. SDK-to-SPE integration can continue entirely from this handoff and the installed consumer, tests, and documentation.
