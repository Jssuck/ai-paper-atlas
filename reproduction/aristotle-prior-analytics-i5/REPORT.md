# Generated model results

Modern AEIO set semantics; premises **Q(P,M), R(S,M)** and conclusion **T(S,P)**.
The universe is always nonempty. A and E have no built-in existential import.
`V` = valid; `× n [a,…]` = invalid, with smallest countermodel size n and occupied atoms.
Atoms use membership bits P=4, M=2, S=1. Full concrete named models are in `report.json`.

## allow-empty

Eligible supports: **255**. Valid moods: **AEE, AOO, EAE, EIO**.

| Premises Q,R | A(S,P) | E(S,P) | I(S,P) | O(S,P) | Premise supports |
|---|---|---|---|---|---:|
| AA | × 1 [3] | × 1 [7] | × 1 [0] | × 1 [0] | 31 |
| AE | × 1 [1] | V | × 1 [0] | × 1 [0] | 15 |
| AI | × 1 [3] | × 1 [7] | × 1 [3] | × 1 [7] | 48 |
| AO | × 1 [1] | × 2 [1,7] | × 1 [1] | V | 32 |
| EA | × 1 [3] | V | × 1 [0] | × 1 [0] | 15 |
| EE | × 1 [1] | × 1 [5] | × 1 [0] | × 1 [0] | 31 |
| EI | × 1 [3] | × 2 [3,5] | × 1 [3] | V | 32 |
| EO | × 1 [1] | × 1 [5] | × 1 [1] | × 1 [5] | 48 |
| IA | × 2 [3,6] | × 1 [7] | × 1 [6] | × 1 [6] | 48 |
| IE | × 2 [1,6] | × 2 [5,6] | × 1 [6] | × 1 [6] | 32 |
| II | × 2 [3,6] | × 1 [7] | × 2 [3,6] | × 1 [7] | 160 |
| IO | × 2 [1,6] | × 2 [5,6] | × 2 [1,6] | × 2 [5,6] | 144 |
| OA | × 2 [3,4] | × 2 [4,7] | × 1 [4] | × 1 [4] | 32 |
| OE | × 2 [1,4] | × 1 [5] | × 1 [4] | × 1 [4] | 48 |
| OI | × 2 [3,4] | × 2 [3,5] | × 2 [3,4] | × 2 [4,7] | 144 |
| OO | × 2 [1,4] | × 1 [5] | × 2 [1,4] | × 1 [5] | 160 |

## all-nonempty

Eligible supports: **218**. Valid moods: **AEE, AEO, AOO, EAE, EAO, EIO**.

| Premises Q,R | A(S,P) | E(S,P) | I(S,P) | O(S,P) | Premise supports |
|---|---|---|---|---|---:|
| AA | × 2 [3,6] | × 1 [7] | × 2 [3,6] | × 1 [7] | 20 |
| AE | × 2 [1,6] | V | × 2 [1,6] | V | 4 |
| AI | × 2 [3,6] | × 1 [7] | × 2 [3,6] | × 1 [7] | 40 |
| AO | × 2 [1,6] | × 2 [1,7] | × 2 [1,6] | V | 24 |
| EA | × 2 [3,4] | V | × 2 [3,4] | V | 4 |
| EE | × 3 [1,2,4] | × 2 [2,5] | × 3 [1,2,4] | × 2 [2,5] | 10 |
| EI | × 2 [3,4] | × 2 [3,5] | × 2 [3,4] | V | 24 |
| EO | × 2 [3,5] | × 2 [2,5] | × 3 [1,2,4] | × 2 [2,5] | 30 |
| IA | × 2 [3,6] | × 1 [7] | × 2 [3,6] | × 1 [7] | 40 |
| IE | × 2 [1,6] | × 2 [5,6] | × 2 [1,6] | × 2 [5,6] | 24 |
| II | × 2 [3,6] | × 1 [7] | × 2 [3,6] | × 1 [7] | 160 |
| IO | × 2 [1,6] | × 2 [5,6] | × 2 [1,6] | × 2 [5,6] | 144 |
| OA | × 2 [3,4] | × 2 [4,7] | × 2 [3,4] | × 2 [4,7] | 24 |
| OE | × 3 [1,2,4] | × 2 [2,5] | × 3 [1,2,4] | × 2 [2,5] | 30 |
| OI | × 2 [3,4] | × 2 [3,5] | × 2 [3,4] | × 2 [4,7] | 144 |
| OO | × 2 [3,5] | × 2 [2,5] | × 3 [1,2,4] | × 2 [2,5] | 150 |

## subject-nonempty

Eligible supports: **240**. Valid moods: **AEE, AEO, AOO, EAE, EAO, EIO**.

| Premises Q,R | A(S,P) | E(S,P) | I(S,P) | O(S,P) | Premise supports |
|---|---|---|---|---|---:|
| AA | × 1 [3] | × 1 [7] | × 1 [3] | × 1 [7] | 24 |
| AE | × 1 [1] | V | × 1 [1] | V | 8 |
| AI | × 1 [3] | × 1 [7] | × 1 [3] | × 1 [7] | 48 |
| AO | × 1 [1] | × 2 [1,7] | × 1 [1] | V | 32 |
| EA | × 1 [3] | V | × 1 [3] | V | 8 |
| EE | × 1 [1] | × 1 [5] | × 1 [1] | × 1 [5] | 24 |
| EI | × 1 [3] | × 2 [3,5] | × 1 [3] | V | 32 |
| EO | × 1 [1] | × 1 [5] | × 1 [1] | × 1 [5] | 48 |
| IA | × 2 [3,6] | × 1 [7] | × 2 [3,6] | × 1 [7] | 40 |
| IE | × 2 [1,6] | × 2 [5,6] | × 2 [1,6] | × 2 [5,6] | 24 |
| II | × 2 [3,6] | × 1 [7] | × 2 [3,6] | × 1 [7] | 160 |
| IO | × 2 [1,6] | × 2 [5,6] | × 2 [1,6] | × 2 [5,6] | 144 |
| OA | × 2 [3,4] | × 2 [4,7] | × 2 [3,4] | × 2 [4,7] | 24 |
| OE | × 2 [1,4] | × 1 [5] | × 2 [1,4] | × 1 [5] | 40 |
| OI | × 2 [3,4] | × 2 [3,5] | × 2 [3,4] | × 2 [4,7] | 144 |
| OO | × 2 [1,4] | × 1 [5] | × 2 [1,4] | × 1 [5] | 160 |

## Direction matters: IE

I(P,M), E(S,M) entails **O(P,S)** under all three policies, but does **not** entail O(S,P), the fixed second-figure conclusion direction.

## Scope of the result

The program exhausts finite Boolean supports, not arbitrary domain cardinalities. The separate support-compression argument in WALKTHROUGH.md explains why those supports suffice for this particular three-unary-predicate AEIO language. Tests do not establish the historical fidelity of the chosen modern semantics.
