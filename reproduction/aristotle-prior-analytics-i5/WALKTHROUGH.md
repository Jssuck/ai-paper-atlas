# Walkthrough: from membership types to second-figure validity

## 1. Fix the direction before reasoning

Every row has premises `Q(P,M)` and `R(S,M)`. Its columns test `A(S,P)`, `E(S,P)`,
`I(S,P)` and `O(S,P)`, respectively. All clauses are **subject first, predicate
second**. Do not silently reverse `P` and `S` when a tempting conclusion appears.

The reference semantics are:

```text
A(X,Y): every element of X is in Y
E(X,Y): X and Y share no element
I(X,Y): X and Y share at least one element
O(X,Y): some element of X is outside Y
```

The universe is nonempty in every policy. Universal clauses do not themselves
assert that their subject or predicate exists.

## 2. Replace labels by membership types

An object can have any of eight membership signatures:

| Atom | P | M | S |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 1 |
| 2 | 0 | 1 | 0 |
| 3 | 0 | 1 | 1 |
| 4 | 1 | 0 | 0 |
| 5 | 1 | 0 | 1 |
| 6 | 1 | 1 | 0 |
| 7 | 1 | 1 | 1 |

An object outside all three terms has atom 0; it is **not** the empty universe.
For example, support mask 1 occupies just atom 0 and represents a one-object
universe with P=M=S=∅. Support mask 0 would be an empty universe and is rejected.

A support records which types occur, not how many objects have each type.
There are `2**8 - 1 = 255` nonempty supports. Distinct labels and multiplicities
produce many more ordinary models but add no AEIO truth information.

For all three terms to be nonempty, use inclusion-exclusion on all 256 supports:

```text
256 − 3×16 + 3×4 − 2 = 218.
```

There are 16 supports (including the empty support) with a given term empty,
4 with a given pair of terms empty, and 2 with all three terms empty. The empty
support is removed by the same inclusion-exclusion, so no further subtraction
is needed. Requiring only S nonempty leaves `256 − 16 = 240` supports.

## 3. Why finite support checking is enough for this language

This is a **mathematical argument separate from the tests**.

Let U be any nonempty universe, finite or infinite, with three unary term
extensions P, M and S. Map each object to its three Boolean membership bits.
Let B be the set of occupied types. It is nonempty and has at most eight members.
Now build a new universe whose objects are the types in B; a term contains a
type exactly when its corresponding bit is 1. No choice of arbitrary
representatives from an infinite collection is needed.

For any pair X,Y of our terms:

- A(X,Y) fails exactly when an occupied type has X=1 and Y=0.
- E(X,Y) fails exactly when an occupied type has X=1 and Y=1.
- I(X,Y) holds exactly when an occupied type has X=1 and Y=1.
- O(X,Y) holds exactly when an occupied type has X=1 and Y=0.

Consequently every AEIO clause preserves its truth under this transformation.
A term is nonempty exactly when an occupied type has its bit set, so all three
existence policies are preserved too. Every conjunction of these premises and
each tested conclusion therefore have the same truth in the original and type
models.

It follows that any countermodel, however large, has a support countermodel
with at most eight objects. Conversely, every enumerated support is realized
by one object per occupied type. Thus an exhaustive and correctly implemented
support check decides entailment **for this specified language and semantics**.

The tests are not this proof. They compare implementations and examples; they
cannot by themselves validate a universal preservation claim or a historical
interpretation. Extensions with numerical cardinality claims, relations,
identity-sensitive formulas or modalities would need a new argument and model.

## 4. Four valid moods, directly

These arguments work even if some term extensions are empty.

### EAE

`E(P,M)` says P and M are disjoint. `A(S,M)` puts all S inside M. An object in
both S and P would therefore lie in both M and P, a contradiction. Hence
`E(S,P)`.

### AEE

`A(P,M)` puts all P inside M. `E(S,M)` makes S disjoint from M. An object in
both S and P would lie in both S and M, a contradiction. Hence `E(S,P)`.

### EIO

`I(S,M)` supplies an object x in S and M. Because `E(P,M)`, x is not in P.
It witnesses `O(S,P)`. The particular premise supplies the needed existence;
no extra nonemptiness policy is necessary.

### AOO

`O(S,M)` supplies an object x in S but outside M. Since `A(P,M)` puts P inside
M, x cannot be in P. It witnesses `O(S,P)`.

## 5. Why EAO and AEO need existence

Both EAE and AEE establish `E(S,P)`. If S is nonempty, choose x in S. Disjointness
puts x outside P, so `O(S,P)` follows. Therefore requiring S nonempty alone is
enough for the weakened EAO and AEO conclusions; requiring all three terms
nonempty is stronger than necessary.

Without S's existence, the one-object universe with P=M=S=∅ is a countermodel
for both weakened moods. All relevant universal premises are true, but the
particular O conclusion has no witness. This is the support `[0]`, mask 1.

These policy differences are an explicit modern modeling choice, not a verdict
about how every passage of the historical syllogistic should be interpreted.

## 6. The IE reversal trap

Consider:

```text
I(P,M): some P is M
E(S,M): no S is M
```

The first premise gives an x in P and M. The second ensures x is not S. This
proves **O(P,S)**: some P is not S. It does not prove **O(S,P)**.

A countermodel to the latter, with all terms nonempty, is:

```text
U = {a,b}
P = {a,b}
M = {a}
S = {b}
```

I(P,M) is witnessed by a; S and M are disjoint. But S⊆P, so O(S,P) is false.
The occupied atoms are 6 for a and 5 for b; the mask is 96. Two objects are
necessary here under all-nonempty: a single object would have to be in all three
terms, contradicting E(S,M). If empty S is allowed, a single atom-6 object already
refutes O(S,P).

Conversely, the EI pair used in EIO genuinely proves the forward O(S,P). It does
not generally prove the reversed O(P,S). The program tests both directions.

## 7. Inspect a three-object smallest countermodel

Under the all-nonempty policy, `EEI` asks whether
`E(P,M), E(S,M)` entail `I(S,P)`. They do not:

```text
U = {x1,x2,x3}
S = {x1}     (atom 1)
M = {x2}     (atom 2)
P = {x3}     (atom 4)
```

Both premises hold and S∩P is empty. All three terms exist. To falsify I(S,P), S
and P must be disjoint; the premises also make M disjoint from each. Three
nonempty pairwise disjoint terms require at least three objects. Thus this
support `[1,2,4]`, mask 22, is not just a countermodel but a smallest one.

The program searches supports by `(occupied-type count, numeric mask)` and
records the first falsifying model. Any ordinary model compresses to a model
with no more objects, so this search order yields globally smallest finite
countermodel cardinality. A larger finite or infinite model cannot make a
smaller cardinality necessary. Numeric-mask tie-breaking is only for
reproducibility.

## 8. What to inspect in the verification

The test suite's separate oracle decodes supports as Boolean tuples and checks
ordinary set membership, rather than calling the production atom evaluator to
decide its expected answers. It checks:

- All 255 supports and the policy filters (255, 218, 240).
- All 9,180 atomic evaluations: 255 supports × 4 quantifiers × 3 subject terms
  × 3 predicate terms, including repeated subject/predicate terms.
- All 64 moods under each of three policies: 192 classifications.
- Every invalid result's witness, policy compliance, premise truth, false
  conclusion, and cardinality/numeric tie-break minimality: 176 witnesses.
- Every premise pair's support count and satisfiability.
- Every support's concrete realization and compression round-trip.
- All 584 labeled models of sizes 1–3 (`8 + 8**2 + 8**3`), checking compression
  preserves every atomic clause and each policy.
- Direction reversal, empty-subject weakening failures, explicitly inconsistent
  premises, invalid inputs, report consistency and command-line behavior.

`run_verification.py` records normal, `-O`, and `-OO` execution. These modes test
that removed assertions or docstrings do not change behavior; they are not three
independent semantic audits. The in-package oracle was written with the same
package, so an external review remains useful.

For a classroom exercise, select an invalid cell in [REPORT.md](REPORT.md),
translate its atom list into term extensions, and verify both premises and the
negation of its conclusion by hand before reading `report.json`.
