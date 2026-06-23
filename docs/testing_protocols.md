# Testing Protocols

Status: testing protocol
Scope: Standing-Proof-Engine verification, automated repo-standing validation, problem-encoding verification, automation-addendum validation, machine-handoff validation, and formalism propagation checks.

## 1. Testing assumption

A test passing means only that the declared artifact satisfies the tested standing condition. A passing structural research test does not prove an open mathematical problem.

## 2. Done definition

Testing is done when:

1. every declared command can be run from the repository root;
2. every command has an expected result;
3. failures are treated as standing failures;
4. research artifacts are validated structurally before any mathematical claim is elevated;
5. all new completed formalisms are registered in `research/research_manifest.json` or a linked addendum artifact;
6. problem encodings are checked against expected-result fixtures;
7. automation addendum metadata is checked by the repo-standing route;
8. machine handoff metadata is checked by the repo-standing route;
9. CI runs the automated repo-standing route;
10. the repo-standing JSON export declares no follow-up actions;
11. repo-standing report artifacts can be generated without manual copying.

## 3. Automated repo-standing route

Command:

```bash
python tools/run_repo_standing.py
```

Expected result includes:

```text
SPE REPO STANDING: PASS
SPE MATHEMATICAL CLAIM STANDING: PARTIAL
SPE FOLLOW-UP ACTIONS: []
```

Machine-readable command:

```bash
python tools/run_repo_standing.py --json
```

Expected JSON includes:

```text
"repo_standing": "PASS"
"mathematical_claim_standing": "PARTIAL"
"follow_up_actions": []
```

Report-writing command:

```bash
python tools/run_repo_standing.py --write-reports
```

Expected generated artifacts:

```text
reports/repo_standing.json
reports/repo_standing.md
```

This is the preferred route for CI, downstream agents, and reviewers because it runs the component checks in the required order and can emit reusable artifacts.

## 4. Automation addendum metadata check

Command:

```bash
python tools/check_automation_addendum.py
```

Expected result:

```text
SPE AUTOMATION ADDENDUM: PASS
```

Machine-readable command:

```bash
python tools/check_automation_addendum.py --json
```

Expected JSON includes:

```text
"automation_addendum": "PASS"
"failures": []
```

Unittest metadata mirror:

```bash
python -m unittest tests.test_automation_addendum_metadata
```

This validates that the addendum points to the repo-standing runner, the CI workflow display path, required workflow commands, and component checks.

## 5. Machine handoff metadata check

Command:

```bash
python -m unittest tests.test_repo_standing_handoff_metadata
```

Expected result:

```text
OK
```

This validates that `reports/repo_standing_handoff.json` records the expected repo-standing commands, expected standing values, empty pending actions, and existing referenced artifacts.

## 6. Research-standing test

Command:

```bash
python tools/validate_research_standing.py
```

Expected result:

```text
SPE RESEARCH STANDING: PASS
```

This validates:

- required files exist;
- manifest JSON parses;
- manifest statuses are valid;
- research report includes non-claims;
- propagation process references required destinations;
- problem docs include required sections;
- machine-readable encodings include transition IDs, rules, cell references, invariant candidates, and non-claims;
- testing and validation documents exist.

## 7. Problem-encoding verification

Command:

```bash
python spe/verify_problem_encodings.py
```

Expected result:

```text
SPE PROBLEM ENCODINGS: PASS
```

Machine-readable command:

```bash
python spe/verify_problem_encodings.py --json
```

Expected JSON includes:

```text
"spe_result": "PASS"
"mathematical_standing": "PARTIAL"
"verified_problem_count": 3
```

This verifies that calibration encodings match expected-result fixtures. It does not prove Collatz, Jacobian, Caccetta-Haggkvist, or any other open problem.

## 8. Existing SPE proof-path tests

Run the pressure-receipt trace:

```bash
python spe/verify.py samples/pressure_demo_001.json
```

Expected result:

```text
SPE RESULT: PARTIAL
```

Run the stale-state proof path:

```bash
python spe/verify.py samples/stale_state_review_commit_001.json
```

Expected result:

```text
SPE RESULT: PASS
```

Run the Aegis incident standing proof:

```bash
python spe/verify.py samples/aegis_incident_standing_001.json
```

Expected result:

```text
SPE RESULT: PASS
```

Run the route package manifest:

```bash
python spe/verify_manifest.py samples/manifest.json
```

Expected result includes:

```text
"spe_result": "PARTIAL"
```

Run the SDK intake binding verifier:

```bash
python spe/verify_sdk_intake.py samples/sdk_intake_receipt_001.json
```

Expected result:

```text
SPE RESULT: PASS
```

Run the expected-result corpus:

```bash
python spe/verify_expected_corpus.py
```

Expected result:

```text
SPE RESULT: PASS
```

## 9. Research formalism test expansion

When a completed mathematical formalism is added, it must include one or more of the following test types:

| Test type | Required when | Example |
|---|---|---|
| Presence test | formalism is documentation-only | file exists and is manifest-registered |
| Schema test | formalism has machine-readable declaration | JSON parses and required fields exist |
| Encoding test | problem encoding exists | encoding references declared transition cells |
| Expected-result test | executable verifier exists | actual output equals expected output |
| Reconstruction test | candidate theorem, invariant, reduction, or obstruction exists | reviewer can reproduce the artifact result |

## 10. Failure handling

If a test fails:

1. do not mark the artifact `PASS`;
2. identify whether the failure is missing file, malformed manifest, status drift, expected-result drift, missing transition-cell reference, or overclaim;
3. update the artifact or downgrade standing;
4. rerun `python tools/run_repo_standing.py`.

## 11. Candidate solution test rule

Any candidate solution to an open problem must pass at least the following before it can be elevated beyond `PARTIAL`:

1. problem statement cited;
2. formal mapping declared;
3. exact claim stated;
4. known barriers reviewed;
5. proof or computation reproducible;
6. independent reviewer instructions included;
7. negative/failure modes logged.

## 12. CI route

The CI route now includes:

```bash
python tools/run_repo_standing.py
python tools/run_repo_standing.py --json
python tools/run_repo_standing.py --write-reports
python -m unittest discover -s tests -p 'test_*.py'
```

The repo-standing command itself includes:

```bash
python tools/check_automation_addendum.py
python tools/check_automation_addendum.py --json
python -m unittest tests.test_automation_addendum_metadata
python -m unittest tests.test_repo_standing_handoff_metadata
```

Leading-dot path note: `github/workflows/verify.yml` is displayed without the leading dot. The actual workflow path includes the leading dot.

## 13. Test interpretation

`PASS` means the artifact proves or satisfies the declared tested condition.

`PARTIAL` means the artifact is useful and reconstructable in part, but one or more proof or standing gaps remain.

`FAIL` means the artifact does not support the declared condition.
