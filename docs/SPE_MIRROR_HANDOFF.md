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
python spe/run_tt_integration_checks.py
```

The runner executes the full SPE TT integration chain and writes local goal status output.

## Remaining Work

1. Confirm `SPE TT Binding` workflow is green after the unified runner commit.
2. Replace local-only status display with durable committed status if workflow write permissions are approved.
3. Propagate SPE TT integration status to Site, admissibility wiki, and SDK after the workflow is green.

## Boundary

This handoff does not grant commit-time permission, does not make Commitment Candidates authorizing, and does not move TT source authority into SPE.

## Current Completion Estimate

```text
StegVerse-Labs - 96%complete
Standing-Proof-Engine - 96%complete
Standing-Proof-Engine - 96%complete TO GOAL ACTIVATION
```

The complete thread is ready for archiving once workflow verification is green or the next downstream propagation handoff begins.
