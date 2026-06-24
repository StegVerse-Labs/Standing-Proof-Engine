# Ecosystem Sandbox Validation Request — 2026-06-23

Status: validation request
Runner: GitHub Actions `verify` workflow
Purpose: force the ecosystem runner to execute the repository validation route from a fresh checkout after expected-corpus and verifier-route repairs.

## Required validation route

The push that creates this file should trigger `.github/workflows/verify.yml`.

The workflow should execute, at minimum:

```bash
python -m spe.verify_expected_corpus
python tools/run_repo_standing.py
python tools/run_repo_standing.py --json
python tools/run_repo_standing.py --write-reports
python -m unittest discover -s tests -p 'test_*.py'
```

## Specific previously failing area

The prior observed failure was in the expected corpus verifier, specifically around expected fixtures for:

- `event_replay_001.expected.json`
- `event_replay_deferred_001.expected.json`
- `hash_import_001.expected.json`
- `receipt_chain_001.expected.json`

The expected corpus verifier has been updated to route destination-event, event-replay, hash-import, and receipt-chain fixtures through their native verifiers before this validation request.

## Pass condition

The ecosystem validation run should be treated as complete only when the GitHub Actions `verify` workflow completes successfully from the fresh checkout produced by this commit.

## Non-claim

This validation request proves only repository execution standing for the declared validation path. It does not prove any open mathematical claim and does not claim downstream external publication or propagation.
