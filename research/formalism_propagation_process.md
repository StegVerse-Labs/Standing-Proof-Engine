# Formalism Propagation Process

Status: research process
Placement: `research/`
Purpose: ensure completed StegVerse Formalisms are added to every repo location needed for research, validation, testing, and review.

## 1. Assumptions

A completed formalism is not complete merely because it is described in prose.

A completed formalism must include:

1. a human-readable definition;
2. a machine-readable declaration or manifest entry;
3. a research placement;
4. a validation placement;
5. a testing placement;
6. an independent reconstruction path;
7. a standing result.

## 2. Done definition

A formalism is done when all required locations below are present and pass repo-standing validation.

| Location | Required content | Standing purpose |
|---|---|---|
| `research/` | source research report, formalism notes, candidate mappings | human-readable research continuity |
| `research/research_manifest.json` | machine-readable inventory of research artifacts | manifest reconstruction |
| `docs/repo_validation.md` | validation standard and standing gates | reviewer-facing validation |
| `docs/testing_protocols.md` | exact test protocols and expected outcomes | repeatable testing |
| `tools/validate_research_standing.py` | executable repository-standing validator | local and CI-verifiable checks |
| `tests/` | unit or fixture tests when executable logic exists | proof-path enforcement |
| `expected_results/` | expected outputs for executable formalism artifacts | drift detection |
| `samples/` | sample inputs, fixtures, traces, or problem encodings | reproducible examples |

## 3. Propagation sequence

Every completed formalism must move through this sequence:

```text
Research intake
→ formalism declaration
→ manifest registration
→ sample or problem encoding
→ expected result declaration
→ validator coverage
→ documentation update
→ reviewer reconstruction path
→ standing result
```

## 4. Required formalism metadata

Each formalism must declare:

```json
{
  "formalism_id": "string",
  "title": "string",
  "status": "draft|candidate|validated|deprecated",
  "source_report": "string",
  "research_files": ["path"],
  "sample_files": ["path"],
  "expected_result_files": ["path"],
  "validator_files": ["path"],
  "standing_status": "PASS|PARTIAL|FAIL",
  "non_claims": ["string"]
}
```

## 5. Standing rules

### PASS

A formalism may be marked `PASS` only when:

- all declared files exist;
- the manifest can be read;
- test commands run successfully;
- expected outputs match actual outputs;
- a reviewer can reconstruct the claim without hidden context.

### PARTIAL

A formalism must be marked `PARTIAL` when:

- the mapping is useful but not independently complete;
- a source report is cited but formal artifacts are missing;
- a candidate invariant is described but not executable;
- a proof path depends on narrative inference.

### FAIL

A formalism must be marked `FAIL` when:

- declared files are missing;
- tests fail;
- expected outcomes drift;
- the artifact claims more than it proves;
- the mapping cannot be reconstructed.

## 6. Required process for adding a completed formalism

1. Add or update the human-readable research file in `research/`.
2. Add any problem encoding under `research/problems/` or `samples/`.
3. Add expected outcomes under `expected_results/` when executable verification exists.
4. Register the artifact in `research/research_manifest.json`.
5. Update `docs/repo_validation.md` if the formalism introduces a new standing gate.
6. Update `docs/testing_protocols.md` if the formalism introduces a new command or expected outcome.
7. Update or extend `tools/validate_research_standing.py`.
8. Run validation locally.
9. Record the result as `PASS`, `PARTIAL`, or `FAIL`.

## 7. Required process for revising a completed formalism

A revision must not silently replace standing context.

Revision steps:

1. preserve the prior formalism ID;
2. add a new version or revision field;
3. document what changed;
4. document whether prior samples still apply;
5. rerun validation;
6. mark superseded artifacts explicitly if needed.

## 8. Required process for deprecating a formalism

A deprecated formalism must remain reconstructable unless it contains sensitive or invalid content requiring removal.

Deprecation steps:

1. mark `status: deprecated` in the manifest;
2. state the replacement, if any;
3. preserve prior citations;
4. preserve expected-result history;
5. ensure validators do not treat deprecated artifacts as active requirements unless explicitly configured.

## 9. Research-specific non-claim rule

Every research formalism must include a non-claims section.

Minimum non-claims:

```text
This artifact does not claim to solve the underlying open problem.
This artifact does not claim that a mapping is a proof.
This artifact does not claim general validity beyond the declared artifacts.
```

## 10. Review handoff

A reviewer handoff is complete when the reviewer can answer:

1. What is being claimed?
2. What is not being claimed?
3. Which source report or external references support the mapping?
4. Which files are authoritative?
5. Which tests verify repo standing?
6. What result should be expected?
7. Which gaps remain?

## 11. CI recommendation

The repo should run the research-standing validator in CI after this process is adopted:

```bash
python tools/validate_research_standing.py
```

If CI cannot run yet, the command remains the local standing check.
