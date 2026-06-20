# External Source References

Standing-Proof-Engine can now verify a proof artifact whose source objects are stored as separate local JSON files.

## Sample Artifact

```text
samples/external_source_ref_stale_state_001.json
```

## Source Objects

The sample references local files under:

```text
samples/source_objects/
```

These files represent review artifacts, evidence packets, authority states, policy states, and context state.

## Verification Path

SPE performs the following steps:

1. Parse the proof artifact.
2. Read `source_object_refs`.
3. Resolve each local JSON reference inside the repository checkout.
4. Reject references that escape the repository root.
5. Load each referenced JSON source object.
6. Compute canonical SHA-256 hashes for the loaded source objects.
7. Verify declared hash bindings.
8. Run the standing evaluation.
9. Emit PASS, PARTIAL, or FAIL.

## Command

```bash
python spe/verify_external_refs.py samples/external_source_ref_stale_state_001.json
```

Expected result:

```text
SPE RESULT: PASS
```

## JSON Output

```bash
python spe/verify_external_refs.py --json samples/external_source_ref_stale_state_001.json
```

## Governance Meaning

This is stronger than embedded-only source objects because the proof artifact no longer has to carry every source object inline.

The reviewer can inspect:

```text
proof artifact -> local source refs -> source objects -> canonical hashes -> standing result
```

This begins to separate the proof envelope from the reviewed materials.

## Current Limitation

Only local JSON files inside the repository checkout are supported. Remote manifests, signatures, and cross-repository source references are future work.
