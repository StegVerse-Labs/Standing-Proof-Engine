# Decision Vocabulary

Canonical governance decision values:

```text
ALLOW
DENY
CONDITIONAL
FAIL_CLOSED
```

Meanings:

- `ALLOW`: current commit-time standing is sufficient.
- `DENY`: current commit-time standing was checked and is not sufficient.
- `CONDITIONAL`: named conditions must be satisfied before another standing check.
- `FAIL_CLOSED`: current standing cannot be safely reconstructed from the available authority, policy, delegation, evidence, context, validity, or recoverability state.

Compatibility:

- `DEFER` is deprecated. Map condition-pending cases to `CONDITIONAL`; map unsafe or indeterminate cases to `FAIL_CLOSED`.
- `FAIL-CLOSED` is deprecated as a spelling. Use `FAIL_CLOSED`.

SPE proof-status values such as `PASS`, `PARTIAL`, and `FAIL` remain separate from governance decision values.
