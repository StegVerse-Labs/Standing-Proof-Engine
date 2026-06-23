# Standing-Proof-Engine Snapshot v0.4.0

## Assumption

This is a documentation snapshot, not a GitHub release tag. It records the SPE package after local destination hash import binding and automated readiness reporting.

## Scope

Version `v0.4.0` captures the SPE reviewer handoff package after destination-generated event hash import binding.

## Included Route

```text
confirmation receipt
-> destination event
-> destination hash import
-> replayable destination state
```

## Included Hash Import Artifacts

```text
samples/destination_generated_event_hash_001.json
spe/verify_hash_import.py
expected_results/hash_import_001.expected.json
docs/destination_hash_import_binding.md
docs/destination_hash_import_activation_closure.md
tests/test_hash_import.py
```

## Included Automation Artifacts

```text
tools/run_repo_standing.py
tools/write_release_readiness.py
reports/repo_standing_template.json
reports/repo_standing_template.md
```

Generated CI outputs:

```text
reports/repo_standing.json
reports/repo_standing.md
reports/release_readiness.json
reports/release_readiness.md
```

## Verification Commands

```bash
python spe/verify_hash_import.py samples/destination_generated_event_hash_001.json
python -m unittest tests.test_hash_import
python tools/run_repo_standing.py
python tools/run_repo_standing.py --json
python tools/run_repo_standing.py --write-reports
python tools/write_release_readiness.py
python -m unittest discover -s tests -p 'test_*.py'
```

## Expected Results

```text
destination_generated_event_hash_001 -> PASS / INSTALLED
repo standing -> PASS
release readiness -> READY
formalism tests -> PASS
```

## Known Limitations

```text
The imported destination hash is represented locally.
The destination-generated receipt chain is not yet present.
Site, Publisher, admissibility wiki, and StegGuardian wiki propagation are not yet verified for v0.4.0.
```

## Next Integration Targets

```text
v0.5.0 -> destination-generated receipt chain fixture
v0.6.0 -> receipt-chain expected-result support
v0.7.0 -> propagation verification across Site, Publisher, admissibility wiki, and StegGuardian wiki
```
