# MR Chain Check

## Assumption

This document records SPE-side verification preparation for the mapped chain from `master-records/core-lite`. The SPE fixture is a copied payload candidate, not a live fetch.

## Done Criteria

```text
mapped chain fixture present
expected fixture present
verification command recorded
boundary recorded
next target recorded
```

## Fixture

```text
samples/external_master_records_receipt_chain_001.json
```

## Expected Fixture

```text
expected_results/external_master_records_receipt_chain_001.expected.json
```

## Verification Command

```bash
python -m spe.verify_expected_result expected_results/external_master_records_receipt_chain_001.expected.json
```

## Expected Result

```text
SPE RESULT: PASS
governance result: CHAIN_BOUND
```

## Boundary

This checks the mapped payload shape inside SPE. Future live emissions must be imported and checked again.

## Next Target

```text
StegVerse-Labs/Site -> publish receipt-chain propagation status after workflow observation
```
