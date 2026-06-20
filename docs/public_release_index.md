# Standing-Proof-Engine Public Release Index

This index is the entry point for reviewing the first public SPE proof paths.

## Core Question

```text
Did this transition possess standing to bind consequence at commit time?
```

## Proof Paths

| Proof Path | Artifact | Verifier | Expected SPE Result | Purpose |
|---|---|---|---:|---|
| Pressure receipt | `samples/pressure_demo_001.json` | `spe/verify.py` | PARTIAL | Shows denial reconstruction with incomplete authority-context hash proof. |
| Stale-state review-to-commit | `samples/stale_state_review_commit_001.json` | `spe/verify.py` | PASS | Shows prior review remains useful but no longer carries execution standing. |
| Source-hash-bound stale state | `samples/source_hash_bound_stale_state_001.json` | `spe/verify_source_bound.py` | PASS | Computes canonical hashes for embedded source objects. |
| External source reference stale state | `samples/external_source_ref_stale_state_001.json` | `spe/verify_external_refs.py` | PASS | Resolves local JSON source references and verifies hash bindings. |

## Negative and Partial Corpus

| Corpus Case | Artifact | Expected SPE Result | Demonstrates |
|---|---|---:|---|
| Missing pressure receipt | `samples/negative/missing_pressure_receipt_fail.json` | FAIL | Required receipt absence is rejected. |
| Broken hash binding | `samples/negative/broken_hash_binding_fail.json` | FAIL | Declared hash mismatch is rejected. |
| Pressure proof gap | `samples/pressure_demo_001.json` | PARTIAL | Denial reconstructs, but authority-context proof is incomplete. |

## Commands

Run all expected-result fixtures:

```bash
python spe/verify_expected_corpus.py
```

Generate reviewer reports:

```bash
python spe/report_expected_corpus.py
```

Run the main workflow locally in pieces:

```bash
python spe/verify.py samples/pressure_demo_001.json
python spe/verify.py samples/stale_state_review_commit_001.json
python spe/verify_source_bound.py samples/source_hash_bound_stale_state_001.json
python spe/verify_external_refs.py samples/external_source_ref_stale_state_001.json
python spe/verify_hash_manifest.py samples/hash_manifests/external_source_ref_stale_state_001.hashes.json
python spe/verify_expected_corpus.py
```

## Reviewer Artifact

GitHub Actions uploads Markdown reviewer reports as:

```text
spe-reviewer-reports
```

The workflow path is shown here without the leading dot as `github/workflows/verify.yml`; the actual repository path includes the leading dot.

## Interpretation Rule

`PASS` means the artifact proves its claimed SPE result.

It does not necessarily mean the transition is allowed.

A `PASS` can prove a deterministic `DENY`.

A `PARTIAL` means the outcome may reconstruct, but at least one standing proof condition still requires inference.

A `FAIL` means the artifact does not support the claimed governance result under the selected verifier.

## Current Public Boundary

SPE currently supports:

- direct trace verification;
- stale-state standing verification;
- embedded source-object hash verification;
- local external JSON source-reference verification;
- frozen hash manifests;
- expected-result fixtures;
- reviewer Markdown reports.

SPE does not yet support:

- remote manifests;
- cryptographic signature verification;
- cross-repository source resolution;
- package release signing.
