# What the finite check establishes

## 1. Explicit modern semantics

Let the universe `U` be nonempty and let `A`, `B`, and `C` be arbitrary subsets
of it. Empty terms are permitted unless a named assumption regime excludes
them. The categorical relations are:

- `A(X,Y)`: every `X` is `Y`, meaning `X ⊆ Y`.
- `E(X,Y)`: no `X` is `Y`, meaning `X ∩ Y = ∅`.
- `I(X,Y)`: some `X` is `Y`, meaning `X ∩ Y ≠ ∅`.
- `O(X,Y)`: some `X` is not `Y`, meaning `X \ Y ≠ ∅`.

The relation names `A/E/I/O` must not be confused with the term names `A/B/C`.
In this reconstruction neither universal relation has existential import.
In particular, both `A(X,Y)` and `E(X,Y)` are true when `X` is empty.
`I` is ordinary existential “some,” not “some but not all.”

Three separately reported regimes are used:

1. `empty_terms_allowed`: no term-existence assumptions.
2. `all_terms_nonempty`: `A ≠ ∅`, `B ≠ ∅`, and `C ≠ ∅`.
3. `A_nonempty_only`: just `A ≠ ∅`; `B` and `C` may be empty except insofar as
   the premises themselves force existence.

The third is a targeted assumption for the displayed fifth affirmative form.
These are explicit alternative modern readings, not an assertion that there is
one historically uniform convention about existential import.

## 2. Region-abstraction theorem

**Theorem.** For any argument made from the relations above on three unary
predicates, possibly with the term-nonemptiness assumptions used here, a
countermodel on any nonempty universe exists if and only if a countermodel
exists among the 255 nonzero occupancy masks of the eight membership types.

**Proof.** Assign every `u ∈ U` its type

`t(u) = 1·[u ∈ A] + 2·[u ∈ B] + 4·[u ∈ C]`.

There are exactly eight types, `0` through `7`. They partition `U`; type `0`
contains elements outside all three terms. For each occupied type keep one
representative. The resulting universe `U*` has between one and eight elements.
It is nonempty because `U` is nonempty.

For any terms `X,Y`, the truth of `I(X,Y)` is exactly whether at least one
occupied type has both the `X` and `Y` bits. The truth of `O(X,Y)` is exactly
whether at least one occupied type has its `X` bit and lacks its `Y` bit.
`E(X,Y)` and `A(X,Y)` are respectively the negations of those existence
conditions. Term nonemptiness likewise asks whether some occupied type has the
relevant bit. Replacing an occupied type by one representative preserves every
one of these conditions, so it preserves all premises, all assumption regimes,
and the conclusion. Thus any original countermodel reduces to one of the finite
representatives. Conversely every nonzero occupancy mask specifies a genuine
nonempty-universe set model, so any countermodel found there is already a
countermodel in the original semantics. This proves both directions. □

The implementation traverses **all 256 raw masks**, as requested. Raw mask `0`
has no witnesses, so it is supplied with a single type-`0` outside witness to
maintain a nonempty universe. It consequently duplicates raw mask `1`.
There are **255 distinct interpreted models**, not 256 distinct nonempty models.
The duplication does not affect validity. Counts of raw masks and distinct
models are identified separately in the JSON. Under all-terms-nonempty there
are 218 masks; under A-only-nonempty there are 240, with no duplication in either
regime.

Consequently this is a finite **decision procedure justified by a completeness
reduction**, not an experiment that checks a few small universes and extrapolates
to arbitrary sizes. The unit tests on universes of size one through three are
implementation cross-checks only; they are not the justification for universal
validity. The theorem does not cover counting, “at least two,” binary relations,
ordering of witnesses, or full first-order logic.

## 3. Direct proofs of the nine supplied forms

The labels below are convenient labels for this reconstruction. All statements
in this section use the semantics above.

| Label | Premises | Conclusion | Direct reason |
|---|---|---|---|
| A1 | `A ⊆ B`, `C ⊆ A` | `C ⊆ B` | Transitivity of inclusion. |
| A2 | `A ⊆ B`, `C ∩ A ≠ ∅` | `C ∩ B ≠ ∅` | The same witness is in `B`. |
| A3 | `A ⊆ B`, `C ∩ B = ∅` | `C ∩ A = ∅` | Any supposed common witness would also be in `B`. |
| A4 | `A ⊆ B`, `C \ B ≠ ∅` | `C \ A ≠ ∅` | A witness outside `B` is outside its subset `A`. |
| A5 | `A ⊆ B`, `B ⊆ C` | `C ∩ A ≠ ∅` | **Requires `A ≠ ∅`**; then any element of `A` witnesses the intersection. |
| E1 | `A ∩ B = ∅`, `C ⊆ B` | `C ∩ A = ∅` | A witness in both would contradict disjointness. |
| E2 | `A ∩ B = ∅`, `C ⊆ A` | `C ∩ B = ∅` | The symmetric inclusion argument. |
| E3 | `A ∩ B = ∅`, `C ∩ A ≠ ∅` | `C \ B ≠ ∅` | The shared `C,A` witness cannot be in `B`. |
| E4 | `A ∩ B = ∅`, `C ∩ B ≠ ∅` | `C \ A ≠ ∅` | The shared `C,B` witness cannot be in `A`. |

Under A5's premises, `A ⊆ C`, hence `C ∩ A = A`. Its conclusion is therefore
**equivalent to `A ≠ ∅` under those premises**, not merely implied by the
stronger assumption that all three terms exist. The explicit counterexample
`A = ∅`, `B = C = {b}` also demonstrates that nonempty `B` and `C` alone do not
suffice. The unrestricted enumeration has 16 raw premise-satisfying masks,
representing 15 distinct models, and eight raw counterexample masks,
representing seven distinct nonempty-universe models because of the outside-only
duplication. Its raw masks are `0, 1, 16, 17, 64, 65, 80, 81`.

`E(X,Y)` and `I(X,Y)` admit simple conversion because intersection is symmetric.
Reversing every eligible occurrence of these relations yields 28 explicit
variants of the nine displayed forms. Two variants are the existence-dependent
A5 form and its I-converse; thus 26 are valid without existence assumptions and
all 28 are valid in each of the two nonemptiness regimes.
The converse of `A` or `O` is not generally licensed. For example, with
`A = {a}` and `B = {a,b}`, `A(A,B)` holds but `A(B,A)` does not. With
`A = {a,b}` and `B = {b}`, `O(A,B)` holds but `O(B,A)` does not.

## 4. What the fixed-first-premise audit does, and does not, count

This audit is deliberately broader than checking the displayed formulas, but
deliberately narrower than claiming a reconstruction of all historical
syllogistic forms.

For each fixed first premise, either `A(A,B)` or `E(A,B)`, it:

1. Chooses the second premise between `C` and one of `A,B`.
2. Permits both subject–predicate orders and all four categorical kinds.
   This gives `2 × 2 × 4 = 16` second premises.
3. Chooses a conclusion between `C` and the **other, unshared end term** of the
   first premise, again in both directions and all four kinds.
   This gives `2 × 4 = 8` possible conclusions for each second premise.

Thus each audit examines 128 ordered candidate arguments. Reversing an `E` or
`I` relation is included as another raw candidate; the report also counts
classes after identifying such reversals. Every candidate's premises are
satisfiable in every reported regime, so none of these validity counts arise
from an inconsistent premise pair.

Two explicitly different comparisons with the nine displayed formulas are
reported. Both allow any **bijective renaming of the three terms** and simple
**E/I conversion**. The ordered comparison retains premise order; the unordered
comparison additionally permits **exchanging the two premises**. Neither adds
subalternation, contraposition, weakening of a conclusion, or arbitrary chaining
of derived rules. Matching is syntactic; the validity of each target argument
is checked independently in the chosen target regime. In particular, the
asymmetric assumption `A_nonempty_only` is not silently treated as invariant
under every renaming.

| Assumptions | First premise | Valid ordered candidates | E/I-only classes | Displayed matches, ordered | Displayed matches, unordered |
|---|---|---:|---:|---:|---:|
| Empty terms allowed | `A(A,B)` | 12 | 6 | 10 | 11 |
| Empty terms allowed | `E(A,B)` | 8 | 4 | 8 | 8 |
| All terms nonempty | `A(A,B)` | 24 | 12 | 12 | 15 |
| All terms nonempty | `E(A,B)` | 14 | 10 | 8 | 8 |
| Only A nonempty | `A(A,B)` | 20 | 10 | 12 | 13 |
| Only A nonempty | `E(A,B)` | 10 | 6 | 8 | 8 |

Two concrete additional cases matter:

- **Common subject:** `A(A,B) & A(A,C) ⇒ I(C,B)` is valid if `A` is nonempty:
  any witness in `A` is in both `B` and `C`. It fails with
  `A = ∅`, `B = {b}`, `C = {c}`. It matches none of the nine displayed formulas,
  even with term renaming, E/I conversion, and premise exchange. Its two
  universal premises share their subject; A5's universal premises form a chain.
  These structural patterns are distinct under the stated comparisons.
- **Witness propagation without existence assumptions:**
  `A(A,B) & O(A,C) ⇒ O(B,C)` is valid because the `A \ C` witness also belongs
  to `B \ C`. It too is unmatched by the displayed formulas under the two
  comparisons. It is the sole remaining unmatched raw candidate with first
  `A(A,B)` and no existence assumptions after premise exchange is allowed.

Other additional candidates include weakened conclusions from already-listed
universal conclusions when term existence is available. For example, if
`E(C,A)` and `C ≠ ∅`, then `O(C,A)`. Counting this as a distinct ordered
candidate does not establish a historically distinct “form.” Likewise the
universal chain `A(A,B) & A(B,C) ⇒ A(A,C)` is A1 after a renaming and premise
exchange, though it is not an ordered-first-premise match.

The report therefore supports a **qualified completeness concern** about the
displayed nine under these explicit modern criteria. It does not establish
that Euler intended exactly either criterion, that no broader equivalence or
contextual convention could matter, or that the letter catalogued every valid
syllogism in the entire tradition. It does not audit all possible first-premise
kinds, arbitrary numbers of premises, or the whole surrounding work.

## 5. The displayed no-inference situation

The premises `A ⊆ B` and `C ∩ A = ∅` do not settle how `C` lies relative to `B`.
Use `U = {a,b,c}`, `A = {a}`, and `B = {a,b}`. All terms can be nonempty in each
of these three models:

| C | Relation to B |
|---|---|
| `{c}` | Disjoint from B. |
| `{b}` | Wholly contained in B. |
| `{b,c}` | Partly inside B and partly outside B. |

Each satisfies the two premises. Together they refute every unconditional
categorical conclusion from `C` to `B`: `A(C,B)`, `E(C,B)`, `I(C,B)`, and
`O(C,B)` are each false in at least one of the examples. This direction matters:
if `A` is nonempty, those premises **do** imply `O(B,C)`, since a witness in `A`
lies in `B` and outside `C`. “No inference” here means no one of the four
listed **C-to-B** conclusions, not literally no logical consequence whatsoever.

## 6. “Some” and the pear-tree example

`I(A,B)` does not imply `O(A,B)`: take `A = B = C = {p}`. This is a countermodel
even under all-terms-nonempty. It also shows why an ordinary existential
statement must not be read as “some but not all.”

For the tree example let `P` be pear trees and `T` be trees. The assumptions
`P ⊆ T` and `T ∩ P ≠ ∅` are compatible with `P = T = {pear}`. They do not imply
that any tree is not a pear tree. The claim `P ⊊ T` is stronger: by the definition
of proper inclusion it adds a witness in `T \ P`. Such a witness can come from
an extra factual premise (for example an oak that is a tree and not a pear
tree), but cannot come from the meaning of existential “some” alone.

The named examples preserve the original lettering `A = trees`, `B = pear
trees`. The strict-inclusion example in the JSON explicitly adds `O(A,B)` to
`A(B,A)`, with `A = {pear,oak}` and `B = {pear}`. That added premise *is the extra
strictness assumption*; the output does not present it as a deduction from
inclusion or from `I`. The separate equality counterexample makes the missing
assumption visible.

## 7. Verification limits

The implementation and its 30 standard-library unit tests were written together.
The tests include a second set-based evaluator, all 9,216 categorical evaluations
on the 256 raw masks, and independent concrete membership assignments on
universes of sizes one through three. These are useful implementation checks,
not an independent scholarly review. A separate oracle review can compare these
results without reusing `euler_logic.py`'s evaluator or model generator for its
expected answers; importing that module as the system under test is compatible
with this independence. The separate review's completion should be recorded
in its own artifact. No such external review is claimed by the test suite.
