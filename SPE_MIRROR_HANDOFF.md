# SPE Mirror Handoff

## Assumption

This file is the current handoff and task source of truth for `StegVerse-Labs/Standing-Proof-Engine`. It must be checked before continuing mirror, release, publication, or cross-repo update work.

## Done Criteria

The current build pass is done when the active hash-import goal has:

```text
destination hash import fixture
hash import verifier
hash import expected fixture
hash import tests
repo-standing automation
release-readiness automation
activation closure
snapshot update
remaining external targets listed
```

## Active Repo

```text
Org: StegVerse-Labs
Repo: Standing-Proof-Engine
Active Goal: destination-generated event hash import
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
destination hash import fixture
hash import verifier
hash import expected fixture
hash import tests
repo-standing automation
release-readiness automation
destination hash import activation closure
v0.4.0 snapshot
```

Still required after this goal:

```text
destination-generated receipt chain
shared expected-result CLI support for event fixtures
Site/Publisher/wiki propagation verification
```

## Known Files Added for Hash Import Goal

```text
samples/destination_generated_event_hash_001.json
spe/verify_hash_import.py
expected_results/hash_import_001.expected.json
docs/destination_hash_import_binding.md
docs/destination_hash_import_activation_closure.md
docs/release_snapshot_v0_4_0.md
tests/test_hash_import.py
tools/run_repo_standing.py
tools/write_release_readiness.py
docs/no_manual_tasks_automation.md
docs/automation_backlog_v0_4_0.md
```

## Known Downstream Destinations

```text
master-records/core-lite -> destination-generated receipt chain
StegVerse-Labs/Site -> public release/status update after tag candidate
GCAT-BCAT-Engine/Publisher -> publication/update propagation check after tag candidate
admissibility-wiki -> governance theorem/update propagation check after tag candidate
stegguardian-wiki -> guardian/standing boundary propagation check after tag candidate
```

## Tag/Release Readiness

Current candidate after hash import closure:

```text
v0.4.0
```

Do not tag until:

```text
workflow result is observed or checked
downstream propagation verification is opened or assigned
remaining destination targets are listed
```

## Next Action

Begin `v0.5.0` destination-generated receipt chain fixture, or hand off to mirror/publisher verification using `docs/propagation_verification_task_v0_3_0.md` and the v0.4.0 snapshot.

## Archive Note

This handoff is intended to make the complete thread archivable. Future sessions should continue from this file rather than relying on full chat history.
