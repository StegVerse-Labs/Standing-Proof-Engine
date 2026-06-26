# Reviewer Execution Checklist

## Assumption

This checklist is for a reviewer evaluating the current SPE activation package from the repository root. It assumes Python 3.11 or later and no external package installation.

## Done Criteria

Review is complete when every command below runs and the reviewer can confirm the expected SPE and governance outcomes.

## 1. Individual Proof Routes

Run:

```bash
python spe/verify.py samples/pressure_demo_001.json
python spe/verify.py samples/stale_state_review_commit_001.json
python spe/verify.py samples/aegis_incident_standing_001.json
```

Expected:

```text
pressure_demo_001 -> SPE RESULT: PARTIAL
stale_state_review_commit_001 -> SPE RESULT: PASS
aegis_incident_standing_001 -> SPE RESULT: PASS
```

## 2. Route Package Manifest

Run:

```bash
python spe/verify_manifest.py samples/manifest.json
```

Expected:

```text
"spe_result": "PARTIAL"
"sample_count": 3
all samples -> "matches_expectation": true
```

## 3. Commitment Candidate Manifest

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

This manifest demonstrates that a user can assemble edge-case tests from Transition Table elements without changing the testing path. The Commitment Candidate remains non-authorizing, and SPE re-binds standing at commit time.

## 4. SDK-Bound Commitment Candidate Intake

Run:

```bash
python spe/verify_sdk_intake.py samples/sdk_intake_cc_001.json
python spe/verify_expected_result.py expected_results/sdk_intake_cc_001.expected.json
```

Expected:

```text
samples/sdk_intake_cc_001.json -> SPE RESULT: PASS
expected_results/sdk_intake_cc_001.expected.json -> SPE RESULT: PASS
```

This proves the Commitment Candidate manifest is not only a standalone manifest demo. It is bound by SDK intake receipt, manifest hash, declared sample count, SPE route package ID, and expected package status.

## 5. Expected Result Corpus

Run:

```bash
python spe/verify_expected_corpus.py
```

Expected:

```text
SPE RESULT: PASS
```

The expected-result corpus includes both the Commitment Candidate manifest fixture and the SDK-bound Commitment Candidate intake fixture, so drift in the six manifest-authored edge cases or their SDK receipt binding fails the corpus.

## 6. Machine-Readable Export

Run:

```bash
python spe/verify_json.py samples/aegis_incident_standing_001.json
```

Expected fields:

```text
spe_result
artifact_type
governance_summary
hashes
checks
```

Expected governance summary:

```text
decision -> DENY
commit_allowed -> false
aggregate_standing -> false
prior_review_replayable -> true
```

## 7. Formalism Tests

Run:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

Expected:

```text
OK
```

## 8. Reviewer Reports

Run:

```bash
python spe/report.py samples/pressure_demo_001.json reports/pressure_demo_001.md default
python spe/report.py samples/stale_state_review_commit_001.json reports/stale_state_review_commit_001.md default
python spe/report.py samples/aegis_incident_standing_001.json reports/aegis_incident_standing_001.md default
python spe/report_expected_corpus.py expected_results reports/expected_corpus
```

Expected generated files:

```text
reports/pressure_demo_001.md
reports/stale_state_review_commit_001.md
reports/aegis_incident_standing_001.md
reports/expected_corpus/README.md
```

## Reviewer Confirmation

The reviewer should be able to confirm:

```text
1. The pressure route produces a reconstructable denial with an intentionally partial proof gap.
2. The stale-state route proves prior review does not carry stale execution standing.
3. The Aegis route proves incident detection does not authorize defensive consequence by itself.
4. The Commitment Candidate route proves candidate presentation does not carry execution authority.
5. The manifest-authored edge cases produce FAIL_CLOSED when current actor, target, scope, policy, delegation, evidence, validity window, or recoverability no longer matches.
6. The SDK-bound Commitment Candidate receipt proves the manifest package is bound by SDK intake, manifest hash, declared sample count, route package ID, and expected package status.
7. Expected-result fixtures detect drift in either SPE result, governance result, or SDK route binding.
8. The current activation package is ready for reviewer handoff but not full repo completion.
```

## Failure Handling

A failed command means one of these occurred:

```text
artifact drift
expected-result drift
verifier regression
SDK intake binding drift
report generation regression
missing file
```

Do not reinterpret a failing result as a successful governance result. Fix the artifact, verifier, expectation, SDK receipt, or documentation so the route package is reconstructable again.
