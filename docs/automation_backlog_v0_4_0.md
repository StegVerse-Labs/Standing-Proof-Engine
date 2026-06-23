# Automation Backlog v0.4.0

## Objective

Remove remaining manual operational steps.

## Automated

```text
repo standing execution
expected-result verification
destination event verification
event replay verification
destination hash import verification
formalism test execution
```

## Remaining Manual Dependencies

```text
GitHub release tagging
cross-repo propagation updates
Site publication updates
Publisher publication updates
wiki synchronization
external downstream receipt acquisition
```

## Next Automation Candidates

Priority order:

```text
1. auto-generate reports/repo_standing.json
2. auto-generate reports/repo_standing.md
3. auto-generate release readiness report
4. auto-generate propagation task status report
5. auto-open downstream update bundles
```

## Stop Condition

Manual actions remain only where external repositories or external governance decisions are required.
