# Event Replay Binding

## Assumption

This is a local SPE fixture representing replay of the destination event result. It does not claim that the destination repository generated the replay from its own workflow.

## Done Criteria

Event replay binding is done when SPE can verify:

```text
event replay fixture exists
replay references the destination event
replay binds the destination event hash
source event verifies
observed result matches expected result
observed result matches the source event result
replay handoff flags are true
CI runs event replay verification and tests
```

## Fixture

```text
samples/event_replay_001.json
```

## Verifier

```bash
python spe/verify_event_replay.py samples/event_replay_001.json
```

Expected:

```text
SPE RESULT: PASS
```

## Verified Checks

```text
parse_event_replay
source_event_hash_binding
source_event_verifies
replay_result_binding
replay_handoff_flags
```

## Governance Meaning

The event replay fixture confirms that the destination event resolves to the expected installed state and that the replay remains bound to the destination event hash.

That creates this local route:

```text
SDK intake receipt
-> SPE route manifest
-> reconstruction pointer
-> confirmation receipt
-> destination event
-> event replay
```

## Current Limitation

This fixture proves local replay of an installed event. A stronger route should add a rejected-event companion fixture so both install and reject paths remain testable.
