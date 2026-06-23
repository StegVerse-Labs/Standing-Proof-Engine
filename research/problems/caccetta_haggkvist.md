# Caccetta-Haggkvist Calibration Encoding

Status: calibration encoding
Standing: PARTIAL
Track: calibration
Problem: Caccetta-Haggkvist conjecture

## 1. Problem statement

The Caccetta-Haggkvist conjecture concerns directed graphs and asks, in one common form, whether a directed graph on `n` vertices with minimum outdegree at least `r` must contain a directed cycle of length at most `ceil(n / r)`.

## 2. Source-standing note

This is a well-documented open problem in extremal directed graph theory. This file does not attempt to replace standard graph-theory references. It creates a StegVerse calibration encoding.

## 3. StegVerse mapping

The problem is a local-to-global transition-standing question:

```text
local condition: every vertex emits at least r outgoing edges
global consequence question: must a short directed cycle exist?
transition object: directed edge expansion, path growth, and cycle closure
standing boundary: local outdegree admissibility vs global short-cycle consequence
```

## 4. State definition

```text
State_CH := directed graph G = (V, E) with |V| = n and minimum outdegree delta_plus(G) >= r
```

## 5. Transition rule

Candidate transitions:

```text
T_expand_path(P): extend a directed path by one admissible outgoing edge
T_close_cycle(P): close a path when an edge returns to a prior vertex
T_layer_growth(S): move from reachable layer S_i to S_{i+1}
T_obstruction_candidate(G): classify graph structure that avoids short directed cycles
```

## 6. Candidate transition-table cells

| Cell candidate | Description | Reason |
|---|---|---|
| `TPT-LOCAL-DEGREE-GLOBAL-CYCLE` | local degree condition is tested against global cycle consequence | the conjecture asks whether local outdegree forces short cycles |
| `TPT-DIRECTED-EXPANSION` | directed path/layer expansion under edge constraints | path growth is the natural transition process |
| `TPT-CYCLE-CLOSURE` | repeated expansion creates or fails to create a return edge | cycle formation is the claimed consequence |
| `TPT-EXTREMAL-OBSTRUCTION` | obstruction candidates classify graphs that delay closure | counterexample search is obstruction-centered |

## 7. Invariant or obstruction candidates

Candidate directions:

1. layer-growth receipt sequences;
2. directed expansion pressure;
3. cycle-closure deficit measures;
4. extremal obstruction fingerprints;
5. admissible local degree standing vs global cycle standing separation.

## 8. Known constraints and barriers

A useful StegVerse encoding must not merely restate the outdegree bound. It must produce one of:

- a clearer obstruction taxonomy;
- a finite transition-cell classification for candidate extremal graphs;
- an executable cycle-closure certificate;
- a failure receipt for attempted counterexamples;
- a stronger bridge between local admissibility and global standing.

## 9. Reviewer reconstruction plan

A reviewer should be able to reconstruct:

1. the directed graph state;
2. the minimum outdegree condition;
3. the short-cycle consequence being tested;
4. the proposed transition-table cells;
5. the fact that no proof is claimed.

Future executable artifacts should include:

```text
samples/problems/caccetta_haggkvist_graphs.json
expected_results/problems/caccetta_haggkvist_encoding_expected.json
tests/test_caccetta_haggkvist_encoding.py
```

## 10. Non-claims

This file does not claim to solve the Caccetta-Haggkvist conjecture.

This file does not claim that local outdegree standing alone proves a short-cycle consequence.

This file does not claim that a transition-cell classification exhausts all extremal directed graphs.

## 11. Standing status

```text
PARTIAL
```

Reason: the local-to-global cycle-standing boundary is encoded, but no independent proof, obstruction theorem, or executable graph verifier exists yet.
