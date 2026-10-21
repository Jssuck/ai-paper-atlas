# Aristotle, *Prior Analytics* I.5: a second-figure teaching model

A small, **Python-standard-library-only** reproduction of the second figure's
validity pattern under explicit **modern set-theoretic AEIO semantics**. It is a
teaching companion, not a claim that Aristotle used Boolean enumeration or these
exact existence conventions.

## Results at a glance

The fixed premise/conclusion order is:

```text
Q(P,M), R(S,M) ⟹ T(S,P)
```

`P` is the conclusion's predicate, `S` its subject, and `M` the middle term.
A three-letter mood is `QRT`: for example, `EIO` means
`E(P,M), I(S,M) ⟹ O(S,P)`.

| Policy | Eligible supports | Valid moods |
|---|---:|---|
| Empty term extensions allowed; universe nonempty | 255 | EAE, AEE, EIO, AOO |
| P, M and S all nonempty | 218 | EAE, AEE, EIO, AOO, EAO, AEO |
| Only S required nonempty (diagnostic policy) | 240 | EAE, AEE, EIO, AOO, EAO, AEO |

There are **no valid A or I conclusions** in the fixed `T(S,P)` direction in any
of these policies. Every one of the 16 premise pairs is satisfiable, so these
results do not come from inconsistent premises.

**Direction trap:** `I(P,M), E(S,M)` entails `O(P,S)`, **not** `O(S,P)`.
The reversed conclusion is not counted as an `IEO` second-figure mood here.

## Run it

Requires Python **3.10 or newer**, no installation, network, datasets, GPU or
third-party packages. From this directory:

```bash
python second_figure.py
python second_figure.py --json report.json --markdown REPORT.md
python -m unittest -v test_second_figure
python run_verification.py
```

The last command regenerates both reports, runs the actual test suite normally,
with `-O`, and with `-OO`, and saves commands, output, exit codes, environment and
file hashes. It clears inherited `PYTHONOPTIMIZE` so the normal run is genuinely
unoptimized. No production validation uses Python's removable `assert` statement.

The model enumerates only 255 supports; this is deliberately a low-cost logical
experiment, not model training. Read [VERIFICATION.md](VERIFICATION.md) for actual
measured test results rather than an assumed pass.

## The four sentence types

For term extensions X and Y:

| Type | Formula | Reading |
|---|---|---|
| A(X,Y) | X ⊆ Y | Every X is Y |
| E(X,Y) | X ∩ Y = ∅ | No X is Y |
| I(X,Y) | X ∩ Y ≠ ∅ | Some X is Y |
| O(X,Y) | X ∖ Y ≠ ∅ | Some X is not Y |

A and E have **no built-in existential import**. Existence is imposed separately
by a policy. In particular, all-empty terms in a one-object universe satisfy
every A and E clause and falsify every I and O clause.

## Read the outputs

- [REPORT.md](REPORT.md): all **16 premise pairs × 4 conclusions** for each policy.
  An invalid cell records the size and occupied atoms of a smallest countermodel.
- [report.json](report.json): all **192 mood-policy results**, including named
  concrete countermodels, premise-support counts, and IE reversal checks.
- [WALKTHROUGH.md](WALKTHROUGH.md): encoding, four direct validity arguments,
  existence effects, countermodel examples, and the support-compression argument.
- `second_figure.py`: model, public APIs, report generation, CLI.
- `test_second_figure.py`: set-based oracle, complete classification, witnesses,
  minimality, compression, malformed inputs, vacuity and CLI regression tests.
- `run_verification.py`, `logs/`, [VERIFICATION.md](VERIFICATION.md): reproducible
  execution and the genuine captured verification record.

An atom is a membership type `(P,M,S)`, encoded as `4P + 2M + S`.
A support is an integer mask from 1 to 255: bit `a` says atom `a` is occupied.
For example, atoms `[5,6]` mean one object of type `(1,0,1)` and one of type
`(1,1,0)`; the support mask is `2**5 + 2**6 = 96`.

“Smallest” means **fewest universe elements** under that policy. Ties are broken
by the numeric support mask, not by a claimed naturalness of the example. Each
occupied atom gets one object `x1`, `x2`, …, in atom order. The JSON stores both
the concrete extensions and their support encoding. All invalid cases have a
countermodel of size at most two when empty terms are allowed, and at most three
when all terms must be nonempty.

## API examples

```python
from second_figure import (
    Clause, Policy, classify, classify_mood, compress_model,
    concrete_model, evaluate_categorical, holds, iter_supports,
)

classify_mood("EIO").valid                         # True
classify_mood("EAO").valid                         # False
classify_mood("EAO", Policy.SUBJECT_NONEMPTY).valid # True

forward = classify_mood("IEO", Policy.ALL_NONEMPTY)
forward.valid                                     # False
forward.countermodel_support                      # 96
concrete_model(96)
# {'universe': ['x1', 'x2'], 'P': ['x1', 'x2'],
#  'M': ['x2'], 'S': ['x1']}

reverse = classify(
    (Clause("I", "P", "M"), Clause("E", "S", "M")),
    Clause("O", "P", "S"),
    Policy.ALL_NONEMPTY,
)
reverse.valid                                     # True

compress_model({"a", "b"}, {"a", "b"}, {"a"}, {"b"})  # 96
holds(96, "O", "S", "P")                          # False
evaluate_categorical("O", {"a", "b"}, {"b"})       # True
len(list(iter_supports(Policy.ALL_NONEMPTY)))       # 218
```

`classify` accepts any finite iterable of validated `Clause` objects; an empty
premise list means no assumptions. It reports `vacuous=True` when no eligible
support satisfies the premises. Inputs are strict: uppercase AEIO/PMS only,
known policy names, nonempty-universe masks 1..255 (booleans rejected), and term
extensions contained in the supplied universe. Invalid values raise
`ValueError`; inappropriate types raise `TypeError`. Finite set inputs must have
hashable elements; arbitrary iterables are assumed to terminate.

## What this does—and does not—establish

The software **actually tests finite supports**, not infinitely many domains.
The separate mathematical preservation argument explains why support exhaustion
is sufficient for the chosen three-unary-predicate AEIO language, including
models with infinite universes. That argument is not a machine-checked theorem.
Tests check the implementation; they do not prove its correctness merely by
being numerous.

This package does not resolve historical disputes about existential import,
formalize Aristotle's natural-language syntax, model modality, reproduce every
proof transformation in I.5, or infer historical influence on modern AI. It keeps
modern semantic consequences separate from claims about the original text.
