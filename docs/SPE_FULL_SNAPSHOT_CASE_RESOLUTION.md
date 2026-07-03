# SPE Full Snapshot Case Resolution

## Assumptions

1. `Admissible-Existence/TT` remains the canonical source for transition semantics.
2. SPE consumes a full downstream TT snapshot for deterministic public checks.
3. Case resolution through the full snapshot does not grant commit-time permission.
4. Workflow paths displayed here without a leading period are iOS-safe display paths. Canonical workflow paths begin with a leading period.

## Done Definition

This step is done when Commitment Candidate cases resolve their transition references through the full TT snapshot before the rest of the SPE manifest route is checked.

## Added File

```text
spe/check_full_snapshot_cases.py
```

## Verified Route

```bash
python spe/check_full_snapshot_cases.py samples/alane_commitment_candidate_manifest.json
```

Expected:

```text
result: PASS
```

## Workflow

```text
github/workflows/spe-tt-binding.yml
```

The canonical repository path begins with a leading period.

The workflow now checks full snapshot case resolution before support cases, receipt chains, TT-bound manifest checks, and the full SPE manifest route.

## Boundary

Full snapshot case resolution binds transition references to TT entries. It does not make a Commitment Candidate authorizing, does not replace standing reconstruction, and does not move TT source authority into SPE.
