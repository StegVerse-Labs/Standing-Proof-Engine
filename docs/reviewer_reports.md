# Reviewer Reports

Standing-Proof-Engine can generate Markdown reports for reviewers.

## Report Generator

```bash
python spe/report.py <artifact.json> <output.md> [default|source_bound|external_refs]
```

Examples:

```bash
python spe/report.py samples/pressure_demo_001.json reports/pressure_demo_001.md default
python spe/report.py samples/external_source_ref_stale_state_001.json reports/external_source_ref_stale_state_001.md external_refs
```

## Report Contents

Each report includes:

- artifact path;
- selected verifier;
- SPE result;
- canonical artifact SHA-256;
- ordered check table;
- plain-language interpretation.

## CI Artifact

The GitHub Actions workflow generates reports for the main proof paths and uploads them as:

```text
spe-reviewer-reports
```

Note: the workflow path is displayed here without the leading dot as `github/workflows/verify.yml`; the actual repository path includes the leading dot.

## Why Reports Matter

Raw JSON is useful for machines.

Markdown reports are useful for reviewers.

The report layer lets an outside reviewer inspect:

```text
artifact -> verifier -> result -> check table -> interpretation
```

without needing to read the verifier source code first.

## Current Report Set

The workflow currently generates reports for:

1. pressure receipt partial proof;
2. stale-state proof path;
3. source-hash-bound proof path;
4. external source-reference proof path.

Future report sets should include negative corpus reports and cross-repository manifest reports.
