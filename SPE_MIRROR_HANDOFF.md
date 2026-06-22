# SPE Mirror Handoff

## Assumption

This file is the current handoff and task source of truth for `StegVerse-Labs/Standing-Proof-Engine`. It must be checked before continuing mirror, release, publication, or cross-repo update work.

## Done Criteria

The current build pass is done when the active confirmation binding goal has:

```text
confirmation fixture
confirmation verifier
expected-result fixture
expected-corpus report support
machine-readable JSON export
CI coverage
activation closure
release snapshot update
mirror/publication verification task
```

## Active Repo

```text
Org: StegVerse-Labs
Repo: Standing-Proof-Engine
Active Goal: master-records confirmation receipt binding
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
```

Still required for the active goal:

```text
confirmation activation closure
release snapshot update for confirmation binding
README or README addendum update for confirmation route
master-records destination event hash fixture
install-or-reject replay path
```

## Known Files Added for Confirmation Goal

```text
samples/master_records_confirmation_001.json
spe/verify_confirmation.py
spe/verify_confirmation_json.py
expected_results/confirmation_001.expected.json
docs/confirmation_binding.md
tests/test_confirmation.py
tests/test_confirmation_json_export.py
```

## Known Downstream Destinations

```text
master-records/core-lite -> confirmation receipt chain, destination event hash, install/reject replay
StegVerse-Labs/Site -> public release/status update after tag candidate
GCAT-BCAT-Engine/Publisher -> publication/update propagation check after tag candidate
admissibility-wiki -> governance theorem/update propagation check after tag candidate
stegguardian-wiki -> guardian/standing boundary propagation check after tag candidate
```

## Tag/Release Readiness

Current candidate after confirmation activation closure:

```text
v0.2.0
```

Do not tag until:

```text
confirmation activation closure exists
release snapshot is updated
mirror/publication verification task is created
remaining destination targets are listed
```

## Next Action

Create `docs/confirmation_activation_closure.md`, then update release/mirror status artifacts.

## Archive Note

This handoff is intended to make the complete thread archivable once the active goal is closed. Future sessions should continue from this file rather than relying on full chat history.
