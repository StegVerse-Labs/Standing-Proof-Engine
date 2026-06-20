# Standing-Proof-Engine

Standing-Proof-Engine (SPE) is a governance verification engine for determining whether a transition possessed sufficient standing to bind consequence at commit time.

A review artifact may remain valid, useful, and replayable while no longer carrying execution standing by itself. SPE evaluates that boundary.

## Core Question

> Did this transition possess standing to bind consequence at the moment of commitment?

## What This Repo Demonstrates First

SPE now includes two minimal proof paths.

### 1. Pressure-Receipt Trace

The pressure-receipt trace includes:

1. one agent;
2. one baseline authority state;
3. one policy/delegation drift event;
4. one pre-commit pressure receipt;
5. one attempted commit;
6. one deterministic DENY;
7. one replay path showing `v1 -> ADMIT` and `v2 -> DENY`.

The sample intentionally includes a partial proof condition: the trace metadata says the reference frame changed, but the recorded `reference_frame_hash` remains the same at the pressure boundary. SPE reports that as `PARTIAL`, not `PASS`, because an independent reviewer can infer authority-context drift from metadata but cannot prove it from the recorded hashes alone.

### 2. Stale-State Review-to-Commit Proof

The stale-state sample demonstrates the public proof path requested for review artifact vs execution standing:

1. the original review artifact remains replayable;
2. the evidence packet remains useful;
3. the originally reviewed transition remains reconstructable;
4. commit-time authority, policy, or evidence state has changed or become stale;
5. prior review no longer carries execution standing by itself;
6. the receipt resolves deterministic DENY;
7. the formalism test validates that denial path.

## Done Criteria

This initial repo is done when it can:

- parse the included artifacts;
- reconstruct review-time or baseline state;
- observe authority/policy/delegation drift;
- inspect pressure or standing receipts;
- evaluate local predicates;
- evaluate aggregate admissibility or aggregate standing;
- confirm commit denial;
- replay stated outcomes;
- report proof gaps as `PASS`, `PARTIAL`, or `FAIL`.

## Quick Start

Run the pressure-receipt trace:

```bash
python spe/verify.py samples/pressure_demo_001.json
```

Expected result:

```text
SPE RESULT: PARTIAL
```

Run the stale-state proof path:

```bash
python spe/verify.py samples/stale_state_review_commit_001.json
```

Expected result:

```text
SPE RESULT: PASS
```

Why does the stale-state proof return `PASS` when the transition is denied?

Because `PASS` means the artifact proves its governance result. In this case, the proven result is `DENY`.

## Status Levels

- `PASS`: the proof path is independently reconstructable from the artifact.
- `PARTIAL`: the outcome is reconstructable, but one or more standing claims require inference from narrative or metadata.
- `FAIL`: the artifact does not support the claimed governance result.

## Design Principle

Replayability is not standing.

Approval is not continuity.

Execution is not admissibility.

A transition may remain fully reconstructable while no longer possessing authority to bind consequence.

## Initial Public Use Cases

SPE is intended to support two related evaluation paths:

1. Pressure-receipt evaluation: can a verifier reconstruct why a commit was denied after drift?
2. Stale-state proof-path presentation: can a verifier show that a prior review remained useful but no longer carried execution standing at commit time?

## Repository Layout

```text
samples/pressure_demo_001.json              sample pressure-receipt trace
samples/stale_state_review_commit_001.json  sample review-to-commit stale-state proof
docs/alane_minimal_proof_path.md            public explanation of the stale-state proof path
spe/verify.py                               standalone verifier
tests/test_pressure_demo.py                 pressure trace formalism test
tests/test_pressure_demo_unittest.py        unittest-compatible pressure trace test
tests/test_stale_state_case.py              stale-state formalism test
.github/workflows/verify.yml                GitHub Actions verification
```

Note: the workflow path is displayed here without the leading dot in prose as `github/workflows/verify.yml`; the actual repository path must include the leading dot for GitHub Actions to run.

## Long-Term Goal

SPE should become a small interoperability verifier for governance artifacts from independent systems. It should evaluate whether the artifact proves consequence-binding standing without requiring trust in the originating implementation or narrative explanation.

StegVerse-Labs - 3% complete
Standing-Proof-Engine - 18% complete
18% complete vs Repo Activation
