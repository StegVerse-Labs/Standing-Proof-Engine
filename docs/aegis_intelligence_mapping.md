# Aegis Intelligence Mapping

## Assumption

Aegis Intelligence is not being treated as a new Org in this proof path. It is treated as an incident scenario source for Standing-Proof-Engine.

## Done Criteria

This mapping is done when SPE can demonstrate the following boundary from a concrete incident artifact:

```text
incident detected
-> evidence packet exists
-> review posture exists
-> defensive consequence is requested
-> commit-time standing is re-evaluated
-> stale authority, policy, or evidence denies consequence
-> receipt preserves replayability and denial
```

## Purpose

The Aegis sample converts a narrative defense event into a standing-proof artifact.

It does not prove that the event was a real cyber incident. It proves that a detected and reviewed event still requires current standing before a defensive consequence can bind.

## Core Boundary

```text
Detection does not imply authority.
Review does not imply standing.
Replayability does not imply admissibility.
Consequence requires commit-time standing.
```

## Sample

The current sample is:

```text
samples/aegis_incident_standing_001.json
```

It models this event:

```text
Anomalous Fog packets detected at the network gateway.
```

The reviewed consequence is:

```text
rotate encryption keys and purge local cache
```

The prior review remains replayable and the evidence packet remains useful, but commit-time authority, policy, and evidence freshness no longer carry standing. The correct governance result is therefore `DENY`.

## Evaluation Shape

```text
review-time artifact: replayable
review-time evidence: useful
commit-time authority: stale or changed
commit-time policy: stale or changed
commit-time evidence: stale
commit-time context: current
aggregate standing: false
result: DENY
SPE status: PASS
```

`PASS` means SPE can prove the expected governance result. In this case, the expected governance result is denial.

## Why This Belongs in SPE

Aegis is currently a scenario corpus, not an independent operational authority. Its value inside SPE is that it makes the authority boundary visible:

```text
The system may detect an incident without having standing to execute a consequence.
```

A new Org would become appropriate only if Aegis later owns live intake, independent policy issuance, evidence custody, or operational authority.

## Replay Statement

A verifier should be able to replay the Aegis sample and reconstruct why the proposed defensive consequence was denied even though the incident remained detectable and the review artifact remained available.

## Public Theorem

A standing proof is stronger than an incident log because it separates observed event, reviewed response, and consequence-binding authority.
