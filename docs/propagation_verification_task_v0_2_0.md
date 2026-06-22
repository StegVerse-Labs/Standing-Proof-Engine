# Propagation Verification Task v0.2.0

## Assumption

This task records the required propagation checks after the SPE v0.2.0 documentation snapshot. It does not claim the downstream repos have already been updated.

## Done Criteria

Propagation verification is complete when each target has been checked for whether the SPE v0.2.0 standing and confirmation-binding information has been applied or intentionally deferred.

## Source Package

```text
Org: StegVerse-Labs
Repo: Standing-Proof-Engine
Snapshot: docs/release_snapshot_v0_2_0.md
Handoff: SPE_MIRROR_HANDOFF.md
Candidate tag: v0.2.0
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
2. Does the handoff mention Standing-Proof-Engine v0.2.0 or the current confirmation-binding route?
3. Does the target have a place to publish or mirror SPE status?
4. Is a change required, deferred, or not applicable?
5. If required, what file should be updated first?
```

## SPE Content to Propagate

```text
Detection does not imply authority.
Review does not imply standing.
Replayability does not imply admissibility.
Consequence requires commit-time standing.
Route declarations must bind to manifest hashes.
Reconstruction pointers must bind to source receipts and manifests.
Confirmation receipts must bind to reconstruction pointers before downstream standing is claimed.
```

## Known Remaining Installs

```text
master-records/core-lite -> destination event hash fixture
master-records/core-lite -> install-or-reject replay artifact
master-records/core-lite -> destination-generated confirmation receipt chain
StegVerse-Labs/Site -> public SPE v0.2.0 status page or release note
GCAT-BCAT-Engine/Publisher -> publication route update for SPE v0.2.0
admissibility-wiki -> standing/admissibility theorem update
stegguardian-wiki -> guardian standing boundary update
```

## Completion Record

```text
Status: OPEN
Created by: Standing-Proof-Engine v0.2.0 local confirmation binding closure
Next executor: mirror/publisher verification session
```
