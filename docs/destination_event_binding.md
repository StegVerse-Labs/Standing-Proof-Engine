# Destination Event Binding

## Assumption

This is a local SPE fixture representing a destination event after confirmation receipt binding. It does not claim that `master-records/core-lite` generated the event from its own workflow.

## Done Criteria

Destination event binding is done when SPE can verify:

```text
destination event fixture exists
event references the confirmation receipt
event binds the confirmation receipt hash
source confirmation verifies
event result is installed
event hash is declared
event target matches confirmation target
CI runs destination event verification and tests
```

## Fixture

```text
samples/destination_event_001.json
```

## Verifier

```bash
python spe/verify_destination_event.py samples/destination_event_001.json
```

Expected:

```text
SPE RESULT: PASS
```

## Verified Checks

```text
parse_destination_event
destination_event_route
source_confirmation_hash_binding
source_confirmation_verifies
destination_event_result_binding
destination_event_target_binding
```

## Governance Meaning

The destination event fixture records that the confirmation receipt has moved into an installed destination-event state. This creates a stronger local chain than confirmation alone:

```text
SDK intake receipt
-> SPE route manifest
-> reconstruction pointer
-> confirmation receipt
-> destination event
```

## Current Limitation

This is still a local fixture. The next stronger version should add install-or-reject replay evidence and a destination-generated event hash from the actual downstream repository.
