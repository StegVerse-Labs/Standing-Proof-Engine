# Frozen Manifests and Expected Results

Standing-Proof-Engine now commits two kinds of stability fixtures:

1. frozen hash manifests;
2. expected result fixtures.

## Frozen Hash Manifest

```text
samples/hash_manifests/external_source_ref_stale_state_001.hashes.json
```

This file pins the canonical SHA-256 hash for each local source object used by the external-reference sample.

Verify it with:

```bash
python spe/verify_hash_manifest.py samples/hash_manifests/external_source_ref_stale_state_001.hashes.json
```

Expected result:

```text
SPE RESULT: PASS
```

If any referenced source object changes without updating the manifest, the verifier fails.

## Expected Result Fixture

```text
expected_results/external_source_ref_stale_state_001.expected.json
```

This file pins the expected SPE result and required check statuses for the external-reference proof path.

Verify it with:

```bash
python spe/verify_expected_result.py expected_results/external_source_ref_stale_state_001.expected.json
```

Expected result:

```text
SPE RESULT: PASS
```

If verifier behavior changes, or if a required check no longer reports the expected status, the fixture verifier fails.

## Why Both Are Needed

The hash manifest detects source-material drift.

The expected result fixture detects verifier-semantics drift.

Together they make the proof path more stable:

```text
source object changed -> hash manifest fails
verifier behavior changed -> expected result fixture fails
standing result changed -> expected result fixture fails
```

## Current Scope

The current fixture set covers the external local-source-reference proof path.

Future fixture sets should cover:

- pressure receipts;
- embedded source-bound artifacts;
- failing examples;
- partial examples;
- cross-repository manifests.
