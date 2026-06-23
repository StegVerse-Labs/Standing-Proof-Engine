# SPE Mirror Handoff

## Assumption

This file is the current handoff and task source of truth for `StegVerse-Labs/Standing-Proof-Engine`. It must be checked before continuing mirror, release, publication, or cross-repo update work.

## Done Criteria

The current build pass is done when the active destination-event/replay goal has:

```text
destination event fixtures
accepted and deferred replay fixtures
destination event verifier
replay verifier
formalism tests
CI coverage
activation closure
release snapshot update
mirror/publication verification task
```

## Active Repo

```text
Org: StegVerse-Labs
Repo: Standing-Proof-Engine
Active Goal: destination event and replay binding
```

## Current Handoff State

Completed in this thread:

```text
Standing proof routes
Aegis proof route
SDK intake receipt binding
SDK manifest hash binding
SDK JSON export
reconstruction pointer binding
pointer expected fixture
pointer CI coverage
pointer activation closure
confirmation fixture
confirmation verifier
confirmation expected fixture
confirmation reviewer-report alias
confirmation JSON export
confirmation CI coverage
confirmation activation closure
v0.2.0 release snapshot
destination event fixture
deferred destination event fixture
event replay fixture
deferred event replay fixture
destination event verifier
event replay verifier
destination/replay tests
destination/replay CI coverage
destination event activation closure
v0.3.0 release snapshot
v0.3.0 propagation verification task
```

Still required for the active goal:

```text
destination-generated event hash import
shared expected-result CLI support for event fixtures
destination-generated receipt chain
Site/Publisher/wiki propagation verification
```

## Known Files Added for Destination Event Goal

```text
samples/destination_event_001.json
samples/destination_event_deferred_001.json
samples/event_replay_001.json
samples/event_replay_deferred_001.json
spe/verify_destination_event.py
spe/verify_event_replay.py
expected_results/destination_event_001.expected.json
expected_results/destination_event_deferred_001.expected.json
expected_results/event_replay_001.expected.json
expected_results/event_replay_deferred_001.expected.json
docs/destination_event_binding.md
docs/event_replay_binding.md
docs/destination_event_activation_closure.md
docs/release_snapshot_v0_3_0.md
docs/propagation_verification_task_v0_3_0.md
tests/test_destination_event.py
tests/test_event_replay.py
tests/test_event_expected_results.py
```

## Known Downstream Destinations

```text
master-records/core-lite -> destination-generated event hash import and receipt chain
StegVerse-Labs/Site -> public release/status update after tag candidate
GCAT-BCAT-Engine/Publisher -> publication/update propagation check after tag candidate
admissibility-wiki -> governance theorem/update propagation check after tag candidate
stegguardian-wiki -> guardian/standing boundary propagation check after tag candidate
```

## Tag/Release Readiness

Current candidate after destination event/replay closure:

```text
v0.3.0
```

Do not tag until:

```text
workflow result is observed or checked
downstream propagation verification is opened or assigned
remaining destination targets are listed
```

## Next Action

Begin `v0.4.0` destination-generated event hash import, or hand off to mirror/publisher verification using `docs/propagation_verification_task_v0_3_0.md`.

## Archive Note

This handoff is intended to make the complete thread archivable. Future sessions should continue from this file rather than relying on full chat history.
