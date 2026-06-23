# StegVerse Formalisms as a Research Program for Unsolved Mathematics

Status: research intake report
Placement: `research/`
Primary source report: Deep Research report generated in this conversation, titled `StegVerse Formalisms as a Research Program for Unsolved Mathematics`.
Repo standing relation: this report extends the Standing-Proof-Engine research surface. It does not change executable standing logic by itself.

## 0. Assumptions

This report assumes that StegVerse Formalisms are a stack of transition-governance languages rather than a single closed theorem system. The working layers are:

1. compositional and categorical structure;
2. graph, hypergraph, and sheaf structure;
3. algebraic, cohomological, and operator-theoretic invariants;
4. dynamical, periodic, and multiscale transition systems;
5. the transition periodic table as a classification surface for primitive local transformations.

This is cited from the source report, which interprets the formalisms as a compositional, structural, invariant, and dynamical stack and identifies the transition periodic table as the layer that classifies primitive local transformations by symmetry, conservation law, singularity type, reversibility, scale behavior, periodic signature, and computational hardness. [SR-1]

## 1. Research thesis

StegVerse Formalisms are most likely to provide mathematical insight where an unsolved problem already exposes:

- local transition rules;
- compositional reductions;
- graph-like or sheaf-like state spaces;
- multiscale structure;
- obstruction invariants;
- explicit standing differences between local admissibility and global consequence.

The source report states that the strongest targets are not merely the most famous open problems, but problems whose formulations already expose local transition rules, compositional reductions, graph-like state spaces, multiscale structure, and obstruction invariants. [SR-2]

## 2. Priority target list

The source report prioritizes the following first-year portfolio:

| Tier | Problem | StegVerse fit | Research posture |
|---|---|---|---|
| A | Collatz conjecture | Tiny local transition rule, huge global orbit graph, periodicity and obstruction search | calibration target |
| A | Jacobian conjecture | Polynomial composition, rooted-tree expansions, degree reduction, invertibility obstruction | calibration target |
| A | Caccetta-Haggkvist conjecture | Local outdegree rules force or fail to force short global directed cycles | calibration target |
| A | Navier-Stokes existence and smoothness | Multiscale transition complex, energy transfer, cancellation, blowup/smoothing boundary | flagship target |
| A | Yang-Mills existence and mass gap | Gauge-local composition, renormalization, spectrum, local-to-global field structure | flagship target |
| A | Smooth 4D Poincare conjecture | Trisections, handle moves, group diagrams, categorical topology bridge | geometry bridge |
| A | Riemann Hypothesis | Euler products, spectral/dynamical zeta viewpoints, positivity/search for trace-like invariants | long-horizon target |
| A | Hodge conjecture | Cohomological/categorical transition between analytic and algebraic structure | stretch geometry target |

The source report recommends Collatz, Jacobian, and Caccetta-Haggkvist as the highest-probability calibration problems for meaningful progress in twelve months, with Navier-Stokes, Yang-Mills, Riemann, and Hodge as longer-horizon flagship targets. [SR-3]

## 3. Individual research parts

### Part A: Formalism catalog

Research objective: write the public axiomatization of StegVerse Mathematical Formalisms.

Required outputs:

- formal object vocabulary;
- morphism and transition vocabulary;
- admissibility and standing predicates;
- invariant schema;
- transition periodic table schema;
- problem-encoding template.

Validation question:

```text
Can an independent reviewer reconstruct the formalism objects, transitions, and invariants without relying on narrative explanation?
```

SPE connection:

SPE already distinguishes `PASS`, `PARTIAL`, and `FAIL` based on independent reconstructability. Research formalisms should inherit that proof status vocabulary.

### Part B: Calibration problem encodings

Research objective: encode Collatz, Jacobian, and Caccetta-Haggkvist inside the same transition schema.

Required outputs:

- one problem declaration per target;
- one transition map per target;
- one known-result mapping per target;
- one obstruction/invariant candidate per target;
- one negative-result log per target.

Validation question:

```text
Does the encoding reproduce known structural facts before claiming new insight?
```

SPE connection:

A research result should be treated as `PARTIAL` unless the repo includes enough artifacts to independently reconstruct the asserted invariant, obstruction, reduction, or counterexample search.

### Part C: Flagship problem technical notes

Research objective: test whether StegVerse captures structure beyond existing descriptions for Navier-Stokes, Yang-Mills, Riemann, Hodge, and Smooth 4D Poincare.

Required outputs:

- one technical note per flagship target;
- explicit statement of what the StegVerse mapping adds;
- explicit statement of what it does not prove;
- benchmark against the source report's caution against mere reformulation.

Validation question:

```text
Does the formalism produce a new invariant, reduction, obstruction, benchmark, or falsifiable conjecture rather than only new terminology?
```

### Part D: Transition periodic table research package

Research objective: convert the existing transition periodic table idea into a reusable mathematical classification artifact.

Required outputs:

- table schema;
- transition cells;
- invariant fields;
- admissibility fields;
- standing fields;
- field-specific examples;
- tests that verify every problem encoding points to at least one transition cell.

Validation question:

```text
Can every included problem encoding be traced to declared transition cells, and can every claimed transition cell be checked against at least one example?
```

### Part E: Candidate solution discipline

Research objective: allow candidate solutions while preventing premature proof claims.

Required outputs for any candidate solution:

1. problem statement and source references;
2. formalism mapping;
3. exact theorem or conjecture being asserted;
4. proof artifact or computational artifact;
5. independent reconstruction instructions;
6. known-barrier review;
7. failure mode log;
8. standing result: `PASS`, `PARTIAL`, or `FAIL`.

Validation question:

```text
Can the candidate survive reconstruction by a reviewer who does not trust the authoring narrative?
```

## 4. Twelve-month program imported into repo process

The source report proposes a three-track first-year program:

- calibration track: Collatz, Jacobian, Caccetta-Haggkvist;
- flagship track: Navier-Stokes, Yang-Mills, Riemann;
- stretch geometry track: Smooth 4D Poincare, Hodge.

Repo translation:

| Month range | Repo artifact | Done condition |
|---|---|---|
| 1-2 | `research/formalism_catalog.md` | public schema exists and validates |
| 3-4 | `research/problems/*.md` | three calibration encodings exist |
| 5-6 | `research/invariants/*.md` | at least one invariant candidate has reconstruction steps |
| 7-8 | `research/flagship/*.md` | flagship notes state added structure and non-claims |
| 9-10 | `research/candidates/*.md` | at least one theorem, reduction, obstruction, or negative result is written |
| 11-12 | `research/release_manifest.json` | package validates and can be reviewed independently |

## 5. Standing boundaries for mathematical research

The repo must not represent a mapping as a solution merely because the mapping is elegant. Research standing requires:

- citation standing: source problem is well documented;
- formal standing: mapping has declared objects, transitions, and invariants;
- reconstruction standing: artifacts allow independent verification;
- testing standing: validation scripts pass;
- non-claim standing: limitations and unresolved gaps are explicit.

This keeps the research line aligned with the SPE principle that review, replayability, detection, or reconstructability does not automatically create authority to bind consequence.

## 6. Source citations

[SR-1] Deep Research report, `StegVerse Formalisms as a Research Program for Unsolved Mathematics`, Executive summary and Assumptions sections. The report cites Baez-Stay on compositional category theory, Leinster on higher operads and higher categories, Diestel on graph theory, Friedman on sheaves on graphs, and Lima on symbolic dynamics and Markov partitions.

[SR-2] Deep Research report, Executive summary. The report identifies problems with local transition rules, compositional reductions, graph-like state spaces, multiscale structure, and obstruction invariants as the strongest StegVerse targets.

[SR-3] Deep Research report, Executive summary and Top priority portfolio. The report prioritizes Collatz, Jacobian, Caccetta-Haggkvist, Navier-Stokes, Yang-Mills, Smooth 4D Poincare, Riemann, and Hodge under the StegVerse-fit ranking.

[SR-4] Deep Research report, Twelve-month research program. The report defines calibration, flagship, and stretch geometry tracks and requires a public axiomatization, benchmark suite, new theorem/reduction/obstruction, and flagship technical note as the first-year completion standard.

## 7. Non-claims

This report does not claim to solve any listed open problem.

This report does not claim that StegVerse Formalisms are already mathematically complete.

This report does not claim that an encoding, analogy, or transition table cell is a proof.

This report creates a repo-standing path for formal mathematical research artifacts to be added, cited, tested, and independently reviewed.
