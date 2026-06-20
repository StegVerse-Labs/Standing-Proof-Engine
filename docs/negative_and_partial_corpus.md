# Negative and Partial Corpus Coverage

Standing-Proof-Engine includes PASS, PARTIAL, and FAIL fixtures so the verifier demonstrates success, incompleteness, and rejection behavior.

## PASS Fixture

```text
expected_results/external_source_ref_stale_state_001.expected.json
```

This fixture proves the external-source-reference stale-state artifact reaches a valid SPE `PASS` result while the underlying transition is still denied.

## PARTIAL Fixture

```text
expected_results/pressure_demo_001.partial.expected.json
```

This fixture preserves the current pressure-receipt proof gap:

```text
authority_context_proof: PARTIAL
```

The artifact reconstructs denial, but the authority-context hash does not independently prove the claimed reference-frame change.

## FAIL Fixtures

```text
expected_results/missing_pressure_receipt_fail.expected.json
expected_results/broken_hash_binding_fail.expected.json
```

These fixtures prove SPE rejects artifacts when:

1. a required pressure receipt is missing;
2. a declared source hash does not match the computed canonical source-object hash.

## Corpus Verification

Run all expected-result fixtures with:

```bash
python spe/verify_expected_corpus.py
```

Expected result:

```text
SPE RESULT: PASS
```

That means every expected fixture matched its declared result. It does not mean every underlying artifact passed. Some fixtures are expected to fail, and the corpus passes only when those failures are correctly detected.

## Why This Matters

A verifier that only demonstrates success paths is weak.

SPE must prove it can also:

- identify incomplete standing proofs;
- reject missing evidence;
- reject mismatched hash bindings;
- preserve known partial states without falsely upgrading them to PASS.
