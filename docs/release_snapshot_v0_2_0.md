# Standing-Proof-Engine Release Snapshot v0.2.0

## Assumption

This is a documentation snapshot, not a GitHub release tag. It records the first SPE activation package that includes SDK intake, reconstruction pointer, and local confirmation receipt binding.

## Done Criteria

This snapshot is complete when it records:

```text
scope
included routes
verification commands
expected results
machine-readable outputs
CI coverage
known local-fixture limitations
next integration targets
propagation verification targets
```

## Scope

Version `v0.2.0` captures the SPE reviewer handoff package after local confirmation receipt binding.

The release theorem remains:

```text
Detection does not imply authority.
Review does not imply standing.
Replayability does not imply admissibility.
Consequence requires commit-time standing.
```

The integration theorem added by this snapshot is:

```text
Route declarations must bind to manifest hashes.
Reconstruction pointers must bind to source receipts and manifests.
Confirmation receipts must bind to reconstruction pointers before downstream standing is claimed.
```

## Included Routes

```text
1. pressure receipt drift denial
2. stale-state review-to-commit denial
3. Aegis incident detection-to-standing denial
4. SDK intake receipt binding
5. reconstruction pointer binding
6. local confirmation receipt binding
```

## Included Artifacts

```text
samples/pressure_demo_001.json
samples/stale_state_review_commit_001.json
samples/aegis_incident_standing_001.json
samples/manifest.json
samples/sdk_intake_receipt_001.json
samples/master_records_pointer_001.json
samples/master_records_confirmation_001.json
expected_results/sdk_intake_receipt_001.expected.json
expected_results/pointer_001.expected.json
expected_results/confirmation_001.expected.json
docs/sdk_intake_binding.md
docs/pointer_binding.md
docs/confirmation_binding.md
docs/sdk_intake_activation_closure.md
docs/pointer_activation_closure.md
docs/confirmation_activation_closure.md
SPE_MIRROR_HANDOFF.md
```

## Verification Commands

```bash
python spe/verify.py samples/pressure_demo_001.json
python spe/verify.py samples/stale_state_review_commit_001.json
python spe/verify.py samples/aegis_incident_standing_001.json
python spe/verify_manifest.py samples/manifest.json
python spe/verify_sdk_intake.py samples/sdk_intake_receipt_001.json
python spe/verify_pointer.py samples/master_records_pointer_001.json
python spe/verify_confirmation.py samples/master_records_confirmation_001.json
python spe/verify_expected_corpus.py
python spe/verify_confirmation_json.py samples/master_records_confirmation_001.json
python -m unittest discover -s tests -p 'test_*.py'
```

## Expected Results

```text
pressure_demo_001 -> PARTIAL / DENY
stale_state_review_commit_001 -> PASS / DENY
aegis_incident_standing_001 -> PASS / DENY
sample manifest -> PARTIAL
SDK intake binding -> PASS / PARTIAL
reconstruction pointer binding -> PASS / PARTIAL
confirmation binding -> PASS / ACCEPTED_FOR_RECONSTRUCTION
expected corpus -> PASS
formalism tests -> PASS
```

## CI Coverage

The workflow path is displayed here without the leading dot:

```text
github/workflows/verify.yml
```

Note: the actual repository path includes the leading dot.

The workflow verifies individual samples, the sample manifest, SDK intake binding, reconstruction pointer binding, confirmation binding, expected-result fixtures, expected corpus, JSON exports, reviewer report generation, and formalism tests.

## Known Limitations

```text
SDK intake receipt is a local SPE fixture.
Reconstruction pointer is a local SPE fixture.
Confirmation receipt is a local SPE fixture.
Destination-generated master-records event hash is not yet bound.
Install-or-reject replay path is not yet implemented.
Site, Publisher, admissibility wiki, and StegGuardian wiki propagation are not yet verified.
```

## Propagation Verification Targets

```text
StegVerse-Labs/Site
GCAT-BCAT-Engine/Publisher
admissibility-wiki
stegguardian-wiki
```

## Release Status

```text
Snapshot: v0.2.0
Activation package: READY FOR LOCAL REVIEWER HANDOFF
Full repo completion: NOT COMPLETE
Confirmation binding: PRESENT
Release tag: NOT CREATED
Propagation verification task: REQUIRED
```

## Next Integration Targets

```text
v0.3.0 -> destination event hash fixture
v0.4.0 -> install-or-reject replay path
v0.5.0 -> destination-generated master-records receipt chain
v0.6.0 -> propagation verification across Site, Publisher, admissibility wiki, and StegGuardian wiki
```
