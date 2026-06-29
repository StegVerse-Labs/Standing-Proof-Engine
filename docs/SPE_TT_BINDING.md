# SPE TT Binding

## Assumptions

1. `Admissible-Existence/TT` is the canonical source for transition identity, handler references, fixtures, and receipt schemas.
2. SPE may keep a downstream authority snapshot so public workflow checks can run without private cross-organization checkout access.
3. The downstream TT snapshot does not redefine TT semantics and does not grant commit-time permission.
4. Workflow paths displayed here without a leading period are iOS-safe display paths. Canonical workflow paths begin with a leading period.

## Done Definition

This integration step is done when a Commitment Candidate manifest sample can be transformed into an SPE artifact carrying a TT transition id, TT code reference, and TT transition resolution receipt before SPE evaluates commit-time standing.

## Added Files

```text
data/tt/tt_transition_authority_manifest.json
spe/tt_registry.py
spe/verify_tt_manifest.py
github/workflows/spe-tt-binding.yml
```

The workflow path above is displayed without the leading period. The canonical repository path begins with a leading period.

## TT Source Boundary

```text
canonical_source: Admissible-Existence/TT
consumer: StegVerse-Labs/Standing-Proof-Engine
```

SPE consumes TT references. SPE does not become the TT source of truth.

## Current Bound Transition

The first bound transition is:

```text
T-221 Irreversible External Commit
```

Legacy SPE manifest cases that used:

```text
reviewed_candidate_to_commit_attempt
```

now resolve through the downstream TT authority manifest to:

```text
T-221
engine/transition_handlers/external_reality.py::irreversible_external_commit
```

## Verification Commands

```bash
python spe/verify_tt_manifest.py samples/alane_commitment_candidate_manifest.json
python spe/verify_manifest.py samples/alane_commitment_candidate_manifest.json
```

Expected:

```text
spe_tt_binding_result: PASS
spe_result: PASS
```

## Receipt Chain

Each generated Commitment Candidate artifact now includes:

```text
commitment_candidate.tt_transition_id
commitment_candidate.tt_code_ref
receipt.tt_transition_id
receipt.tt_transition_receipt
```

## Non-Claims

```text
TT binding does not grant commit-time permission.
TT binding does not make a Commitment Candidate authorizing.
TT binding does not replace SPE standing reconstruction.
TT binding does not move TT source authority into SPE.
```
