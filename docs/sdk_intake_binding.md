# SDK Intake Binding

## Assumption

This binding is represented inside `Standing-Proof-Engine` as a local fixture. It does not claim that `StegVerse-org/StegVerse-SDK` has already emitted the receipt from its own repository workflow.

## Done Criteria

SDK intake binding is done when SPE can verify:

```text
SDK-origin receipt exists
receipt declares Standing-Proof-Engine route
receipt identifies the SPE route package manifest
receipt binds the declared sample count to the manifest
receipt expects the manifest package status
SPE verifies the manifest result against the receipt expectation
```

## Fixture

```text
samples/sdk_intake_receipt_001.json
```

The fixture declares:

```text
origin_repo: StegVerse-org/StegVerse-SDK
destination_repo: StegVerse-Labs/Standing-Proof-Engine
route: standing_proof_engine
artifact_package: samples/manifest.json
expected_package_status: PARTIAL
```

## Verifier

```bash
python spe/verify_sdk_intake.py samples/sdk_intake_receipt_001.json
```

Expected:

```text
SPE RESULT: PASS
```

## Verified Checks

```text
parse_sdk_intake
route_declaration
handoff_flags
manifest_result_binding
sample_count_binding
```

## Governance Meaning

The SDK intake receipt does not prove the standing theorem by itself. It proves that an upstream intake layer can declare a route package for SPE and that SPE can check whether the declared package result matches the intake expectation.

That creates this route:

```text
SDK intake receipt
-> route declaration
-> SPE manifest package
-> SPE route verification
-> expected package status binding
```

## Current Limitation

This is a local SPE fixture. The next stronger version should add a corresponding SDK-side generated receipt and a stable hash relationship between the SDK receipt and SPE manifest.
