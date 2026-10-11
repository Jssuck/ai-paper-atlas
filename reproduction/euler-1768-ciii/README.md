# Euler Letter CIII: reproducible set-semantics audit

A dependency-free Python reconstruction of nine formalized categorical
arguments associated with Letter CIII. It distinguishes empty-term semantics
from explicit existential assumptions and audits a larger, precisely bounded
set of fixed-first-premise candidates.

**Main result:** eight of the nine supplied forms hold without term-existence
assumptions. A5 requires `A ≠ ∅`; all nine hold when that assumption is added.
The audit also identifies valid candidate patterns not represented by the nine
displayed formulas under the explicit matching conventions below.

## Run exactly

Requirements: Python 3.8 or later; only the standard library. The recorded run
used CPython **3.12.14**, Linux x86_64. No package installation or network access
is needed by these scripts.

From this directory:

```sh
mkdir -p results
python3 -m unittest discover -s tests -v
python3 reproduce.py --output results
```

To regenerate the captured logs, using Bash and failing if either command fails:

```bash
set -euo pipefail
mkdir -p results
python3 -m unittest discover -s tests -v 2>&1 | tee results/tests.log
python3 reproduce.py --output results 2>&1 | tee results/run.log
```

The commands perform local writes only. `report.json` and `report.txt` contain
the semantic results. `environment.json` records the runtime and SHA-256 hashes
of the implementation, runner, and tests. Environment timestamps and test-run
duration naturally vary; the logical report is deterministic.

## Recorded results

The checked-in run completed successfully: **30 tests passed**. The CLI also
completed successfully and produced parseable JSON and the text report.
`results/tests.log` is the captured unit-test output and `results/run.log` is
the captured reproduction output. A JSON-to-text roundtrip regression is among
the passing tests.

### Displayed forms

| Assumption regime | Raw masks / distinct models | Valid displayed forms | Explicit E/I variants valid |
|---|---:|---:|---:|
| Empty terms allowed | 256 / 255 | 8 / 9 | 26 / 28 |
| All A, B, C nonempty | 218 / 218 | 9 / 9 | 28 / 28 |
| Only A assumed nonempty | 240 / 240 | 9 / 9 | 28 / 28 |

The 256 raw masks describe occupancy of eight membership types. To keep the
universe nonempty, raw mask zero is given a witness outside all terms; it then
duplicates raw mask one. This is why the unrestricted count is 255 distinct
models. **The mathematical completeness argument is in [PROOF.md](PROOF.md)**:
every arbitrary-universe countermodel in this fragment reduces to one witness
per occupied type. This is not a claim that finitely many sampled universes
alone prove validity.

The exceptional A5 is:

```text
A(A,B) & A(B,C) => I(C,A)
```

Under those premises, `C ∩ A = A`, so its conclusion is equivalent to `A` being
nonempty. Without existence assumptions its premises hold in **16 raw masks /
15 distinct models**, and its conclusion fails in **8 raw masks / 7 distinct
models**. An especially clear counterexample is
`A = ∅` and `B = C = {b}`.

### Bounded completeness audit

For fixed first premise `A(A,B)` or `E(A,B)`, all 16 second premises connecting
`C` with `A` or `B` are paired with all eight conclusions between the two
unshared end terms. Both directions and all four categorical kinds are
included, for **128 ordered candidates per first premise per regime**.

| Assumptions | First premise | Valid / 128 | Matches to displayed forms, keeping premise order | Matches also allowing premise exchange |
|---|---|---:|---:|---:|
| Empty terms allowed | A(A,B) | 12 | 10 | 11 |
| Empty terms allowed | E(A,B) | 8 | 8 | 8 |
| All terms nonempty | A(A,B) | 24 | 12 | 15 |
| All terms nonempty | E(A,B) | 14 | 8 | 8 |
| Only A nonempty | A(A,B) | 20 | 12 | 13 |
| Only A nonempty | E(A,B) | 10 | 8 | 8 |

Both matching columns permit bijective term renaming and E/I conversion. The
second additionally exchanges premise order. Neither silently adds weakening,
subalternation, contraposition, or chaining of rules. Counts are ordered
syntactic candidates, not counts of historically distinct syllogistic forms.
The JSON also gives E/I-only equivalence-class counts and every candidate's
validity or explicit countermodel masks.

Two focused findings:

- `A(A,B) & A(A,C) => I(C,B)` is valid if `A` exists, but matches none of the nine
  displayed forms under either convention. This common-subject pattern differs
  from the chain in A5.
- `A(A,B) & O(A,C) => O(B,C)` is valid even with empty terms permitted and is
  likewise unmatched.

These findings support a qualified concern about completeness of the displayed
list **under the specified modern comparison criteria**. Euler's historical
criterion for distinct “forms” is not fully reconstructed here. This is not a
claim to have audited all of Euler's syllogistic. Some other extra candidates
are simply weaker conclusions available once existence is assumed.

## Further countermodels and examples

- `A ⊆ B` and `C ∩ A = ∅` allow `C` to be disjoint from `B`, wholly inside `B`,
  or partially overlapping `B`; three explicit all-terms-nonempty models are
  saved. No one of the four **C-to-B** categorical conclusions follows. With `A`
  nonempty, the reverse-direction consequence `O(B,C)` does follow.
- `I(A,B)` does **not** imply `O(A,B)`, including when all three terms exist.
- Pear trees being included among trees, and some trees being pear trees, do
  not establish a non-pear tree. Equality of the two classes is a countermodel;
  proper inclusion supplies an additional witness and is an extra assumption.
  The named examples retain `A = trees`, `B = pear trees`, so their inclusion is
  `B ⊆ A`.
- E and I convert simply; A and O generally do not.

## Files

- `euler_logic.py`: semantic evaluator, nine-form catalog, explicit conversion
  variants, fixed-first candidate generation and matching, named examples.
- `reproduce.py`: executable reproduction and JSON/text/environment writer.
- `tests/test_euler_logic.py`: 30 tests, including exhaustive bitmask/set
  agreement, concrete small-universe abstraction checks, CLI roundtrip,
  existential-import regressions, and candidate-scope checks.
- `PROOF.md`: completeness reduction, direct proofs, existence analysis,
  matching conventions, limits, and interpretation of additional cases.
- `results/report.json`: full machine-readable results, including all 768
  regime/candidate checks and their counterexample masks.
- `results/report.txt`: readable summary and explicit example models.
- `results/environment.json`, `results/tests.log`, `results/run.log`: provenance
  and captured execution records.

## Independent review and visual QA

A separate [independent code and semantics review](review/review.zh-CN.md)
(in Chinese) is included. Its standard-library quantifier/set oracle independently
constructs the expected formulas, models, candidate inventory, and matching
orbits, and compares them with the implementation. All **8 independent test
groups** pass; a separate rerun also passes the 30 implementation tests and
reproduces the JSON/text reports byte-for-byte. Runtime details and source
SHA-256 hashes are in `review/independent_results.json`.

Re-run the full independent check from this directory:

```sh
bash review/run_review.sh
```

The [diagram visual QA record](qa/visual-review.zh-CN.md) documents the separate
rendering and visual inspection. These review artifacts state their own scope;
passing implementation tests alone would not establish independent review.
