# Heartbeat-Guided Path Selection and IICT

Status: Ongoing research  
Scope: Standing-Proof-Engine / StegVerse micro-node and repo-node governance  
Creator: Rigel Randolph

## Summary

This note records an ongoing research path connecting the StegVerse system heartbeat, micro-node ephemeral validity rotation, tetrahedron governance enforcement, factor-bound action recording, and Irreversibility-Inference Convergence Theory (IICT).

The core claim is not that heartbeat deviation alone determines system degradation. Rather, heartbeat and `ΔHeartbeat` act as timing and coherency signals within a broader system-state vector. They help determine when the ecosystem should continue, refresh, rotate, reroute, deepen verification, rollback, quarantine, or fail closed.

## Static Repo Failure vs Dynamic Ecosystem Operation

A static repository behaves as if action only occurs when an external actor pushes a commit or triggers a workflow. In that model, derived artifacts such as frozen hashes, receipts, expected-result fixtures, and verifier outputs can become stale between updates. The system then consumes stale state during validation and fails downstream.

A StegVerse repo-node should not behave only as a passive artifact store. It should act as a living participant in a dynamic ecosystem. It should continuously maintain standing by observing local state, deriving dependent values, refreshing volatile bindings, recording receipts, and routing state transitions before stale material is consumed.

The desired loop is:

```text
observe local derived state
recompute or recheck volatile bindings
consume only admissible current state
record the decision and contributing factors
route stale or conflicting state to refresh, rollback, quarantine, or fail-closed behavior
```

## System Heartbeat

The system heartbeat is the timing substrate of the ecosystem. It is not merely a liveness signal. It is the cadence by which ephemeral authority, short-lived validation material, token rotation, receipt freshness, and micro-node continuity are maintained across the system.

The heartbeat may operate at a high frequency, potentially in the MHz range, so that refresh and successor-token preparation can occur before expiry rather than after failure.

At each heartbeat interval, the system can evaluate whether active tokens remain valid, whether any token is approaching its refresh horizon, whether successor tokens are ready, and whether any token has been revoked, conflicted, expired, or orphaned.

## Ephemeral Validity Rotation

Short-lived tokens should not be revalidated at every consumption boundary. Doing so would defeat their purpose and introduce unnecessary delay.

Instead, each token should be accepted during its declared validity window while the heartbeat coordinates successor preparation and rotation.

A token validity record should include fields such as:

```json
{
  "token_id": "node-token-001",
  "valid_from": "2026-06-24T03:00:00Z",
  "expires_at": "2026-06-24T03:05:00Z",
  "refresh_after": "2026-06-24T03:04:00Z",
  "refresh_deadline": "2026-06-24T03:04:55Z",
  "successor_required": true,
  "successor_token_ref": null,
  "on_valid": "CONSUME",
  "on_near_expiry": "REFRESH_IN_PARALLEL",
  "on_expired_with_successor": "ROTATE",
  "on_expired_without_successor": "FAIL_CLOSED",
  "on_revoked": "FAIL_CLOSED"
}
```

The transition states are:

```text
TOKEN_VALID -> CONSUME
TOKEN_NEAR_EXPIRY -> REFRESH_IN_PARALLEL + CONTINUE
TOKEN_REFRESHED -> ROTATE + RECORD
TOKEN_EXPIRED_WITH_SUCCESSOR_READY -> CONSUME_SUCCESSOR
TOKEN_EXPIRED_WITHOUT_SUCCESSOR -> FAIL_CLOSED
TOKEN_REVOKED_OR_CONFLICTED -> FAIL_CLOSED
TOKEN_STATUS_UNKNOWN -> QUARANTINE_OR_RECHECK
```

## Derived-State Refresh

Derived hashes, receipts, and expected-result bindings are different from ephemeral tokens.

Ephemeral tokens are validity-window objects. They remain consumable until expiry unless revoked or conflicted.

Derived hashes are state-derived bindings. They must be recomputed when their source state changes.

The ecosystem should therefore distinguish:

```text
EPHEMERAL_VALIDITY_ROTATION
DERIVED_STATE_REFRESH
```

A derived-state refresh loop should behave as follows:

```text
source state changes
-> recompute derived value
-> record updated hash or receipt
-> recheck derived chain
-> allow downstream consumption only after derived state is current
```

## ΔHeartbeat as a Stress Signal

`ΔHeartbeat` is the observed deviation from nominal heartbeat cadence:

```text
ΔHeartbeat = observed heartbeat interval - nominal heartbeat interval
```

`ΔHeartbeat` should not determine system degradation alone. It should be treated as an early-warning or contributing stress signal.

A broader state vector should include:

```text
ΔHeartbeat
token refresh success rate
successor-token readiness
receipt latency
micro-node queue depth
verification delay
hash-refresh delay
rollback frequency
fail-closed frequency
resource saturation
network transport delay
state reconstruction latency
```

A soft stress state may trigger increased observation, refresh priority, redundancy, queue inspection, or load balancing. A hard standing failure should require corroborating signals such as missed refresh deadlines, expired tokens without successors, failed receipt chains, conflicting state, unrecoverable hash drift, or repeated rollback attempts.

## Tetrahedron Governance Enforcement

The tetrahedron governance model provides the structural admissibility frame. One common formulation uses:

```text
authority
policy
evidence
context
```

Another formulation may use:

```text
identity
delegation
state
execution boundary
```

Heartbeat and `ΔHeartbeat` are not replacements for these governance anchors. They are dynamic signals that help determine whether the system can maintain coherence while satisfying them.

The system coherency vector may be modeled as:

```text
Coherency(t) = f(
  authority_state,
  policy_state,
  evidence_state,
  context_state,
  ΔHeartbeat,
  token_refresh_status,
  receipt_latency,
  queue_depth,
  rollback_pressure,
  recoverability,
  execution_boundary_distance
)
```

## Heartbeat-Guided Path Selection

The system may have more than one possible path toward an admissible outcome. Some paths may be faster but require tighter timing. Some may be slower but more recoverable. Others may preserve authority but require deeper proof, defer execution, reroute through alternate nodes, or roll back to a prior admissible state.

Heartbeat and `ΔHeartbeat` help estimate path viability.

For example:

```text
low ΔHeartbeat + stable receipts
-> continue normal route

moderate ΔHeartbeat + token refresh pressure
-> pre-rotate tokens and continue

high ΔHeartbeat + queue growth
-> shed noncritical work and preserve core authority

high ΔHeartbeat + receipt latency
-> route through alternate node

high ΔHeartbeat + weak evidence currency
-> increase proof depth or pause execution

high ΔHeartbeat + missed refresh boundary
-> rollback, reconstruct, or fail closed
```

The system is not merely asking whether a state is valid. It is also asking which path keeps the system converging toward an admissible solution with the least loss of coherence, authority, recoverability, and continuity.

## Factor-Bound Action Recording

Heartbeat-guided path selection allows the system to record the factors contributing to every state transition.

A transition should not be recorded merely as:

```text
STATE_A -> STATE_B
```

It should record the factors that made the transition admissible:

```text
prior state
proposed transition
available paths
selected path
authority condition
policy condition
evidence condition
context condition
heartbeat condition
ΔHeartbeat
token validity condition
successor-token readiness
receipt latency
queue depth
resource pressure
refresh status
rollback availability
recoverability profile
reason for path selection
reason rejected paths were not selected
final transition result
```

This creates a richer standing record than a pass/fail result. The transition receipt becomes a state-decision explanation that binds the system action to the observable conditions present at the time of transition.

## Relationship to IICT

Irreversibility-Inference Convergence Theory describes convergence by minimizing the distance between the point of inference and the point of irreversibility.

Heartbeat-guided path selection operationalizes this idea.

```text
Inference window
-> system observes possible paths
-> heartbeat measures timing and coherency pressure
-> governance tetrahedron constrains admissible options
-> transition table selects path
-> micro-node acts or defers
-> receipt records contributing factors
-> system approaches or avoids irreversibility
```

Stale hashes, expiring tokens, delayed receipts, and degraded heartbeat are all examples of the same deeper problem: the system may approach irreversibility with outdated inference.

The dynamic ecosystem solution is:

```text
refresh inference before irreversibility,
or choose a path that delays, reroutes, rolls back, quarantines, or fails closed.
```

## Research Status

This is ongoing research. The current implementation direction is to model these concepts first inside Standing-Proof-Engine, then scale the same behavior to repo-node, org-node, and ecosystem-level ingestion and publication paths.

Open implementation questions include:

1. How should heartbeat cadence be represented in receipts?
2. How should `ΔHeartbeat` be normalized across heterogeneous nodes?
3. What threshold separates ordinary timing variance from actionable stress?
4. Which paths should be available at micro-node, repo-node, org-node, and master-record levels?
5. When should refresh occur automatically, and when should a stale condition only produce `REFRESH_REQUIRED`?
6. How should path alternatives and rejected paths be recorded without creating excessive receipt volume?
7. How should this model interact with the existing transition table and commit-time standing determinations?
