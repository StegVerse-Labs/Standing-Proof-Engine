# Repository Validation

Status: validation protocol
Scope: Standing-Proof-Engine repository standing, including research additions and automated standing checks.

## 1. Validation assumption

Repository standing is not established by documentation alone. The repo has standing only when its declared artifacts, manifests, tests, and expected outcomes can be independently reconstructed by an automated route.

## 2. Done definition

The repository is validation-ready when:

1. required documentation exists;
2. required research artifacts exist;
3. required manifests are parseable;
4. declared status values are valid;
5. non-claims are present for research artifacts;
6. executable tests pass;
7. expected outputs are documented;
8. reviewer reconstruction paths are explicit;
9. a single repo-standing command runs the required research and problem-encoding checks;
10. CI runs that repo-standing command on push and pull request.

## 3. Standing levels

### PASS

Repo standing is `PASS` when all required validation gates pass and no declared artifact overclaims beyond its evidence.

### PARTIAL

Repo standing is `PARTIAL` when the repo contains useful artifacts but one or more proof, test, citation, or reconstruction paths remain incomplete.

### FAIL

Repo standing is `FAIL` when a required artifact is missing, a manifest cannot be parsed, a required test fails, or a research artifact claims more than it proves.

## 4. Required validation gates

| Gate | Check | Expected result |
|---|---|---|
| Documentation gate | Required docs exist | PASS |
| Research gate | Research report and process exist | PASS |
| Manifest gate | `research/research_manifest.json` parses as JSON | PASS |
| Status gate | Manifest statuses are `PASS`, `PARTIAL`, or `FAIL` | PASS |
| Non-claim gate | Research report and problem encodings include explicit non-claims | PASS |
| Process gate | Propagation process defines all required destinations | PASS |
| Problem-encoding gate | Problem encodings match expected-result fixtures | PASS |
| Test gate | `python tools/run_repo_standing.py` runs | PASS |

## 5. Required automated command

Run the repo-standing route:

```bash
python tools/run_repo_standing.py
```

Expected output includes:

```text
SPE REPO STANDING: PASS
SPE MATHEMATICAL CLAIM STANDING: PARTIAL
SPE FOLLOW-UP ACTIONS: []
```

Machine-readable route:

```bash
python tools/run_repo_standing.py --json
```

Expected JSON includes:

```text
"repo_standing": "PASS"
"mathematical_claim_standing": "PARTIAL"
"follow_up_actions": []
```

This means the research package, calibration problem encodings, expected-result fixtures, and unittest route are structurally valid. It does not mean any mathematical problem mapping has been proven.

## 6. Component validation commands

The automated command above runs these component checks:

```bash
python tools/validate_research_standing.py
python spe/verify_problem_encodings.py
python spe/verify_problem_encodings.py --json
python -m unittest tests.test_problem_encodings
python -m unittest discover -s tests -p 'test_*.py'
```

The repository also documents executable proof-path validation commands. These remain part of broader repo standing:

```bash
python spe/verify.py samples/pressure_demo_001.json
python spe/verify.py samples/stale_state_review_commit_001.json
python spe/verify.py samples/aegis_incident_standing_001.json
python spe/verify_manifest.py samples/manifest.json
python spe/verify_sdk_intake.py samples/sdk_intake_receipt_001.json
python spe/verify_expected_corpus.py
```

Expected standing meanings:

- `PASS`: the artifact proves its declared governance result.
- `PARTIAL`: the artifact reconstructs an outcome but contains an explicit proof gap.
- `FAIL`: the artifact does not support the claimed result.

## 7. Research validation rules

A research artifact must not be marked `PASS` for mathematical conclusion unless:

1. the source problem is cited;
2. the StegVerse mapping is formalized;
3. the invariant, reduction, obstruction, or theorem is stated exactly;
4. the proof or computation is reproducible;
5. known barriers or limitations are listed;
6. independent reconstruction instructions exist.

A research artifact may be marked `PASS` for structural repo placement while its mathematical conclusion remains `PARTIAL`.

## 8. Review checklist

A reviewer should verify:

1. Which artifact is being evaluated?
2. What does it claim?
3. What does it explicitly not claim?
4. Which source report or external references support it?
5. Which files are authoritative?
6. Which automated command validates it?
7. What expected result should occur?
8. Which remaining gaps prevent stronger mathematical standing?

## 9. Completed validation expansion

The calibration research expansion now includes:

- `research/problems/*.md` files;
- machine-readable problem declarations under `samples/problems/`;
- expected-result fixtures under `expected_results/problems/`;
- tests for transition-cell references;
- CI coverage for `python tools/run_repo_standing.py`.

## 10. Leading-dot path note

The path `github/workflows/verify.yml` is displayed without its leading dot in this document. The actual GitHub Actions path includes the leading dot.
