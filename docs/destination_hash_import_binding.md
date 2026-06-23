# Destination Hash Import Binding

## Assumption

This is a local SPE fixture representing an imported destination-generated event hash. It does not claim the downstream repository has already emitted the hash from its own workflow.

## Done Criteria

Destination hash import binding is done when SPE can verify:

```text
import fixture exists
import references the destination event
import binds the local source event hash
import binds the destination event hash
source event verifies
imported event result matches expected result
hash import flags are true
formalism tests cover drift detection
```

## Fixture

```text
samples/destination_generated_event_hash_001.json
```

## Verifier

```bash
python spe/verify_hash_import.py samples/destination_generated_event_hash_001.json
```

Expected:

```text
SPE RESULT: PASS
```

## Verified Checks

```text
parse_hash_import
hash_import_route
source_event_hash_binding
destination_event_hash_binding
source_event_verifies
hash_result_binding
hash_import_flags
```

## Governance Meaning

The hash import fixture adds an explicit imported hash layer above the local destination event. SPE can now check whether the imported destination hash matches the canonical local destination event hash before treating the downstream event as bound.

That creates this route:

```text
confirmation receipt
-> destination event
-> destination event hash import
-> replayable destination state
```

## Current Limitation

The imported hash is represented locally. The next stronger route should fetch or receive the destination hash from the downstream repository receipt chain and bind it to a destination-generated receipt.
