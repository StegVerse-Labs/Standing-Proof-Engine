# Propagation Verification Task v0.3.0

## Assumption

This task records the required propagation checks after the SPE v0.3.0 documentation snapshot. It does not claim the downstream repos have already been updated.

## Done Criteria

Propagation verification is complete when each target has been checked for whether the SPE v0.3.0 destination event and replay information has been applied or intentionally deferred.

## Source Package

```text
Org: StegVerse-Labs
Repo: Standing-Proof-Engine
Snapshot: docs/release_snapshot_v0_3_0.md
Handoff: SPE_MIRROR_HANDOFF.md
Candidate tag: v0.3.0
```

## Verification Targets

```text
StegVerse-Labs/Site
GCAT-BCAT-Engine/Publisher
admissibility-wiki
stegguardian-wiki
```

## Target Checks

For each target, verify:

```text
1. Does the target have a current *_MIRROR_HANDOFF.md file?
2. Does the handoff mention Standing-Proof-Engine v0.3.0 or destination event replay binding?
3. Does the target have a place to publish or mirror SPE status?
4. Is a change required, deferred, or not applicable?
5. If required, what file should be updated first?
```

## SPE Content to Propagate

```text
Destination events must bind to confirmation receipt hashes.
Replay artifacts must bind to destination event hashes.
Final states must be replayable as declared outcomes.
Both installed and not-installed paths must remain testable.
```

## Known Remaining Installs

```text
master-records/core-lite -> destination-generated event hash import
master-records/core-lite -> destination-generated receipt chain
StegVerse-Labs/Site -> public SPE v0.3.0 status page or release note
GCAT-BCAT-Engine/Publisher -> publication route update for SPE v0.3.0
admissibility-wiki -> standing/admissibility replay-boundary update
stegguardian-wiki -> guardian replay/final-state boundary update
```

## Completion Record

```text
Status: OPEN
Created by: Standing-Proof-Engine v0.3.0 local destination event and replay binding closure
Next executor: mirror/publisher verification session
```
