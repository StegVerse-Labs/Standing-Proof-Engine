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
samples/sdk_commitment_intake_envelope_001.json
samples/sdk_commitment_standing_receipts_001.json
SPE_MIRROR_HANDOFF.md
```

The SPE consumer validates the SDK envelope contract, independently reconstructs `candidate_hash` and `envelope_hash`, preserves `package_id`, `transition_id`, and `run_id`, and rejects any envelope that requests execution authority or implies inherited standing.

The canonical cross-repo fixture now binds one SDK-generated envelope to three deterministic SPE receipt examples:

```text
ALLOW
DENY
FAIL_CLOSED
```

Every receipt preserves:

```text
transition_id: transition.sdk.spe.fixture.001
run_id: run-sdk-spe-fixture-001
candidate_hash: fa64ea26db289fdf30cbce4f08f18c4ef71f68f839396d10d71476f1451c4232
envelope_hash: 000e932913031bbd5a9357d6f6cadade19594c8595c55ca7ef106bebb5a25af8
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
fca157afe6f29355ac4c6c6359906f70cffc46d4
3201fa4af3588384cd87430b295a630b9e13f7a5
fe437418eb0c391d7ccffab0933d7fac448f4744
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

The SDK intake test now verifies:

```text
- canonical envelope hash reconstruction
- candidate hash reconstruction
- transition_id and run_id preservation
- ALLOW receipt reconstruction
- DENY receipt reconstruction
- FAIL_CLOSED receipt reconstruction
- no execution authority or Master-Records installation claim
```

No new workflow was added. The test remains on the existing repository verification and sandbox surfaces.

## Known Remaining Work

Destination Org/Repo: `StegVerse-Labs/Standing-Proof-Engine`

```text
1. Verify the expanded SDK commitment intake test passes on current main.
2. Preserve transition_id and run_id into master-records/orchestration lifecycle evidence.
3. Define the governed execution-authority consumer contract for SPE ALLOW.
4. Create tag/release v0.5.0 if release tooling or an existing declared release task becomes available.
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
SDK-to-SPE integration implementation: FIXTURE-BOUND
SDK-to-SPE integration verification: PENDING CURRENT-MAIN RUN
Git tag/release: NOT YET RECORDED
```

Do not claim that the Git tag or GitHub release exists until repository evidence confirms creation.

## Next Integration Goal Candidate

After SDK envelope compatibility is verified, the next integration goal is preserving the SPE standing receipt through `master-records/orchestration` and into the governed execution-authority boundary without converting `ALLOW` into execution.

## Archive Note

The SDK-to-SPE implementation thread can continue entirely from this handoff, the canonical fixture, deterministic receipt examples, and the installed consumer tests.
