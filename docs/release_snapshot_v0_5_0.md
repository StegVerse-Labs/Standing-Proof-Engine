# Standing-Proof-Engine Release Snapshot v0.5.0

## Assumption

This is a documentation snapshot, not a GitHub release tag. It records the local receipt-chain activation closure after the v0.4.0 destination hash import path.

## Done Criteria

This snapshot is complete when it records:

```text
scope
included receipt-chain artifacts
verification commands
expected results
CI/repo-standing coverage
known limits
next integration targets
```

## Scope

Version `v0.5.0` captures the local destination-generated receipt chain proof path.

The release theorem extension is:

```text
A destination hash import is stronger when it is bound into an ordered receipt chain.
A receipt chain is admissible only when source import, ordered receipts, artifact existence, final binding, and chain flags all verify.
```

## Included Artifacts

```text
samples/destination_receipt_chain_001.json
spe/verify_receipt_chain.py
expected_results/receipt_chain_001.expected.json
tests/test_receipt_chain.py
docs/destination_receipt_chain_activation_closure.md
tools/run_repo_standing.py
github/workflows/verify.yml
```

Note: `github/workflows/verify.yml` is displayed without the leading dot. The actual repository path includes the leading dot.

## Verification Commands

```bash
python spe/verify_receipt_chain.py samples/destination_receipt_chain_001.json
python spe/verify_expected_result.py expected_results/receipt_chain_001.expected.json
python -m unittest tests.test_receipt_chain
python tools/run_repo_standing.py
python tools/write_release_readiness.py
```

## Expected Results

```text
destination receipt chain -> PASS / CHAIN_BOUND
receipt chain expected fixture -> PASS
receipt chain tests -> PASS
repo standing -> PASS
release readiness -> READY
```

## CI and Repo-Standing Coverage

The receipt-chain route is covered by:

```text
github/workflows/verify.yml
tools/run_repo_standing.py
spe/verify_expected_corpus.py
```

CI verifies the expected-result fixture. Repo-standing verifies the direct receipt-chain command and the expected corpus.

## Known Limits

This snapshot verifies the local SPE receipt-chain shape. It does not claim that `master-records/core-lite` has emitted the chain from its own workflow yet.

## Release Status

```text
Snapshot: v0.5.0
Local activation package: COMPLETE
Full repo completion: NOT COMPLETE
Receipt chain route: PRESENT
Receipt chain verifier: PRESENT
Receipt chain expected fixture: PRESENT
Receipt chain tests: PRESENT
Repo-standing coverage: PRESENT
CI coverage: PRESENT
```

## Next Integration Targets

```text
master-records/core-lite -> emit destination-generated receipt chain
StegVerse-Labs/Site -> publish current SPE standing summary
Publisher/wiki propagation -> verify public references match release snapshots
```
