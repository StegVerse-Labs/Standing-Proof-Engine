# Static Diagnostic Report — 2026-06-23

Status: static diagnostic report
Scope: Standing-Proof-Engine verifier chain, GitHub Actions workflow route, fixture hash bindings, source-bound stale-state sample, expected no-manual repo-standing route.

## Diagnostic method

This diagnostic inspected repository files through the GitHub connector and followed the failing GitHub Actions screenshots supplied during this run. It did not execute a live CI rerun from the assistant environment.

## Confirmed issues found and corrected

### 1. Direct-script import boundary in workflow

Symptom: `python spe/verify_manifest.py samples/manifest.json` failed with `ModuleNotFoundError: No module named 'spe'`.

Cause: direct script execution made `spe/` the script directory, so package imports like `from spe.result_export import ...` could fail.

Correction: workflow verifier calls were normalized to module execution, for example:

```bash
python -m spe.verify_manifest samples/manifest.json
```

Diagnostic status: fixed at workflow level.

### 2. Chained fixture hash drift

Symptoms occurred sequentially in confirmation, destination event, deferred destination event, installed replay, and deferred replay verifier steps.

Cause: upstream fixture content changed, but downstream stored hash fields were not synchronized with the repository canonical hashing function:

```python
json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
```

Corrections:

- `samples/master_records_confirmation_001.json` source pointer hash updated.
- `samples/destination_event_001.json` source confirmation hash updated.
- `samples/destination_event_deferred_001.json` source confirmation hash updated.
- `samples/event_replay_001.json` source event hash updated from canonical destination event hash.
- `samples/event_replay_deferred_001.json` source event hash updated from canonical deferred destination event hash.

Regression coverage added:

- `tests/test_confirmation_hash_binding.py`
- `tests/test_destination_event_hash_binding.py`
- `tests/test_event_replay_hash_binding.py`

Diagnostic status: fixed for the observed chain. Remaining recommendation: add a generator/sync tool so chained fixture hashes are derived, not hand-maintained.

### 3. Source-bound stale-state schema mismatch

Symptom: source-bound sample verifier returned `FAIL` because `commit_state` failed and formalism expectation expected `PASS`.

Cause: source-bound sample used `*_hash_ref` fields, but the generic stale-state verifier checks literal fields:

```text
authority_state_hash
policy_hash
evidence_packet_hash
```

Correction: `samples/source_hash_bound_stale_state_001.json` now includes literal hash-reference aliases in `review_time` and `commit_time` while preserving source-bound refs and DENY semantics.

Diagnostic status: fixed at fixture/schema compatibility level.

### 4. Primary runner coverage gap

Symptom: workflow-only verifier steps surfaced failures before the primary repo-standing route would necessarily catch them.

Cause: `tools/run_repo_standing.py` did not explicitly include every workflow verifier class and still used some direct `spe/*.py` script calls.

Correction: primary runner now uses a `spe_module(...)` helper for module execution and explicitly includes:

- destination event installed/deferred checks,
- event replay installed/deferred checks,
- source-bound text and JSON checks,
- external-source-ref text and JSON checks,
- destination hash import,
- destination receipt chain,
- release readiness,
- binding regression unittests,
- full unittest discovery.

Diagnostic status: fixed in primary runner.

## Remaining risks / not proven by this diagnostic

1. A live GitHub Actions rerun has not been observed after the latest fixes.
2. Expected-result fixture hashes for artifacts changed during this repair cycle may still need regeneration if a later workflow step compares stored artifact hashes rather than verifier status only.
3. Chained hash fields remain manually stored; future upstream fixture edits can create new downstream drift unless an automatic hash-sync/check tool is introduced.
4. Some repository manifest/addendum registration updates were previously blocked by connector policy; those remain documentation/registration gaps, not necessarily runtime verifier failures.

## Recommended next diagnostic command sequence

Run from repository root:

```bash
python tools/run_repo_standing.py
python tools/run_repo_standing.py --json
python tools/run_repo_standing.py --write-reports
python -m unittest discover -s tests -p 'test_*.py'
```

Then rerun the GitHub Actions `verify` workflow.

## Non-claim

This diagnostic validates structural repo-standing paths and fixture consistency. It does not prove an open mathematical problem and does not claim downstream publication or external propagation completion.
