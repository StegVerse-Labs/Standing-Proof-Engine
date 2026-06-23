# Event Replay Binding

## Assumption

This is a local SPE fixture representing replay of destination event results. It does not claim that the destination repository generated the replay from its own workflow.

## Done Criteria

Event replay binding is done when SPE can verify:

```text
event replay fixtures exist
replay references the destination event
replay binds the destination event hash
source event verifies
observed result matches expected result
observed result matches the source event result
replay handoff flags are true
CI runs both replay verifications and tests
```

## Fixtures

```text
samples/event_replay_001.json
samples/event_replay_deferred_001.json
```

## Verifier

```bash
python spe/verify_event_replay.py samples/event_replay_001.json
python spe/verify_event_replay.py samples/event_replay_deferred_001.json
```

Expected:

```text
SPE RESULT: PASS
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

The event replay fixtures confirm that destination events resolve to their expected final states and that replay remains bound to destination event hashes.

That creates this local route:

```text
SDK intake receipt
-> SPE route manifest
-> reconstruction pointer
-> confirmation receipt
-> destination event
-> event replay
```

## Covered Outcomes

```text
INSTALLED
NOT_INSTALLED
```

## Current Limitation

These fixtures prove local replay of accepted and deferred destination event states. A stronger route should add destination-generated event hashes from the downstream repository.
