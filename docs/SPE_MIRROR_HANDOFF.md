# SPE Mirror Handoff

## Assumptions

1. This file is the current handoff source of truth for `StegVerse-Labs/Standing-Proof-Engine`.
2. `Admissible-Existence/TT` remains the canonical source for transition semantics.
3. SPE consumes TT snapshots and verifies standing routes; it does not redefine TT.
4. Workflow paths displayed here without a leading period are iOS-safe display paths. Canonical workflow paths begin with a leading period.

## Current Goal

Activate SPE TT integration so Commitment Candidate standing checks resolve through TT transition identity, handler references, fixtures, receipt schemas, and full-snapshot coverage before SPE evaluates commit-time standing.

## Current Build State

Implemented:

```text
data/tt/tt_transition_authority_manifest.json
data/tt/tt_support_transition_authority_manifest.json
spe/tt_registry.py
spe/tt_full_snapshot.py
spe/check_tt_authority_manifest.py
spe/check_tt_support_manifest.py
spe/check_tt_full_snapshot.py
spe/check_full_snapshot_cases.py
spe/verify_tt_support_cases.py
spe/verify_commitment_candidate_receipt_chain.py
spe/check_spe_tt_activation_goal.py
spe/write_tt_goal_status.py
spe/check_no_manual_tt_tasks.py
spe/run_tt_integration_checks.py
```

Samples and expectations:

```text
samples/tt_transition_authority_manifest_check.json
samples/tt_support_transition_cases_manifest.json
samples/commitment_candidate_receipt_chain_expectation.json
samples/tt_full_snapshot_expectation.json
samples/spe_tt_activation_goal.json
```

Documentation:

```text
docs/SPE_TT_BINDING.md
docs/SPE_TT_SUPPORT_BINDING.md
docs/SPE_COMMITMENT_CANDIDATE_RECEIPT_CHAIN.md
docs/SPE_FULL_TT_SNAPSHOT.md
docs/SPE_FULL_SNAPSHOT_CASE_RESOLUTION.md
docs/SPE_TT_STATUS.md
```

Workflow:

```text
github/workflows/spe-tt-binding.yml
github/workflows/spe-tt-goal-status.yml
```

## Verification

Run:

```bash
python -m spe.run_tt_integration_checks
```

The runner executes the full SPE TT integration chain and invokes each nested checker as a Python module from the repository root.

The no-manual-task validator requires the canonical module command and rejects the legacy direct-script form:

```text
python spe/run_tt_integration_checks.py
```

## Current Repair State

```text
Nested module execution repair: e9a024090808d35e83f724c85c0c3d227cac4bd1
Canonical invocation validator repair: 8c72090fa914c4eab6fb106c3643197675b064ac
```

The latest observed failure showed all substantive TT checks passing. Only the stale workflow-term assertion failed, and that assertion is now aligned with the canonical module invocation.

## Remaining Work

1. Confirm `SPE TT Binding` is green after the validator repair.
2. Record a passing TT binding receipt or durable status artifact.
3. Tag/release `v0.5.0` only after all required checks are green.
4. Propagate verified SPE TT integration status to Site, Publisher, admissibility-wiki, stegguardian-wiki, and SDK.

## Boundary

This handoff does not grant commit-time permission, does not make Commitment Candidates authorizing, and does not move TT source authority into SPE.

## Current Completion Estimate

```text
StegVerse-Labs - 97%complete
Standing-Proof-Engine - 98%complete
Standing-Proof-Engine - 97%complete TO GOAL ACTIVATION
```

The complete thread is ready for archiving once workflow verification is green or the next downstream propagation handoff begins.
