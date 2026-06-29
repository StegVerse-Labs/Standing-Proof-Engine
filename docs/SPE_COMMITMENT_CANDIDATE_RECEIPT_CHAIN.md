# SPE Commitment Candidate Receipt Chain

## Assumptions

1. `Admissible-Existence/TT` remains the canonical source for transition semantics.
2. SPE consumes TT transition ids, code references, fixture references, and receipt schema references before standing reconstruction.
3. Commitment Candidates remain non-authorizing even when a TT transition resolves.
4. Workflow paths displayed here without a leading period are iOS-safe display paths. Canonical workflow paths begin with a leading period.

## Done Definition

This step is done when every generated Commitment Candidate test carries a TT transition id, TT code reference, TT transition resolution receipt, standing result, and final standing receipt in one verifiable chain.

## Added Files

```text
samples/commitment_candidate_receipt_chain_expectation.json
spe/verify_commitment_candidate_receipt_chain.py
docs/SPE_COMMITMENT_CANDIDATE_RECEIPT_CHAIN.md
```

## Receipt Chain Elements

Each generated Commitment Candidate artifact must contain:

```text
historical_review.review_id
historical_review.transition_cell_id
historical_review.tt_transition_id
commitment_candidate.candidate_id
commitment_candidate.tt_transition_id
commitment_candidate.tt_code_ref
standing_evaluation.result
receipt.receipt_id
receipt.tt_transition_id
receipt.tt_transition_receipt
receipt.decision
```

The nested TT transition receipt must contain:

```text
receipt_type
canonical_source
transition_id
transition_name
code_ref
implementation_status
fixture_ref
receipt_schema_ref
required_field
resolved
decision
reason
```

## Verification

```bash
python spe/verify_commitment_candidate_receipt_chain.py samples/commitment_candidate_receipt_chain_expectation.json
```

Expected:

```text
spe_commitment_candidate_receipt_chain_result: PASS
```

## Workflow

```text
github/workflows/spe-tt-binding.yml
```

The canonical repository path begins with a leading period.

The workflow now validates:

```text
TT consequence/reconstruction coverage
TT support-family coverage
runtime support-transition cases
Commitment Candidate TT receipt chain
TT-bound Commitment Candidate manifest
SPE manifest route
```

## Boundary

Receipt-chain integration does not grant commit-time permission, does not make a Commitment Candidate authorizing, does not replace standing reconstruction, and does not move TT source authority into SPE.
