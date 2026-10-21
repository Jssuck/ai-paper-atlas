# Independent implementation review

**Verdict: PASS for the stated modern AEIO semantics.** No semantic, countermodel,
minimality, or input-validation defect was found in the reviewed version. This is
a separate-agent implementation review, not an external human peer review or a
historical certification.

The final captured run completed on **2026-10-21 at 11:50:37 UTC**, using
**CPython 3.12.14 on Linux x86-64**. Both the authored suite and a newly written
independent audit passed in genuine normal, `-O`, and `-OO` interpreters. The
reviewed source and documentation did not change during those runs.

## What was reviewed

The reviewer read `second_figure.py`, every authored test in
`test_second_figure.py`, `run_verification.py`, `README.md`, `WALKTHROUGH.md`, and
the generated reports and verification record. The authored suite now contains
**41 test methods**, not the earlier intermediate total of 39.

The new [audit script](audit_second_figure.py) does **not** import the author's
test oracle. It constructs all nonempty combinations of a literal list of the
eight Boolean membership tuples, uses the tuples themselves as domain objects,
and evaluates clauses with direct set difference/intersection. It does not use
production constants, truth evaluators, support decoding, or policy filtering to
derive expected semantic answers. Arithmetic support encoding is used only at
the boundary when comparing the documented integer-mask representation.

This differs from the production bit-flag evaluator and from the authored test
oracle's scan and decoding of integer masks. It is still written in Python and
uses the same explicitly chosen mathematical semantics; it is not an independent
formalization of Aristotle's historical intentions.

## Exhaustive classification and witness results

Premises are fixed as `Q(P,M), R(S,M)` and the conclusion as `T(S,P)`.

| Policy | Eligible supports | Valid moods | Invalid moods |
|---|---:|---|---:|
| `allow-empty` | 255 | AEE, AOO, EAE, EIO | 60 |
| `all-nonempty` | 218 | AEE, AEO, AOO, EAE, EAO, EIO | 58 |
| `subject-nonempty` | 240 | AEE, AEO, AOO, EAE, EAO, EIO | 58 |

All **192 mood-policy classifications** agree with the independent enumeration.
All **176 returned concrete countermodels** have a nonempty universe, obey the
selected existence policy, satisfy both premises, and falsify the specified
conclusion. Each has the globally smallest support cardinality, with the lowest
numeric support mask among ties. This was checked against **every eligible
support**, not by trusting the production search order or a guessed witness-size
bound. Every premise pair is satisfiable under each policy; no listed valid mood
is an artifact of inconsistent premises. No affirmative A or I conclusion is
valid in this fixed direction.

The independent minimum-size histograms are:

| Policy | Size 1 | Size 2 | Size 3 |
|---|---:|---:|---:|
| `allow-empty` | 40 | 20 | 0 |
| `all-nonempty` | 8 | 44 | 6 |
| `subject-nonempty` | 32 | 26 | 0 |

All premise-support counts were independently recalculated. The full 16 counts
per policy and each mutant's actual detecting discrepancy are retained in
[results-normal.json](results-normal.json), with equivalent records for the
other two interpreter modes.

### Direction checks

The audit separately checks IE, EI, and nonconversion of O under all three
policies:

- `I(P,M), E(S,M)` entails **O(P,S)**, but not **O(S,P)**.
- `E(P,M), I(S,M)` entails **O(S,P)**, but not **O(P,S)**.
- `O(P,S)` does not entail `O(S,P)`, even with all terms nonempty.

For the failed forward IE inference, the minimum witness is mask **64**, size 1,
when empty terms are allowed, and mask **96**, size 2, for both policies requiring
S to exist. The latter realizes `P={a,b}, M={a}, S={b}`. For O nonconversion,
minimum masks are **16**, **96**, and **48** respectively under allow-empty,
all-nonempty, and subject-nonempty. These are checked witnesses, not deductions
from the mere absence of a valid mood name.

## Additional independent coverage, per interpreter mode

- **9,180 atomic cases**: 255 supports × 4 quantifiers × 3 subjects × 3 predicates,
  including repeated terms. Both production evaluation functions are checked,
  yielding **18,360 truth-function comparisons**.
- **255 occupied-support decodings**, **765 extensions**, and **765
  support-policy membership cases**, plus complete ordered policy enumeration.
- **4,680 labeled models** of sizes 1–4 (`8 + 64 + 512 + 4096`), including repeated
  membership types and objects outside all terms. Compression agrees with an
  independently calculated support and preserves **168,480 clause truths** and
  **14,040 policy predicates**. Concrete realizations are independently decoded
  rather than checked solely by a production round trip.
- **21 direction/general-entailment cases**, including contradictory premises
  and empty premise lists, checked for validity, vacuity, premise counts, policy,
  and witnesses.
- **187 malformed-input calls**: **103 expected TypeError** and **84 expected
  ValueError** outcomes. These are invalid API calls, not the 176 invalid moods.
  Cases cover booleans masquerading as masks, out-of-range masks, wrong types,
  invalid quantifiers/terms/policies/moods, bad clause inputs, empty universes,
  extensions outside the universe, noniterables, and unhashable elements.
- Every published **192 JSON mood row**, **6 JSON IE-reversal rows**, and **48
  Markdown data rows** matches checked results. The report-writing entry point
  reproduces both saved artifacts byte for byte in a temporary directory.

## Fault-injection checks

The audit deliberately changes an in-memory copy of the implementation and
runs the relevant independent checks. **All 13 targeted faulty variants were
detected; zero survived and zero were counted as detected merely because of an
unexpected crash.** No production source was mutated on disk.

1. O incorrectly treated as I.
2. E incorrectly treated as I.
3. A incorrectly given existential import.
4. S-only policy incorrectly requiring P.
5. All-nonempty policy ignored.
6. Numeric-mask search order substituted for cardinality-first order.
7. Second-figure conclusion direction reversed.
8. First premise direction reversed.
9. Last countermodel returned instead of the first/minimum.
10. Premise-support count off by one.
11. The outside-all-terms atom omitted.
12. Boolean support masks accepted.
13. Multiplicities added rather than erased during compression.

For example, numeric-only ordering returns mask **104**, a three-object witness,
for `IIE` under allow-empty, although mask **128** is a one-object countermodel.
The independent minimality check catches this specific plausible ordering bug.
Targeted mutation success establishes sensitivity to these faults; it is not a
claim that all possible bugs have been tested.

## Genuine execution record and rerun instructions

| Interpreter mode | Observed optimization | Authored tests | Independent audit | Exit codes |
|---|---:|---:|---|---|
| normal | 0 | 41 passed | PASS | 0 / 0 |
| `-O` | 1 | 41 passed | PASS | 0 / 0 |
| `-OO` | 2 | 41 passed | PASS | 0 / 0 |

These are **six actual subprocess runs**, not results inferred from the normal
run. Optimization modes repeat the same audits; they are not three different
independent semantic implementations. The audit's checks raise explicit
exceptions and do not depend on removable `assert` statements.

From the reproduction root, rerun:

```bash
python3 independent-review/run_review.py
```

The runner removes inherited `PYTHONOPTIMIZE`, sets `PYTHONHASHSEED=0` and
`PYTHONDONTWRITEBYTECODE=1`, executes the authored tests and this audit in each
mode, probes the observed optimization levels, preserves commands/output/exit
codes/timings, and checks reviewed-file hashes before and after execution.

[verification.json](verification.json) records environment, exact commands,
results, and SHA-256 identities. The `author-*.log` and `independent-*.log` files
contain captured output. Only public relative working directories are recorded;
no network, account data, or third-party dependency was used.

## Documentation assessment and resolved issue

The support-preservation argument in `WALKTHROUGH.md` is sound for the stated
language: map any nonempty domain to its occupied Boolean membership types;
AEIO truth and the three existence policies depend only on those types. This
also covers infinite original domains without selecting representatives from
infinitely many classes. Conversely, every enumerated support has the displayed
finite realization. Together these facts justify extending the finite-support
classification and smallest-witness result beyond the finite examples tested.
The argument remains prose mathematics, **not a machine-checked theorem**.

The documents correctly separate that argument, implementation tests, chosen
existence policies, and historical interpretation. They explicitly distinguish
the forward IE failure from its valid reversed conclusion.

One publication-hygiene issue was found: the first authored verification logs
included an absolute local working directory. The builder changed the logging
helper to publish portable commands/relative directories and reran its suite.
The final reviewed helper and text logs no longer contain those local paths.
Generated bytecode caches are not review deliverables and should not be included
in the public package.

## Version binding and limits

[reviewed-files.sha256](reviewed-files.sha256) binds the seven reviewed
implementation/test/helper/document/report files. In particular:

```text
second_figure.py
0381ae2f863818f3e318e27f16a1f362c553e0ef92c7502a5465f9fd2ae6d930

test_second_figure.py
652443c9cf06e2dd3f8acc462827deb39df038186fe93b7d7975c0f3a87f1698
```

**Any change to a bound file requires a rerun and refreshed review evidence.**
Do not carry this PASS to a different hash. `evidence-files.sha256` additionally
binds the review scripts, this report, and captured independent evidence, excluding
the manifest itself.

No implementation-review blockers or denied checks remain. No network-dependent
or pending test is represented as passed. Unverified scope includes other Python
versions/platforms, resource exhaustion or hostile Python objects, a formal
proof assistant, modal/relational/cardinality-sensitive extensions, and
historical fidelity or influence claims. The ordinary API assumes finite,
terminating iterables of hashable objects. This review does not certify the
surrounding article's citations or publication process.
