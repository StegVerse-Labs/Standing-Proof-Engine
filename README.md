# Standing-Proof-Engine

Standing-Proof-Engine (SPE) is a governance verification engine for determining whether a transition possessed sufficient standing to bind consequence at commit time.

A review artifact may remain valid, useful, and replayable while no longer carrying execution standing by itself. SPE evaluates that boundary.

## Current Goal

SPE is now integrating `Admissible-Existence/TT` as the canonical transition authority.

Assumption: TT provides canonical transition identity, handler references, fixtures, and receipt schemas. SPE consumes those references but does not redefine TT semantics.

Done means: Commitment Candidate tests carry a TT transition id, TT code reference, and TT transition resolution receipt before SPE evaluates commit-time standing.

## TT Binding

Initial TT binding is documented in:

```text
docs/SPE_TT_BINDING.md
```

The downstream TT authority snapshot is:

```text
data/tt/tt_transition_authority_manifest.json
```

The first bound transition is:

```text
T-221 Irreversible External Commit
```

Legacy Commitment Candidate cases using:

```text
reviewed_candidate_to_commit_attempt
```

resolve to:

```text
T-221
engine/transition_handlers/external_reality.py::irreversible_external_commit
```

Run:

```bash
python spe/verify_tt_manifest.py samples/alane_commitment_candidate_manifest.json
python spe/verify_manifest.py samples/alane_commitment_candidate_manifest.json
```

Expected:

```text
spe_tt_binding_result: PASS
spe_result: PASS
```

Workflow path displayed without leading period for iOS compatibility:

```text
github/workflows/spe-tt-binding.yml
```

The canonical repository path begins with a leading period.

## Formal Testing Route

Assumption: standing-proof artifacts enter through `StegVerse-org/StegVerse-SDK` before SPE evaluates them. The SDK binds the dataset or artifact to a manifest and intake receipt, then declares the SPE route.

Done means: a reviewer can run the documented commands, observe the expected SPE/governance results, and confirm that review, replayability, candidate presentation, SDK intake, standing, TT transition binding, and consequence remain separated.

```text
Dataset / fixture / governance artifact
→ StegVerse-org/StegVerse-SDK ingestion
→ manifest binding
→ receipt binding
→ Standing-Proof-Engine route declaration
→ TT transition resolution
→ commit-time standing proof
→ standing result receipt
```

Route role:

```text
SDK ingests.
TT defines transition semantics.
SPE proves standing.
Receipts bind every transition.
```

SPE is not a replacement for `StegVerse-org/stegverse-demo-suite` or `StegGhost/entity-sandbox-runner`. Demo-suite demonstrates public validation behavior. Entity-sandbox-runner stresses bounded entity behavior. SPE proves whether a reviewed artifact still has consequence-binding standing at commit time.

## Core Question

> Did this transition possess standing to bind consequence at the moment of commitment?

## What This Repo Demonstrates

SPE now includes:

```text
1. pressure-receipt trace
2. stale-state review-to-commit proof
3. Aegis incident standing proof
4. SDK intake binding for the original route package
5. manifest-authored Commitment Candidate edge-case package
6. SDK intake binding for the Commitment Candidate package
7. initial TT-bound Commitment Candidate route for T-221
```

## Proof Routes

### 1. Pressure-Receipt Trace

The pressure-receipt trace includes one agent, one baseline authority state, one policy/delegation drift event, one pre-commit pressure receipt, one attempted commit, one deterministic `DENY`, and one replay path showing `v1 -> ADMIT` and `v2 -> DENY`.

The sample intentionally includes a partial proof condition: the trace metadata says the reference frame changed, but the recorded `reference_frame_hash` remains the same at the pressure boundary. SPE reports that as `PARTIAL`, not `PASS`, because an independent reviewer can infer authority-context drift from metadata but cannot prove it from the recorded hashes alone.

### 2. Stale-State Review-to-Commit Proof

The stale-state sample demonstrates the public proof path requested for review artifact vs execution standing:

```text
review remains replayable
evidence remains useful
reviewed transition remains reconstructable
commit-time authority/policy/evidence is changed or stale
prior review does not carry execution standing by itself
receipt resolves deterministic DENY
formalism test validates the denial path
```

### 3. Aegis Incident Standing Proof

The Aegis sample demonstrates the same standing boundary through an incident-response narrative:

```text
incident detected
defensive consequence proposed
review artifact remains replayable
evidence packet remains useful
commit-time authority, policy, and evidence freshness are insufficient
SPE denies the consequence
receipt preserves detection and denial
```

This makes the public theorem concrete:

```text
Detection does not imply authority.
Review does not imply standing.
Candidate presentation does not imply execution authority.
Consequence requires commit-time standing.
```

### 4. SDK Intake Binding

The SDK intake fixture demonstrates upstream route declaration:

```text
samples/sdk_intake_receipt_001.json
```

Run:

```bash
python spe/verify_sdk_intake.py samples/sdk_intake_receipt_001.json
```

Expected:

```text
SPE RESULT: PASS
```

### 5. Commitment Candidate Manifest

The Commitment Candidate manifest demonstrates user-authored testing from Transition Table elements without adding a new test path for each case.

Current manifest:

```text
samples/alane_commitment_candidate_manifest.json
```

Run:

```bash
python spe/verify_manifest.py samples/alane_commitment_candidate_manifest.json
```

Expected:

```text
"spe_result": "PASS"
"sample_count": 6
all samples -> "source": "transition_case"
all samples -> "artifact_type": "commitment_candidate_test"
all samples -> "governance_result": "FAIL_CLOSED"
all samples -> "matches_expectation": true
```

The manifest covers:

```text
expired delegation
changed target scope
stale evidence
changed policy version
degraded recoverability
actor substitution
```

Each case proves that the Commitment Candidate presents a proposed crossing but does not carry execution authority. SPE re-binds standing at commit time and resolves `FAIL_CLOSED` when current actor, target, scope, policy, delegation, evidence, validity window, or recoverability no longer matches.

### 6. SDK-Bound Commitment Candidate Route

The SDK-bound Commitment Candidate receipt demonstrates that the manifest-authored edge-case package can be routed through the same SDK intake verifier used by the original route package.

Current receipt:

```text
samples/sdk_intake_cc_001.json
```

Run:

```bash
python spe/verify_sdk_intake.py samples/sdk_intake_cc_001.json
```

Expected:

```text
SPE RESULT: PASS
```

Expected-result fixture:

```text
expected_results/sdk_intake_cc_001.expected.json
```

Run:

```bash
python spe/verify_expected_result.py expected_results/sdk_intake_cc_001.expected.json
```

Expected:

```text
SPE RESULT: PASS
```

## Activation Snapshot

The current activation handoff is recorded in:

```text
docs/activation_status.md
docs/release_snapshot_v0_1_0.md
docs/reviewer_execution_checklist.md
```

`v0.1.0` is a documentation snapshot, not a GitHub release tag. It marks the first activation-ready reviewer handoff package.

Current status:

```text
Activation package: READY FOR REVIEWER HANDOFF
Full repo completion: NOT COMPLETE
Primary theorem: IMPLEMENTED IN TESTED SAMPLE ROUTES
Commitment Candidate route: PRESENT
Manifest-authored edge cases: PRESENT
SDK intake binding for original route: PRESENT
SDK intake binding for Commitment Candidate route: PRESENT
TT-bound Commitment Candidate route: PRESENT
CI route coverage: PRESENT
Expected governance-result drift detection: PRESENT
Reviewer report generation: PRESENT
Reviewer execution checklist: PRESENT
```

## Route Package Verification

The initial public route package is declared in:

```text
samples/manifest.json
```

Run:

```bash
python spe/verify_manifest.py samples/manifest.json
```

Expected package result:

```text
PARTIAL
```
