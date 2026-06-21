# Reconstruction Pointer Binding

## Assumption

This is a local SPE fixture for master-records reconstruction handoff. It does not claim that `master-records/core-lite` has already ingested or confirmed the pointer.

## Done Criteria

Pointer binding is done when SPE can verify:

```text
pointer fixture exists
pointer references the SDK intake receipt
pointer binds the SDK intake receipt hash
pointer references the SPE route manifest
pointer binds the SPE route manifest hash
pointer target matches manifest package status and sample count
expected-result fixture covers pointer verification
CI runs pointer verification and expected-result validation
```

## Fixture

```text
samples/master_records_pointer_001.json
```

## Verifier

```bash
python spe/verify_pointer.py samples/master_records_pointer_001.json
```

Expected:

```text
SPE RESULT: PASS
```

## Expected Fixture

```text
expected_results/pointer_001.expected.json
```

## Verified Checks

```text
parse_pointer
source_hash_binding
manifest_hash_binding
target_binding
```

## Governance Meaning

The pointer does not reconstruct the full SPE package by itself. It proves that a downstream reconstruction target can be given stable references to the SDK intake receipt and SPE manifest package.

That creates this route:

```text
SDK intake receipt
-> SPE route manifest
-> reconstruction pointer
-> downstream reconstruction target
```

## Current Limitation

This is a local pointer fixture. The next stronger version should add confirmation from the destination repository and a master-records receipt that the pointer was installed or rejected.
