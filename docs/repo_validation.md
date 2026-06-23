# Repository Validation

Status: validation protocol
Scope: Standing-Proof-Engine repository standing, including research additions.

## 1. Validation assumption

Repository standing is not established by documentation alone. The repo has standing only when its declared artifacts, manifests, tests, and expected outcomes can be independently reconstructed.

## 2. Done definition

The repository is validation-ready when:

1. required documentation exists;
2. required research artifacts exist;
3. required manifests are parseable;
4. declared status values are valid;
5. non-claims are present for research artifacts;
6. executable tests pass;
7. expected outputs are documented;
8. reviewer reconstruction paths are explicit.

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
| Non-claim gate | Research report includes explicit non-claims | PASS |
| Process gate | Propagation process defines all required destinations | PASS |
| Test gate | Research-standing validator runs | PASS |

## 5. Required commands

Run the research standing validator:

```bash
python tools/validate_research_standing.py
```

Expected output:

```text
SPE RESEARCH STANDING: PASS
```

This means the research package itself is structurally valid. It does not mean every mathematical problem mapping has been proven.

## 6. Existing SPE validation commands

The repository already documents executable proof-path validation commands. These remain part of broader repo standing.

```bash
python spe/verify.py samples/pressure_demo_001.json
python spe/verify.py samples/stale_state_review_commit_001.json
python spe/verify.py samples/aegis_incident_standing_001.json
python spe/verify_manifest.py samples/manifest.json
python spe/verify_sdk_intake.py samples/sdk_intake_receipt_001.json
python spe/verify_expected_corpus.py
```

Expected standing meanings:

- `PASS`: the artifact proves its governance result.
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
6. Which commands validate it?
7. What expected result should occur?
8. Which remaining gaps prevent stronger standing?

## 9. Required next validation expansion

When problem-specific encodings are added, the repo should add:

- `research/problems/*.md` files;
- optional machine-readable problem declarations;
- tests for transition-cell references;
- expected-result fixtures;
- CI coverage for `python tools/validate_research_standing.py`.

## 10. Leading-dot path note

The path `github/workflows/verify.yml` is displayed without its leading dot in this document. The actual GitHub Actions path must include the leading dot.
