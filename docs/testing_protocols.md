# Testing Protocols

Status: testing protocol
Scope: Standing-Proof-Engine verification, research-standing validation, and formalism propagation checks.

## 1. Testing assumption

A test passing means only that the declared artifact satisfies the tested standing condition. A passing structural research test does not prove an open mathematical problem.

## 2. Done definition

Testing is done when:

1. every declared command can be run from the repository root;
2. every command has an expected result;
3. failures are treated as standing failures;
4. research artifacts are validated structurally before any mathematical claim is elevated;
5. all new completed formalisms are registered in `research/research_manifest.json`.

## 3. Research-standing test

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
- testing and validation documents exist.

## 4. Existing SPE proof-path tests

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

## 5. Research formalism test expansion

When a completed mathematical formalism is added, it must include one or more of the following test types:

| Test type | Required when | Example |
|---|---|---|
| Presence test | formalism is documentation-only | file exists and is manifest-registered |
| Schema test | formalism has machine-readable declaration | JSON parses and required fields exist |
| Encoding test | problem encoding exists | encoding references declared transition cells |
| Expected-result test | executable verifier exists | actual output equals expected output |
| Reconstruction test | candidate theorem, invariant, reduction, or obstruction exists | reviewer can reproduce the artifact result |

## 6. Failure handling

If a test fails:

1. do not mark the artifact `PASS`;
2. identify whether the failure is missing file, malformed manifest, status drift, expected-result drift, or overclaim;
3. update the artifact or downgrade standing;
4. rerun the validator.

## 7. Candidate solution test rule

Any candidate solution to an open problem must pass at least the following before it can be elevated beyond `PARTIAL`:

1. problem statement cited;
2. formal mapping declared;
3. exact claim stated;
4. known barriers reviewed;
5. proof or computation reproducible;
6. independent reviewer instructions included;
7. negative/failure modes logged.

## 8. CI recommendation

Add the research validator to CI when the workflow is next updated:

```bash
python tools/validate_research_standing.py
```

Leading-dot path note: `github/workflows/verify.yml` is displayed without the leading dot. The actual workflow path must include the leading dot.

## 9. Test interpretation

`PASS` means the artifact proves or satisfies the declared tested condition.

`PARTIAL` means the artifact is useful and reconstructable in part, but one or more proof or standing gaps remain.

`FAIL` means the artifact does not support the declared condition.
