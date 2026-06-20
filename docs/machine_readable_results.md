# Machine-Readable SPE Results

Standing-Proof-Engine can emit human-readable verification output or machine-readable JSON output.

## Human-Readable Output

```bash
python spe/verify.py samples/stale_state_review_commit_001.json
```

Example result:

```text
SPE RESULT: PASS
```

## Machine-Readable Output

```bash
python spe/verify_json.py samples/stale_state_review_commit_001.json
```

The JSON result contains:

```text
spe_result      PASS, PARTIAL, or FAIL
artifact_type   pressure_trace, stale_state_proof, or unsupported
hashes          canonical SHA-256 hashes for the artifact and object sections
checks          ordered verification checks with status and detail
```

## Canonical Hashing

SPE hashes JSON by:

1. sorting object keys;
2. using compact JSON separators;
3. preserving UTF-8 text;
4. hashing the canonical bytes with SHA-256.

This means two JSON objects with the same semantic fields but different key order produce the same hash.

## Why This Matters

Reviewers should not need to trust the author of a narrative explanation.

A verifier should be able to:

1. parse the artifact;
2. compute stable section hashes;
3. run standing checks;
4. emit a reproducible result;
5. explain which checks passed, partially passed, or failed.

## Current Scope

The current implementation computes canonical hashes from the sample JSON artifacts. It does not yet resolve external file references or verify cryptographic signatures.

Those are future strengthening steps.
