# Collatz Calibration Encoding

Status: calibration encoding
Standing: PARTIAL
Track: calibration
Problem: Collatz conjecture

## 1. Problem statement

For a positive integer `n`, repeatedly apply:

```text
C(n) = n / 2       if n is even
C(n) = 3n + 1     if n is odd
```

The conjecture states that every positive integer eventually reaches `1` under repeated application of `C`.

## 2. Source-standing note

This is a well-documented open problem in elementary number theory and dynamical systems. This repo file does not attempt to replace standard mathematical references. It creates a StegVerse calibration encoding.

## 3. StegVerse mapping

The Collatz problem is a minimal local-transition system with a global standing question.

```text
state: positive integer n
transition: parity-conditioned map C(n)
orbit: n, C(n), C^2(n), ...
terminal cycle: 1 -> 4 -> 2 -> 1
standing question: does every admissible initial state enter the terminal cycle?
```

## 4. State definition

```text
State_Collatz := positive integer n with parity signature p(n) = n mod 2
```

## 5. Transition rule

```text
T_even(n): n -> n / 2
T_odd(n): n -> 3n + 1
```

Compressed odd transition candidate:

```text
T_odd_compressed(n): n -> (3n + 1) / 2^v2(3n + 1)
```

where `v2(k)` is the exponent of the largest power of `2` dividing `k`.

## 6. Candidate transition-table cells

| Cell candidate | Description | Reason |
|---|---|---|
| `TPT-PARITY-BRANCH` | parity-conditioned local transition | the rule depends on even/odd state class |
| `TPT-ORBIT-COLLAPSE` | repeated local transitions appear to collapse to a terminal cycle | the conjecture asks for universal convergence |
| `TPT-MONOTONE-FAILURE` | simple size monotonicity fails | odd transitions can increase state size |
| `TPT-COMPRESSED-RETURN` | accelerated return map after odd transition | useful for studying net descent after expansion |

## 7. Invariant or obstruction candidates

Candidate directions:

1. parity-word admissibility constraints;
2. logarithmic drift over compressed odd transitions;
3. residue-class obstruction search;
4. cycle exclusion by transition receipt reconstruction;
5. orbit-height certificate schema.

## 8. Known constraints and barriers

A useful StegVerse encoding must not merely restate the recurrence. It must produce one of:

- a new invariant;
- a stronger obstruction search;
- a finite certificate class;
- a falsifiable transition-cell prediction;
- a computational receipt format that improves independent reconstruction.

## 9. Reviewer reconstruction plan

A reviewer should be able to reconstruct:

1. the local rule;
2. the terminal cycle;
3. the accelerated odd map;
4. the proposed transition-table cells;
5. the fact that no proof is claimed.

Future executable artifacts should include:

```text
samples/problems/collatz_orbits.json
expected_results/problems/collatz_encoding_expected.json
tests/test_collatz_encoding.py
```

## 10. Non-claims

This file does not claim to solve the Collatz conjecture.

This file does not claim that a transition-table classification is a proof.

This file does not claim that orbit sampling establishes universal convergence.

## 11. Standing status

```text
PARTIAL
```

Reason: the local transition system is encoded, but no independent proof, obstruction theorem, or executable certificate validator exists yet.
