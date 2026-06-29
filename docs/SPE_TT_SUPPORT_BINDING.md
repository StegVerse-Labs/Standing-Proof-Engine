# SPE TT Support Family Binding

## Assumptions

1. `Admissible-Existence/TT` remains the canonical source for transition semantics.
2. SPE may carry a downstream support-family snapshot so public checks can run without private cross-organization checkout access.
3. The snapshot does not redefine TT semantics and does not grant commit-time permission.
4. Workflow paths displayed here without a leading period are iOS-safe display paths. Canonical workflow paths begin with a leading period.

## Done Definition

This step is done when SPE has a checked support-family TT snapshot covering validation, classification, boundary, installation, runtime, durable, and quarantine/failure transitions.

## Added Files

```text
data/tt/tt_support_transition_authority_manifest.json
spe/check_tt_support_manifest.py
```

## Covered Families

```text
Validation
Classification
Boundary
Installation
Execution
Commit
Quarantine/Failure
```

## Workflow

```text
github/workflows/spe-tt-binding.yml
```

The canonical repository path begins with a leading period.

The workflow now runs:

```bash
python spe/check_tt_authority_manifest.py
python spe/check_tt_support_manifest.py
python spe/verify_tt_manifest.py samples/alane_commitment_candidate_manifest.json
python spe/verify_manifest.py samples/alane_commitment_candidate_manifest.json
```

## Boundary

Support-family binding makes SPE aware of TT support transitions. It does not make SPE the TT source of truth, does not make a Commitment Candidate authorizing, and does not replace commit-time standing reconstruction.
