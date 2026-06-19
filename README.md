# Standing-Proof-Engine

Standing-Proof-Engine (SPE) is a governance verification engine for determining whether a transition possessed sufficient standing to bind consequence at commit time.

A review artifact may remain valid, useful, and replayable while no longer carrying execution standing by itself. SPE evaluates that boundary.

## Core Question

> Did this transition possess standing to bind consequence at the moment of commitment?

## What This Repo Demonstrates First

The first proof path uses a pressure-receipt trace with:

1. one agent;
2. one baseline authority state;
3. one policy/delegation drift event;
4. one pre-commit pressure receipt;
5. one attempted commit;
6. one deterministic DENY;
7. one replay path showing `v1 -> ADMIT` and `v2 -> DENY`.

The sample intentionally includes a partial proof condition: the trace metadata says the reference frame changed, but the recorded `reference_frame_hash` remains the same at the pressure boundary. SPE reports that as `PARTIAL`, not `PASS`, because an independent reviewer can infer authority-context drift from metadata but cannot prove it from the recorded hashes alone.

## Done Criteria

This initial repo is done when it can:

- parse the included trace;
- reconstruct baseline state;
- observe authority/policy/delegation drift;
- inspect the pressure receipt;
- evaluate local predicates;
- evaluate aggregate admissibility;
- confirm commit denial;
- replay the stated v1/v2 outcomes;
- report proof gaps as `PASS`, `PARTIAL`, or `FAIL`.

## Quick Start

```bash
python spe/verify.py samples/pressure_demo_001.json
```

Expected result:

```text
SPE RESULT: PARTIAL
```

Why `PARTIAL`?

Because the denial path is reconstructable, but the authority-context change is not fully cryptographically linked in the sample. A complete proof should include explicit policy and delegation-chain hashes or a changed reference-frame hash.

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
samples/pressure_demo_001.json   sample pressure-receipt trace
spe/verify.py                    standalone verifier
tests/test_pressure_demo.py      formalism test for the sample
.github/workflows/verify.yml     GitHub Actions verification
```

Note: the workflow path is displayed here without the leading dot in prose as `github/workflows/verify.yml`; the actual repository path must include the leading dot for GitHub Actions to run.

## Long-Term Goal

SPE should become a small interoperability verifier for governance artifacts from independent systems. It should evaluate whether the artifact proves consequence-binding standing without requiring trust in the originating implementation or narrative explanation.

StegVerse-Labs - 2% complete
Standing-Proof-Engine - 8% complete
8% complete vs Repo Activation