# SPE Full TT Snapshot Consumption

## Assumptions

1. `Admissible-Existence/TT` remains the canonical source for transition semantics.
2. SPE consumes downstream TT snapshots only to make public workflow verification deterministic.
3. The full SPE snapshot is a consumer view assembled from existing SPE downstream TT snapshots.
4. Workflow paths displayed here without a leading period are iOS-safe display paths. Canonical workflow paths begin with a leading period.

## Done Definition

This step is done when SPE can assemble and verify one full transition snapshot covering every currently implemented TT family and transition used by the downstream consumer snapshots.

## Added Files

```text
samples/tt_full_snapshot_expectation.json
spe/tt_full_snapshot.py
spe/check_tt_full_snapshot.py
docs/SPE_FULL_TT_SNAPSHOT.md
```

## Snapshot Inputs

```text
data/tt/tt_transition_authority_manifest.json
data/tt/tt_support_transition_authority_manifest.json
```

## Verified Snapshot Coverage

```text
transition_count: 64
families: Validation, Classification, Boundary, Installation, Execution, Commit, External Reality, Quarantine/Failure, Reconstruction
```

## Verification Command

```bash
python spe/check_tt_full_snapshot.py
```

Expected:

```text
PASS: SPE consumes a full TT transition snapshot with all expected families and transitions.
```

## Workflow

```text
github/workflows/spe-tt-binding.yml
```

The canonical repository path begins with a leading period.

The workflow now validates:

```text
TT consequence/reconstruction coverage
TT support-family coverage
full TT transition snapshot consumption
runtime support-transition cases
Commitment Candidate TT receipt chain
TT-bound Commitment Candidate manifest
SPE manifest route
```

## Boundary

Full snapshot consumption does not make SPE the TT source of truth, does not redefine TT semantics, does not grant commit-time permission, and does not make a Commitment Candidate authorizing.
