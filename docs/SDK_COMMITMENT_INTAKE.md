# SPE SDK Commitment Intake

## Purpose

This contract accepts a deterministic, transport-neutral Commitment Candidate envelope emitted by `StegVerse-org/StegVerse-SDK` and binds an SPE standing result to the candidate and envelope hashes.

## Intake Validation

The SPE consumer requires:

```text
schema_version = stegverse.sdk.spe_commitment_intake.v0.1
destination_repo = StegVerse-Labs/Standing-Proof-Engine
route_purpose = FRESH_STANDING_DETERMINATION
receipt_required = true
expected_result = [ALLOW, DENY, FAIL_CLOSED]
```

The embedded candidate must remain non-authorizing and require a fresh standing determination.

## Integrity Checks

SPE independently reconstructs and validates:

```text
candidate_hash
envelope_hash
package_id
transition_id
run_id
```

Any mismatch fails closed before a standing result receipt can be emitted.

## Standing Receipt

`emit_spe_standing_receipt(...)` binds the supplied SPE result to:

```text
package_id
transition_id
run_id
candidate_hash
envelope_hash
policy_refs
delegation_refs
evidence_refs
reasons
```

The receipt explicitly states:

```text
execution_authorized = false
execution_performed = false
master_record_installed = false
```

An `ALLOW` result advances only to the next governed execution-authority boundary. It does not execute the action.

## Verification

```bash
python -m unittest tests.test_sdk_commitment_intake
```

No new workflow is required. The test belongs in the repository's existing verification and sandbox surfaces.

## Boundary

```text
SDK construction is not SPE standing.
SPE standing is not execution authority.
ALLOW is not execution.
A receipt is not Master-Records installation.
Hash agreement is necessary but not sufficient for admissibility.
```
