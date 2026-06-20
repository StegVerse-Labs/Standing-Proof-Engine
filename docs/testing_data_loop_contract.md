# Testing Data Loop Contract

Standing-Proof-Engine is a downstream standing-proof evaluation route.

Formal standing-proof artifacts reach this repository after the corrected testing data loop has produced receipt-bound artifacts.

## Required Upstream Loop

```text
User
→ StegVerse-org/StegVerse-SDK or LLM Adapter
→ StegVerse-org ingestion
→ StegGhost/entity-sandbox-runner ingestion/CGE
→ ephemeral sandbox batch
→ StegGhost/entity-sandbox-runner ingestion/CGE return validation
→ StegVerse-org ingestion
→ Standing-Proof-Engine
```

## Required Input Evidence

Standing-proof inputs preserve:

```text
sdk_or_llm_adapter_intake receipt
stegverse_org_ingestion_outbound receipt
stegghost_ingestion_cge_admission receipt
ephemeral_sandbox_batch receipt
stegghost_ingestion_cge_return_validation receipt
stegverse_org_ingestion_return receipt
master-records action receipt references
```

## Standing-Proof Responsibility

SPE checks whether a reviewed artifact still has consequence-binding standing at commit time.

It consumes receipt-bound standing artifacts and emits standing result receipts.

SDK contract reference:

```text
StegVerse-org/StegVerse-SDK/docs/TESTING_DATA_LOOP_CONTRACT.md
```

Route result schema:

```text
StegVerse-org/StegVerse-SDK/schemas/formal-testing-route-result.schema.json
```
