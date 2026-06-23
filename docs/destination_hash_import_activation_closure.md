# Destination Hash Import Activation Closure

## Assumption

This file closes the local destination-generated event hash import goal inside `Standing-Proof-Engine`. It does not claim that `master-records/core-lite` has generated or exported the hash from its own workflow.

## Done Criteria

Destination hash import activation is closed when SPE can verify:

```text
hash import fixture exists
hash import references the destination event
hash import binds the local source event hash
hash import binds the imported destination event hash
source event verifies
imported hash result matches the expected event result
hash import flags are true
expected-result fixture covers hash import
formalism tests cover hash drift
repo-standing runner includes hash import verification
release readiness report includes hash import artifacts
```

## Closed Scope

```text
samples/destination_generated_event_hash_001.json
spe/verify_hash_import.py
expected_results/hash_import_001.expected.json
docs/destination_hash_import_binding.md
tests/test_hash_import.py
tools/run_repo_standing.py
tools/write_release_readiness.py
```

## Verification Commands

```bash
python spe/verify_hash_import.py samples/destination_generated_event_hash_001.json
python -m unittest tests.test_hash_import
python tools/run_repo_standing.py
python tools/run_repo_standing.py --json
python tools/run_repo_standing.py --write-reports
python tools/write_release_readiness.py
```

## Expected Outcomes

```text
Hash import verifier: PASS
Hash import tests: PASS
Repo standing: PASS
Release readiness: READY
```

## Closure Meaning

SPE can now verify a local import record that binds a destination event hash to the canonical local destination event. This reduces manual reviewer work because the repo-standing route and release-readiness route now cover the hash import path.

## Next Integration Goal

The next integration goal should add a destination-generated receipt chain fixture.

Candidate next work:

```text
destination receipt chain fixture
receipt chain verifier
receipt chain expected-result fixture
repo-standing coverage for receipt chain
release snapshot v0.5.0
```
