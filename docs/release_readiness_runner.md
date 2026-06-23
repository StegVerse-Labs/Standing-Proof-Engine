# Release Readiness Runner Binding

Status: active runner addendum
Scope: local SPE release-readiness report generation and repo-standing integration.

## Primary command

```bash
python tools/run_repo_standing.py
```

The primary repo-standing runner includes the release-readiness writer as a checked step.

## Release-readiness command

```bash
python tools/write_release_readiness.py
```

Expected terminal output:

```text
SPE RELEASE READINESS: READY
```

Generated artifacts:

```text
reports/release_readiness.json
reports/release_readiness.md
```

## Standing boundary

This binding verifies local SPE release readiness only. It does not claim downstream propagation, external publication, or completion of external target updates.

## Manual-task posture

Manual internal release-readiness copying is not required. The runner generates machine-readable and human-readable reports under `reports/`, and the CI artifact upload includes report outputs.
