# CI Rerun Trigger

This file intentionally records a no-op CI rerun trigger after adding expected-corpus JSON diagnostics and fixture-path listing to the recovery branch.

Purpose:

- force a fresh PR validation run on the current recovery head;
- confirm `python -m spe.verify_expected_corpus --json` exposes hidden corpus fixture failures;
- preserve the change as a visible recovery-branch event rather than mutating runtime logic.
