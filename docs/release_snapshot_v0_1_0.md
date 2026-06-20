# Standing-Proof-Engine Release Snapshot v0.1.0

## Assumption

This is a documentation snapshot, not a GitHub release tag. It records the first public activation package for reviewer handoff.

## Done Criteria

This snapshot is complete when it records:

```text
scope
included routes
verification commands
expected results
machine-readable outputs
CI coverage
known partial condition
next release targets
```

## Scope

Version `v0.1.0` captures the first activation-ready SPE proof route package.

The release theorem is:

```text
Detection does not imply authority.
Review does not imply standing.
Replayability does not imply admissibility.
Consequence requires commit-time standing.
```

## Included Routes

```text
1. pressure receipt drift denial
2. stale-state review-to-commit denial
3. Aegis incident detection-to-standing denial
```

## Included Artifacts

```text
samples/pressure_demo_001.json
samples/stale_state_review_commit_001.json
samples/aegis_incident_standing_001.json
samples/manifest.json
expected_results/aegis_incident_standing_001.expected.json
expected_results/external_source_ref_stale_state_001.expected.json
docs/activation_status.md
docs/sample_manifest_verification.md
docs/aegis_intelligence_mapping.md
docs/alane_minimal_proof_path.md
```

## Verification Commands

```bash
python spe/verify.py samples/pressure_demo_001.json
python spe/verify.py samples/stale_state_review_commit_001.json
python spe/verify.py samples/aegis_incident_standing_001.json
python spe/verify_manifest.py samples/manifest.json
python spe/verify_expected_corpus.py
python spe/verify_json.py samples/aegis_incident_standing_001.json
python -m unittest discover -s tests -p 'test_*.py'
```

## Expected Results

```text
pressure_demo_001 -> PARTIAL / DENY
stale_state_review_commit_001 -> PASS / DENY
aegis_incident_standing_001 -> PASS / DENY
sample manifest -> PARTIAL
expected corpus -> PASS
formalism tests -> PASS
```

## Known Partial Condition

The pressure trace intentionally records metadata-level authority-context drift while leaving one reference-frame hash unchanged. SPE therefore reports the trace as `PARTIAL`, not `PASS`.

This is expected behavior and is preserved to show that SPE distinguishes reconstructable denial from fully proven cryptographic standing context.

## Machine-Readable Output

`spe/verify_json.py` emits:

```text
spe_result
artifact_type
governance_summary
hashes
checks
```

The `governance_summary` field allows reviewer tooling to read the consequence decision without parsing the full artifact.

## CI Coverage

The workflow path is displayed here without the leading dot:

```text
github/workflows/verify.yml
```

Note: the actual repository path includes the leading dot.

The workflow verifies individual samples, the sample manifest, expected-result fixtures, expected corpus, JSON exports, reviewer report generation, and formalism tests.

## Release Status

```text
Snapshot: v0.1.0
Activation package: READY FOR REVIEWER HANDOFF
Full repo completion: NOT COMPLETE
Route package: PRESENT
CI coverage: PRESENT
Expected governance-result drift detection: PRESENT
```

## Next Release Targets

```text
v0.2.0 -> SDK intake receipt fixture binding
v0.3.0 -> master-records reconstruction pointer binding
v0.4.0 -> independent implementation fixture compatibility
v0.5.0 -> expanded stale-state variant matrix
```
