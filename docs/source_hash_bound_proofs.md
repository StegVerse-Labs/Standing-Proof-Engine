# Source-Hash-Bound Proofs

Standing-Proof-Engine now supports a stronger sample format where source objects are embedded in the artifact and hash bindings are computed from those objects.

## Sample

```text
samples/source_hash_bound_stale_state_001.json
```

## What Changed

Earlier samples used declared placeholder hashes such as authority or policy hashes.

The source-bound sample adds:

```text
source_objects
```

and:

```text
declared_hash_bindings
```

The verifier computes canonical SHA-256 hashes for the embedded source objects and checks whether the declared bindings match.

## AUTO Bindings

The sample uses:

```text
"AUTO"
```

as a binding value.

This means the verifier computes the binding from the embedded source object during evaluation. A future sample may replace `AUTO` with the literal computed SHA-256 value once the artifact is frozen.

## Governance Meaning

This moves SPE closer to independent reconstruction:

```text
narrative claim
  ↓
embedded source object
  ↓
canonical hash
  ↓
declared binding check
  ↓
standing evaluation
```

A reviewer can now test whether a review-time or commit-time state claim is anchored to source data rather than relying only on a declared string.

## Current Command

```bash
python spe/verify_source_bound.py samples/source_hash_bound_stale_state_001.json
```

Expected result:

```text
SPE RESULT: PASS
```

The transition is still denied. The proof passes because SPE can reconstruct and verify why the denial follows from the source-bound artifact.

## Current Limitation

The source objects are embedded inside the sample artifact. SPE does not yet resolve external file references or remote manifests.

The next strengthening step is external source reference resolution.
