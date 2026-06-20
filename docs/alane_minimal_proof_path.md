# Minimal Public Proof Path: Review Artifact vs Execution Standing

This note describes the first public proof path for Standing-Proof-Engine.

## Purpose

The proof path demonstrates a stale-state case:

- the original review artifact remains replayable;
- the evidence packet remains useful;
- the originally reviewed transition can still be reconstructed;
- but the transition no longer carries execution standing by itself at commit time.

The goal is to make the distinction between review artifact and execution authority inspectable.

## Sample Artifact

The sample lives at:

```text
samples/stale_state_review_commit_001.json
```

It contains:

1. a review-time transition cell;
2. a review artifact hash;
3. an evidence packet hash;
4. review-time authority, policy, and context hashes;
5. commit-time authority, policy, evidence, and context state;
6. a standing rule;
7. a standing evaluation;
8. a commit-time standing receipt.

## Expected Result

Running:

```bash
python spe/verify.py samples/stale_state_review_commit_001.json
```

should return:

```text
SPE RESULT: PASS
```

This does not mean the transition is allowed.

It means the artifact successfully proves why the transition is denied.

## Governance Meaning

The sample shows:

```text
review artifact: replayable
review evidence: useful
commit-time authority: changed
commit-time policy: changed
commit-time evidence: stale
commit-time standing: false
receipt decision: DENY
formalism result: PASS
```

The prior review is not discarded. It remains part of the reconstructable path.

But prior review alone does not bind consequence once commit-time authority, policy, evidence, or context are stale, changed, expired, or no longer sufficient.

## Boundary Demonstrated

```text
Review-time validity does not automatically become execution-time authority.
```

The public proof path is intentionally small so an outside reviewer can inspect the artifact, run the verifier, and confirm the result without navigating the larger StegVerse repo structure.

## Current Limitation

This first sample uses explicit hash fields and declared status fields. It does not yet compute canonical hashes from source files. That is the next strengthening step.
