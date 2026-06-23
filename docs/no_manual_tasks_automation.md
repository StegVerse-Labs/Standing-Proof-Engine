# No Manual Tasks Automation

## Assumption

This document records the current automation path for eliminating manual verifier selection inside `Standing-Proof-Engine`. It does not claim that downstream repositories have already imported or mirrored the outputs.

## Done Criteria

Manual task reduction is complete for this pass when one command covers the active SPE structural checks:

```text
python tools/run_repo_standing.py
```

and one JSON command covers the same checks for machine ingestion:

```text
python tools/run_repo_standing.py --json
```

## Automated Coverage

The repo-standing runner now includes:

```text
research standing
problem encodings
problem encoding JSON export
automation addendum
automation addendum JSON export
installed destination event binding
deferred destination event binding
installed event replay binding
deferred event replay binding
destination hash import binding
problem encoding tests
event expected-result tests
hash import tests
all formalism tests
```

## Governance Meaning

Reviewers, CI, and downstream agents do not need to remember separate commands for the destination event/replay/hash-import path. They can run the repo-standing route and receive one PASS/FAIL result.

## Remaining Non-Automated Work

```text
Downstream Site/Publisher/wiki propagation still requires connector-side updates.
Destination-generated receipt chain still requires downstream source artifacts.
GitHub release tagging still requires an explicit release action or supported connector path.
```

## Next Automation Candidate

Add a generated handoff status report that writes current repo-standing output into `reports/repo_standing.json` and `reports/repo_standing.md` during CI.
