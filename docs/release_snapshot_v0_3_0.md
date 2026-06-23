# Standing-Proof-Engine Release Snapshot v0.3.0

## Assumption

This is a documentation snapshot, not a GitHub release tag. It records the SPE package after local destination event and dual replay coverage.

## Done Criteria

This snapshot is complete when it records:

```text
scope
included routes
verification commands
expected results
CI coverage
known local-fixture limitations
next integration targets
propagation verification targets
```

## Scope

Version `v0.3.0` captures the SPE reviewer handoff package after destination event binding, accepted replay, and deferred replay coverage.

The release theorem remains:

```text
Detection does not imply authority.
Review does not imply standing.
Replayability does not imply admissibility.
Consequence requires commit-time standing.
```

The integration theorem extended by this snapshot is:

```text
Destination events must bind to confirmation receipt hashes.
Replay artifacts must bind to destination event hashes.
Final states must be replayable as declared outcomes, including installed and not-installed paths.
```

## Included Routes

```text
1. pressure receipt drift denial
2. stale-state review-to-commit denial
3. Aegis incident detection-to-standing denial
4. SDK intake receipt binding
5. reconstruction pointer binding
6. local confirmation receipt binding
7. destination event binding
8. accepted event replay
9. deferred event replay
```

## Included Event Artifacts

```text
samples/destination_event_001.json
samples/destination_event_deferred_001.json
samples/event_replay_001.json
samples/event_replay_deferred_001.json
expected_results/destination_event_001.expected.json
expected_results/destination_event_deferred_001.expected.json
expected_results/event_replay_001.expected.json
expected_results/event_replay_deferred_001.expected.json
docs/destination_event_binding.md
docs/event_replay_binding.md
docs/destination_event_activation_closure.md
```

## Verification Commands

```bash
python spe/verify_destination_event.py samples/destination_event_001.json
python spe/verify_destination_event.py samples/destination_event_deferred_001.json
python spe/verify_event_replay.py samples/event_replay_001.json
python spe/verify_event_replay.py samples/event_replay_deferred_001.json
python -m unittest discover -s tests -p 'test_*.py'
```

## Expected Results

```text
destination_event_001 -> PASS / INSTALLED
destination_event_deferred_001 -> PASS / NOT_INSTALLED
event_replay_001 -> PASS / INSTALLED
event_replay_deferred_001 -> PASS / NOT_INSTALLED
formalism tests -> PASS
```

## CI Coverage

The workflow path is displayed here without the leading dot:

```text
github/workflows/verify.yml
```

Note: the actual repository path includes the leading dot.

The workflow verifies destination event binding and both accepted and deferred replay paths.

## Known Limitations

```text
Destination event fixtures are local SPE fixtures.
Replay fixtures are local SPE fixtures.
Destination-generated event hashes are not yet imported from the downstream repository.
Expected-result verifier integration for event fixtures is represented by formalism tests, not the shared expected-result CLI.
Site, Publisher, admissibility wiki, and StegGuardian wiki propagation are not yet verified for v0.3.0.
```

## Propagation Verification Targets

```text
StegVerse-Labs/Site
GCAT-BCAT-Engine/Publisher
admissibility-wiki
stegguardian-wiki
```

## Release Status

```text
Snapshot: v0.3.0
Activation package: READY FOR LOCAL REVIEWER HANDOFF
Full repo completion: NOT COMPLETE
Destination event binding: PRESENT
Accepted replay path: PRESENT
Deferred replay path: PRESENT
Release tag: NOT CREATED
Propagation verification task: REQUIRED
```

## Next Integration Targets

```text
v0.4.0 -> destination-generated event hash import
v0.5.0 -> shared expected-result CLI support for event fixtures
v0.6.0 -> destination-generated master-records receipt chain
v0.7.0 -> propagation verification across Site, Publisher, admissibility wiki, and StegGuardian wiki
```
