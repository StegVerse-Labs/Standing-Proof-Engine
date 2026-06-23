# Jacobian Calibration Encoding

Status: calibration encoding
Standing: PARTIAL
Track: calibration
Problem: Jacobian conjecture

## 1. Problem statement

The Jacobian conjecture asks whether a polynomial map over a characteristic-zero field with constant nonzero Jacobian determinant must have a polynomial inverse.

## 2. Source-standing note

This is a well-documented open problem in algebraic geometry and polynomial mapping theory. This file does not attempt to replace standard references. It creates a StegVerse calibration encoding.

## 3. StegVerse mapping

The Jacobian problem can be read as a local-to-global standing question:

```text
local condition: Jacobian determinant is constant and nonzero
global consequence question: does local invertibility force polynomial global invertibility?
transition object: polynomial map composition and reduction
standing boundary: local differential admissibility vs global algebraic invertibility
```

## 4. State definition

```text
State_Jacobian := polynomial map F: k^n -> k^n with declared field, dimension, degree, and Jacobian determinant
```

## 5. Transition rule

Candidate transitions:

```text
T_compose(F, G): F -> G o F
T_reduce_degree(F): F -> reduced normal form candidate
T_lift_dimension(F): F_n -> stabilized F_m
T_inverse_candidate(F): F -> candidate G where G o F = identity
```

## 6. Candidate transition-table cells

| Cell candidate | Description | Reason |
|---|---|---|
| `TPT-LOCAL-GLOBAL-INVERTIBILITY` | local admissibility is tested against global consequence | constant Jacobian is local; polynomial inverse is global |
| `TPT-COMPOSITION-REDUCTION` | structure is transformed by composition without changing core standing question | reductions often preserve equivalence class |
| `TPT-DEGREE-OBSTRUCTION` | degree growth and degree cancellation become standing evidence | inverse existence imposes structural constraints |
| `TPT-NORMAL-FORM-LIFT` | problem is shifted into a normalized or higher-dimensional representation | common strategy for polynomial map reductions |

## 7. Invariant or obstruction candidates

Candidate directions:

1. degree-vector standing receipts;
2. composition-chain canonicalization;
3. nilpotent perturbation class tracking;
4. inverse-candidate obstruction receipts;
5. local differential standing vs global algebraic standing separation.

## 8. Known constraints and barriers

A useful StegVerse encoding must not merely state that local invertibility should imply global invertibility. It must produce one of:

- a clearer invariant boundary;
- a canonical reduction receipt;
- a finite obstruction template;
- a testable normal-form classification;
- a failed-candidate explanation that improves search.

## 9. Reviewer reconstruction plan

A reviewer should be able to reconstruct:

1. the local Jacobian condition;
2. the global inverse claim;
3. the difference between local admissibility and global standing;
4. the proposed transition-table cells;
5. the fact that no proof is claimed.

Future executable artifacts should include:

```text
samples/problems/jacobian_maps.json
expected_results/problems/jacobian_encoding_expected.json
tests/test_jacobian_encoding.py
```

## 10. Non-claims

This file does not claim to solve the Jacobian conjecture.

This file does not claim that local-to-global framing is a proof.

This file does not claim that a normal-form transition preserves all proof-relevant structure unless separately verified.

## 11. Standing status

```text
PARTIAL
```

Reason: the local-to-global transition boundary is encoded, but no independent proof, obstruction theorem, or executable verifier exists yet.
