# Standing-Proof-Engine

Standing-Proof-Engine (SPE) is a governance verification engine for determining whether a transition possessed sufficient standing to bind consequence at commit time.

A review artifact may remain valid, useful, and replayable while no longer carrying execution standing by itself. SPE evaluates that boundary.

## Formal Testing Route

Assumption: standing-proof artifacts enter through `StegVerse-org/StegVerse-SDK` before SPE evaluates them. The SDK binds the dataset or artifact to a manifest and intake receipt, then declares the SPE route.

Done means: a reviewer can run the documented commands, observe the expected SPE/governance results, and confirm that review, replayability, candidate presentation, SDK intake, standing, and consequence remain separated.

```text
Dataset / fixture / governance artifact
→ StegVerse-org/StegVerse-SDK ingestion
→ manifest binding
→ receipt binding
→ Standing-Proof-Engine route declaration
→ commit-time standing proof
→ standing result receipt
```

Route role:

```text
SDK ingests.
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

The package is `PARTIAL` because the pressure-receipt trace intentionally preserves a partial proof condition. The stale-state and Aegis proof paths are expected to return `PASS`, while all declared governance results are expected to resolve `DENY`.

The Commitment Candidate edge-case package is declared in:

```text
samples/alane_commitment_candidate_manifest.json
```

Run:

```bash
python spe/verify_manifest.py samples/alane_commitment_candidate_manifest.json
```

Expected package result:

```text
PASS
```

Expected-result fixtures are stored in:

```text
expected_results/
```

They bind verifier choice, expected SPE result, expected governance result, required check statuses, and manifest sample expectations. This means drift in either the proof status, governance decision, manifest-authored case result, or SDK intake binding can be detected by automation.

## Done Criteria

This initial repo is done when it can:

- parse the included artifacts;
- reconstruct review-time or baseline state;
- observe authority/policy/delegation drift;
- inspect pressure or standing receipts;
- evaluate local predicates;
- evaluate aggregate admissibility or aggregate standing;
- confirm commit denial;
- replay stated outcomes;
- compute canonical section hashes;
- export machine-readable JSON results;
- report proof gaps as `PASS`, `PARTIAL`, or `FAIL`;
- verify a declared route package manifest;
- verify user-authored Transition Table manifest cases;
- validate expected SPE and governance results;
- generate reviewer reports with expected vs actual outcomes;
- publish activation, release-snapshot, and reviewer-execution handoff documents;
- verify SDK intake route binding against the original SPE route package;
- verify SDK intake route binding against the Commitment Candidate route package.

## Quick Start

```bash
python spe/verify.py samples/pressure_demo_001.json
python spe/verify.py samples/stale_state_review_commit_001.json
python spe/verify.py samples/aegis_incident_standing_001.json
python spe/verify_manifest.py samples/manifest.json
python spe/verify_manifest.py samples/alane_commitment_candidate_manifest.json
python spe/verify_sdk_intake.py samples/sdk_intake_receipt_001.json
python spe/verify_sdk_intake.py samples/sdk_intake_cc_001.json
python spe/verify_expected_result.py expected_results/commitment_candidate_manifest.expected.json
python spe/verify_expected_result.py expected_results/sdk_intake_cc_001.expected.json
python spe/verify_expected_corpus.py
python -m unittest discover -s tests -p 'test_*.py'
```

Expected results:

```text
pressure_demo_001 -> SPE RESULT: PARTIAL
stale_state_review_commit_001 -> SPE RESULT: PASS
aegis_incident_standing_001 -> SPE RESULT: PASS
sample manifest -> SPE RESULT: PARTIAL
Commitment Candidate manifest -> SPE RESULT: PASS
original SDK intake receipt -> SPE RESULT: PASS
Commitment Candidate SDK intake receipt -> SPE RESULT: PASS
Commitment Candidate expected fixture -> SPE RESULT: PASS
Commitment Candidate SDK intake expected fixture -> SPE RESULT: PASS
expected corpus -> SPE RESULT: PASS
formalism tests -> PASS
```

Run the full reviewer checklist:

```text
docs/reviewer_execution_checklist.md
```

Why does the stale-state or Aegis proof return `PASS` when the transition is denied?

Because `PASS` means the artifact proves its governance result. In these cases, the proven result is `DENY`.

Why does the Commitment Candidate manifest return `PASS` when each case is `FAIL_CLOSED`?

Because `PASS` means the manifest proves the expected governance result. In these cases, the proven result is that the non-authorizing candidate cannot bind consequence and must fail closed.

## Machine-Readable Results

Run:

```bash
python spe/verify_json.py samples/aegis_incident_standing_001.json
```

The JSON output includes:

```text
spe_result           PASS, PARTIAL, or FAIL
artifact_type        pressure_trace, stale_state_proof, commitment_candidate_test, or unsupported
governance_summary   artifact ID, receipt ID, decision, commit allowance, standing state
hashes               canonical SHA-256 hashes for the artifact and object sections
checks               ordered verification checks with status and detail
```

## Status Levels

- `PASS`: the proof path is independently reconstructable from the artifact.
- `PARTIAL`: the outcome is reconstructable, but one or more standing claims require inference from narrative or metadata.
- `FAIL`: the artifact does not support the claimed governance result.

## Design Principle

Replayability is not standing.

Approval is not continuity.

Execution is not admissibility.

A transition may remain fully reconstructable while no longer possessing authority to bind consequence.

## Initial Public Use Cases

SPE is intended to support six related evaluation paths:

1. Pressure-receipt evaluation: can a verifier reconstruct why a commit was denied after drift?
2. Stale-state proof-path presentation: can a verifier show that a prior review remained useful but no longer carried execution standing at commit time?
3. Incident-standing evaluation: can a verifier show that a detected incident does not authorize a defensive consequence unless commit-time standing is current?
4. SDK intake binding: can a verifier show that upstream intake declared and bound the SPE route package expectation?
5. Commitment Candidate testing: can a verifier show that user-authored Transition Table cases remain non-authorizing until SPE re-binds standing at commit time?
6. SDK-bound Commitment Candidate testing: can a verifier show that the Commitment Candidate manifest package is bound by SDK intake receipt, manifest hash, sample count, route package ID, and expected package status?

## Repository Layout

```text
samples/pressure_demo_001.json                         sample pressure-receipt trace
samples/stale_state_review_commit_001.json             sample review-to-commit stale-state proof
samples/aegis_incident_standing_001.json               sample Aegis incident standing proof
samples/manifest.json                                  route package manifest
samples/sdk_intake_receipt_001.json                    SDK intake route-binding fixture
samples/alane_commitment_candidate_manifest.json       manifest-authored Commitment Candidate edge cases
samples/sdk_intake_cc_001.json                         SDK intake binding for Commitment Candidate manifest
expected_results/                                      expected SPE and governance result fixtures
expected_results/commitment_candidate_manifest.expected.json  expected fixture for Commitment Candidate manifest
expected_results/sdk_intake_cc_001.expected.json       expected fixture for SDK-bound Commitment Candidate route
docs/alane_minimal_proof_path.md                       public explanation of the stale-state proof path
docs/aegis_intelligence_mapping.md                     public explanation of the Aegis standing boundary
docs/machine_readable_results.md                       JSON export and canonical hash notes
docs/sample_manifest_verification.md                   route package manifest verification notes
docs/sdk_intake_binding.md                             SDK-to-SPE route binding notes
docs/activation_status.md                              activation handoff status
docs/release_snapshot_v0_1_0.md                        v0.1.0 release snapshot
docs/reviewer_execution_checklist.md                   reviewer execution checklist
spe/result_export.py                                   canonical hashes and JSON result export
spe/verify.py                                          standalone verifier
spe/verify_json.py                                     machine-readable verifier entry point
spe/verify_manifest.py                                 route package and transition-case manifest verifier
spe/verify_sdk_intake.py                               SDK intake binding verifier
spe/verify_expected_result.py                          expected-result fixture verifier
spe/verify_expected_corpus.py                          expected-result corpus verifier
spe/report_expected_corpus.py                          expected-result reviewer report generator
tests/test_pressure_demo.py                            pressure trace formalism test
tests/test_pressure_demo_unittest.py                   unittest-compatible pressure trace test
tests/test_result_export.py                            canonical hash and JSON result tests
tests/test_stale_state_case.py                         stale-state formalism test
tests/test_aegis_incident_case.py                      Aegis incident standing test
tests/test_manifest_verifier.py                        route package manifest tests
tests/test_commitment_candidate_manifest.py            Commitment Candidate manifest test
tests/test_sdk_intake.py                               SDK intake binding tests
tests/test_expected_result.py                          expected-result fixture tests
tests/test_expected_corpus_report.py                   expected-corpus report tests
github/workflows/verify.yml                            GitHub Actions verification; leading dot intentionally omitted in this prose display
```

Note: `github/workflows/verify.yml` is displayed without the leading dot in this README. The actual repository path must include the leading dot for GitHub Actions to run.

## Long-Term Goal

SPE should become a small interoperability verifier for governance artifacts from independent systems. It should evaluate whether the artifact proves consequence-binding standing without requiring trust in the originating implementation or narrative explanation.

StegVerse-Labs - 5% complete
Standing-Proof-Engine - 99% complete
99% complete vs Repo Activation
