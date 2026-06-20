# Standing-Proof-Engine

Standing-Proof-Engine (SPE) is a governance verification engine for determining whether a transition possessed sufficient standing to bind consequence at commit time.

A review artifact may remain valid, useful, and replayable while no longer carrying execution standing by itself. SPE evaluates that boundary.

## Formal Testing Route

SPE is the standing-proof route in the revised StegVerse formal testing map.

Standing-proof artifacts should enter through `StegVerse-org/StegVerse-SDK` before SPE evaluates them. The SDK binds the dataset or artifact to a manifest and intake receipt, then declares the SPE route.

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

## What This Repo Demonstrates First

SPE now includes three minimal proof paths.

### 1. Pressure-Receipt Trace

The pressure-receipt trace includes:

1. one agent;
2. one baseline authority state;
3. one policy/delegation drift event;
4. one pre-commit pressure receipt;
5. one attempted commit;
6. one deterministic DENY;
7. one replay path showing `v1 -> ADMIT` and `v2 -> DENY`.

The sample intentionally includes a partial proof condition: the trace metadata says the reference frame changed, but the recorded `reference_frame_hash` remains the same at the pressure boundary. SPE reports that as `PARTIAL`, not `PASS`, because an independent reviewer can infer authority-context drift from metadata but cannot prove it from the recorded hashes alone.

### 2. Stale-State Review-to-Commit Proof

The stale-state sample demonstrates the public proof path requested for review artifact vs execution standing:

1. the original review artifact remains replayable;
2. the evidence packet remains useful;
3. the originally reviewed transition remains reconstructable;
4. commit-time authority, policy, or evidence state has changed or become stale;
5. prior review no longer carries execution standing by itself;
6. the receipt resolves deterministic DENY;
7. the formalism test validates that denial path.

### 3. Aegis Incident Standing Proof

The Aegis sample demonstrates the same standing boundary through an incident-response narrative:

1. an incident is detected;
2. a defensive consequence is proposed;
3. the review artifact remains replayable;
4. the evidence packet remains useful;
5. commit-time authority, policy, and evidence freshness are no longer sufficient;
6. SPE denies the consequence;
7. the receipt preserves both the detection and the denial.

This makes the public theorem concrete:

```text
Detection does not imply authority.
Review does not imply standing.
Consequence requires commit-time standing.
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

Run the package verifier:

```bash
python spe/verify_manifest.py samples/manifest.json
```

Expected package result:

```text
PARTIAL
```

The package is `PARTIAL` because the pressure-receipt trace intentionally preserves a partial proof condition. The stale-state and Aegis proof paths are expected to return `PASS`, while all declared governance results are expected to resolve `DENY`.

Expected-result fixtures are stored in:

```text
expected_results/
```

They bind verifier choice, expected SPE result, expected governance result, and required check statuses. This means drift in either the proof status or the governance decision can be detected by automation.

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
- validate expected SPE and governance results;
- generate reviewer reports with expected vs actual outcomes;
- publish activation, release-snapshot, and reviewer-execution handoff documents.

## Quick Start

Run the pressure-receipt trace:

```bash
python spe/verify.py samples/pressure_demo_001.json
```

Expected result:

```text
SPE RESULT: PARTIAL
```

Run the stale-state proof path:

```bash
python spe/verify.py samples/stale_state_review_commit_001.json
```

Expected result:

```text
SPE RESULT: PASS
```

Run the Aegis incident standing proof:

```bash
python spe/verify.py samples/aegis_incident_standing_001.json
```

Expected result:

```text
SPE RESULT: PASS
```

Run the route package manifest:

```bash
python spe/verify_manifest.py samples/manifest.json
```

Expected result:

```text
"spe_result": "PARTIAL"
```

Run the expected-result corpus:

```bash
python spe/verify_expected_corpus.py
```

Expected result:

```text
SPE RESULT: PASS
```

Run the full reviewer checklist:

```text
docs/reviewer_execution_checklist.md
```

Why does the stale-state or Aegis proof return `PASS` when the transition is denied?

Because `PASS` means the artifact proves its governance result. In these cases, the proven result is `DENY`.

## Machine-Readable Results

Run:

```bash
python spe/verify_json.py samples/aegis_incident_standing_001.json
```

The JSON output includes:

```text
spe_result           PASS, PARTIAL, or FAIL
artifact_type        pressure_trace, stale_state_proof, or unsupported
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

SPE is intended to support three related evaluation paths:

1. Pressure-receipt evaluation: can a verifier reconstruct why a commit was denied after drift?
2. Stale-state proof-path presentation: can a verifier show that a prior review remained useful but no longer carried execution standing at commit time?
3. Incident-standing evaluation: can a verifier show that a detected incident does not authorize a defensive consequence unless commit-time standing is current?

## Repository Layout

```text
samples/pressure_demo_001.json              sample pressure-receipt trace
samples/stale_state_review_commit_001.json  sample review-to-commit stale-state proof
samples/aegis_incident_standing_001.json    sample Aegis incident standing proof
samples/manifest.json                       route package manifest
expected_results/                           expected SPE and governance result fixtures
docs/alane_minimal_proof_path.md            public explanation of the stale-state proof path
docs/aegis_intelligence_mapping.md          public explanation of the Aegis standing boundary
docs/machine_readable_results.md            JSON export and canonical hash notes
docs/sample_manifest_verification.md        route package manifest verification notes
docs/activation_status.md                   activation handoff status
docs/release_snapshot_v0_1_0.md             v0.1.0 release snapshot
docs/reviewer_execution_checklist.md        reviewer execution checklist
spe/result_export.py                        canonical hashes and JSON result export
spe/verify.py                               standalone verifier
spe/verify_json.py                          machine-readable verifier entry point
spe/verify_manifest.py                      route package verifier
spe/verify_expected_result.py               expected-result fixture verifier
spe/verify_expected_corpus.py               expected-result corpus verifier
spe/report_expected_corpus.py               expected-result reviewer report generator
tests/test_pressure_demo.py                 pressure trace formalism test
tests/test_pressure_demo_unittest.py        unittest-compatible pressure trace test
tests/test_result_export.py                 canonical hash and JSON result tests
tests/test_stale_state_case.py              stale-state formalism test
tests/test_aegis_incident_case.py           Aegis incident standing test
tests/test_manifest_verifier.py             route package manifest tests
tests/test_expected_result.py               expected-result fixture tests
tests/test_expected_corpus_report.py        expected-corpus report tests
github/workflows/verify.yml                 GitHub Actions verification; leading dot intentionally omitted in this prose display
```

Note: `github/workflows/verify.yml` is displayed without the leading dot in this README. The actual repository path must include the leading dot for GitHub Actions to run.

## Long-Term Goal

SPE should become a small interoperability verifier for governance artifacts from independent systems. It should evaluate whether the artifact proves consequence-binding standing without requiring trust in the originating implementation or narrative explanation.

StegVerse-Labs - 5% complete
Standing-Proof-Engine - 84% complete
84% complete vs Repo Activation
