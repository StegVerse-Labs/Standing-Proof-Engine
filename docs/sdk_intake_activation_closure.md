# SDK Intake Activation Closure

## Assumption

This file closes the current SDK intake receipt binding goal inside `Standing-Proof-Engine`. It does not claim that the upstream SDK repository has generated the receipt from its own workflow.

## Done Criteria

SDK intake activation is closed when SPE can verify:

```text
SDK-origin receipt fixture exists
receipt declares the Standing-Proof-Engine route
receipt identifies the SPE manifest package
receipt binds the canonical manifest hash
receipt binds declared sample count to manifest sample count
receipt binds expected manifest package result
expected-result fixture covers the SDK receipt
expected-corpus reports include the SDK receipt
machine-readable JSON export includes SDK route metadata
CI runs the SDK receipt verifier, expected fixture, JSON export, and tests
```

## Closed Scope

```text
samples/sdk_intake_receipt_001.json
spe/verify_sdk_intake.py
spe/verify_sdk_intake_json.py
expected_results/sdk_intake_receipt_001.expected.json
docs/sdk_intake_binding.md
tests/test_sdk_intake.py
tests/test_sdk_intake_json_export.py
```

## Verification Commands

```bash
python spe/verify_sdk_intake.py samples/sdk_intake_receipt_001.json
python spe/verify_sdk_intake_json.py samples/sdk_intake_receipt_001.json
python spe/verify_expected_result.py expected_results/sdk_intake_receipt_001.expected.json
python spe/verify_expected_corpus.py
python -m unittest discover -s tests -p 'test_*.py'
```

## Expected Outcomes

```text
SDK intake verifier: PASS
SDK intake JSON export: PASS
SDK expected fixture: PASS
Expected corpus: PASS
Formalism tests: PASS
```

## Closure Meaning

SPE can now prove that an upstream intake receipt declares the SPE route package and binds that declaration to the current manifest hash and expected package result.

This closes the local SDK-to-SPE binding route.

## Next Integration Goal

The next integration goal should move from local SDK fixture binding to cross-repository reconstruction pointers.

Candidate next work:

```text
master-records reconstruction pointer fixture
route package pointer receipt
SPE-to-master-records hash handoff
reconstruction pointer verifier
expected-result fixture for reconstruction pointer binding
```
