#!/usr/bin/env python3
"""Independent audit oracle: actual sets and direct quantifiers, no production masks.

Run from any working directory with Python 3.10+ and no dependencies.
The only production import is the implementation being tested. Every expected
truth value, witness, support, argument result, and example is computed below.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import FrozenInstanceError
import importlib.util
from itertools import product
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("euler_cv_under_audit", ROOT / "euler_cv.py")
impl = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = impl
spec.loader.exec_module(impl)

NAMES = ("A", "B", "C")
# Boolean triples are member(A), member(B), member(C); not binary strings.
REGIONS = tuple(product((False, True), repeat=3))
CLAIMS = tuple(product("AEIO", NAMES, NAMES))
FORMS = {
    "valid": (("E", "A", "B"), ("I", "B", "C"), ("O", "C", "A")),
    "invalid": (("I", "A", "B"), ("E", "B", "C"), ("O", "C", "A")),
    "corrected": (("I", "A", "B"), ("E", "B", "C"), ("O", "A", "C")),
}
METRICS = Counter()


def type_number(region):
    a, b, c = region
    return int(a) + 2 * int(b) + 4 * int(c)


def structure(assignment, canonical=False):
    """Build an independent universe and three actual sets from booleans."""
    labels = [f"t{type_number(row)}" if canonical else f"x{i}" for i, row in enumerate(assignment)]
    universe = frozenset(labels)
    classes = {
        name: frozenset(label for label, row in zip(labels, assignment) if row[column])
        for column, name in enumerate(NAMES)
    }
    return universe, classes


def expected_support(universe, classes):
    occupied = {type_number(tuple(x in classes[name] for name in NAMES)) for x in universe}
    return sum(2 ** index for index in occupied)


def holds(claim, universe, classes):
    kind, subject, predicate = claim
    xset, yset = classes[subject], classes[predicate]
    if kind == "A":
        return all(x not in xset or x in yset for x in universe)
    if kind == "E":
        return all(not (x in xset and x in yset) for x in universe)
    if kind == "I":
        return any(x in xset and x in yset for x in universe)
    if kind == "O":
        return any(x in xset and x not in yset for x in universe)
    raise ValueError(kind)


def witnesses(claim, universe, classes):
    kind, subject, predicate = claim
    if kind not in ("I", "O"):
        raise ValueError(kind)
    return frozenset(x for x in universe if x in classes[subject] and
                     ((x in classes[predicate]) if kind == "I" else (x not in classes[predicate])))


def serialize(universe, classes):
    occupied = sorted({type_number(tuple(x in classes[name] for name in NAMES)) for x in universe})
    return {"U": sorted(universe), **{name: sorted(classes[name]) for name in NAMES},
            "support": sum(2 ** index for index in occupied), "occupied_types": occupied}


def compare_model(actual, universe, classes, reduce=True):
    assert actual.universe == universe
    for name in NAMES:
        assert actual.term(name) == classes[name]
    assert actual.support() == expected_support(universe, classes)
    assert actual.all_classes_nonempty() == all(bool(classes[name]) for name in NAMES)
    assert actual.as_dict() == serialize(universe, classes)
    mapping = {x: f"t{type_number(tuple(x in classes[name] for name in NAMES))}" for x in universe}
    assert impl.representatives(actual) == mapping
    for x in universe:
        assert actual.atom(x) == type_number(tuple(x in classes[name] for name in NAMES))
    reduced = impl.from_support(expected_support(universe, classes)) if reduce else None
    if reduced is not None:
        assert set(mapping.values()) == reduced.universe
    for claim in CLAIMS:
        proposition = impl.Proposition(*claim)
        expected = holds(claim, universe, classes)
        assert proposition.holds(actual) is expected, (claim, universe, classes)
        METRICS["direct_quantifier_truth_comparisons"] += 1
        if reduced is not None:
            assert proposition.holds(reduced) is expected
            METRICS["reduced_truth_comparisons"] += 1
        if claim[0] in ("I", "O"):
            expected_witnesses = witnesses(claim, universe, classes)
            assert proposition.witnesses(actual) == expected_witnesses
            METRICS["exact_witness_set_comparisons"] += 1
            if reduced is not None:
                assert proposition.witnesses(reduced) == {mapping[x] for x in expected_witnesses}
                METRICS["reduced_witness_image_comparisons"] += 1
    for argument in impl.ARGUMENTS:
        expected = tuple(holds(claim, universe, classes) for claim in FORMS[argument.name])
        assert argument.statuses(actual) == expected
        assert argument.countermodel(actual) is (expected[0] and expected[1] and not expected[2])
        METRICS["argument_status_and_countermodel_comparisons"] += 1


def expected_summary(name, data, nonempty):
    chosen = [(support, universe, classes) for support, (universe, classes) in sorted(data.items())
              if not nonempty or all(classes.values())]
    stats = [(support, universe, tuple(holds(p, universe, classes) for p in FORMS[name]))
             for support, universe, classes in chosen]
    bad = [(support, universe) for support, universe, truth in stats if truth[0] and truth[1] and not truth[2]]
    formula = " & ".join(f"{p[0]}({p[1]},{p[2]})" for p in FORMS[name][:2])
    p = FORMS[name][2]
    formula += f" => {p[0]}({p[1]},{p[2]})"
    return {
        "argument": formula,
        "all_classes_nonempty": nonempty,
        "total_support_models": len(stats),
        "premise_models": sum(truth[0] and truth[1] for _, _, truth in stats),
        "countermodels": len(bad),
        "valid_on_support_models": not bad,
        "false_conclusion_models": sum(not truth[2] for _, _, truth in stats),
        "false_conclusion_and_true_premises": len(bad),
        "minimal_countermodel_size": min((len(universe) for _, universe in bad), default=None),
        "countermodel_supports": [support for support, _ in bad],
    }


def expect_error(error_type, action):
    try:
        action()
    except error_type:
        METRICS["expected_input_errors"] += 1
    else:
        raise AssertionError(f"Expected {error_type.__name__}")


def malformed_and_edges():
    class IntegerSubclass(int):
        pass
    for value in (0, -1, 256, 999, True, False, 1.0, "1", None, [], {}, IntegerSubclass(1)):
        expect_error(ValueError, lambda value=value: impl.from_support(value))
    expect_error(ValueError, lambda: impl.Model([], [], [], []))
    expect_error(ValueError, lambda: impl.Model({"x"}, {"outside"}, set(), set()))
    expect_error(ValueError, lambda: impl.Model({"x"}, set(), {"outside"}, set()))
    expect_error(ValueError, lambda: impl.Model({"x"}, set(), set(), {"outside"}))
    expect_error(TypeError, lambda: impl.Model({1}, set(), set(), set()))
    expect_error(TypeError, lambda: impl.Model(None, set(), set(), set()))
    singleton = impl.Model({"x"}, set(), set(), set())
    for name in ("D", "a", "", None, 1):
        expect_error(ValueError, lambda name=name: singleton.term(name))
        expect_error(ValueError, lambda name=name: impl.Proposition("I", name, "A"))
        expect_error(ValueError, lambda name=name: impl.Proposition("I", "A", name))
    for kind in ("X", "i", "", None, 1):
        expect_error(ValueError, lambda kind=kind: impl.Proposition(kind, "A", "B"))
    expect_error(ValueError, lambda: singleton.atom("absent"))
    for kind in ("A", "E"):
        expect_error(ValueError, lambda kind=kind: impl.Proposition(kind, "A", "B").witnesses(singleton))
    universe, a = {"x"}, {"x"}
    frozen = impl.Model(universe, a, set(), set())
    universe.add("y")
    a.clear()
    assert frozen.universe == {"x"} and frozen.a == {"x"}
    expect_error(FrozenInstanceError, lambda: setattr(frozen, "a", frozenset()))
    # Empty labels are legitimate string labels; identity, not typography, matters.
    odd_u = {"", "对象", "a b"}
    odd_sets = {"A": {""}, "B": {"对象"}, "C": {"a b"}}
    compare_model(impl.Model(odd_u, *odd_sets.values()), odd_u, odd_sets)


def main():
    assert impl.TERMS == NAMES
    assert tuple(argument.name for argument in impl.ARGUMENTS) == ("valid", "invalid", "corrected")
    assert impl.ARGUMENTS == (impl.VALID, impl.INVALID, impl.CORRECTED)
    # Independent support enumeration: all nonempty selections of boolean triples.
    data = {}
    for flags in product((False, True), repeat=8):
        occupied = tuple(region for region, present in zip(REGIONS, flags) if present)
        if not occupied:
            continue
        universe, classes = structure(occupied, canonical=True)
        support = expected_support(universe, classes)
        assert support not in data
        data[support] = universe, classes
        compare_model(impl.from_support(support), universe, classes)
        METRICS["support_models"] += 1
    assert set(data) == set(range(1, 256))
    for nonempty in (False, True):
        expected = [serialize(*data[support]) for support in sorted(data)
                    if not nonempty or all(data[support][1].values())]
        assert [m.as_dict() for m in impl.models(nonempty)] == expected
    # Repeated-region assignments include every labeled structure of sizes 1..4.
    for size in range(1, 5):
        for assignment in product(REGIONS, repeat=size):
            universe, classes = structure(assignment)
            compare_model(impl.Model(universe, *(classes[name] for name in NAMES)), universe, classes)
            METRICS["labeled_models"] += 1
    examples = {
        "valid_remainder_disjoint_A": ({"w", "r", "a"}, {"a"}, {"w"}, {"w", "r"}),
        "valid_remainder_subset_A": ({"w", "r"}, {"r"}, {"w"}, {"w", "r"}),
        "valid_remainder_mixed_A": ({"w", "r", "q"}, {"r"}, {"w"}, {"w", "r", "q"}),
        "invalid_countermodel_nonempty": ({"s", "v"}, {"s", "v"}, {"s"}, {"v"}),
        "invalid_true_conclusion_alternative": ({"s", "v"}, {"s"}, {"s"}, {"v"}),
        "valid_both_premises_false_conclusion_true": ({"s", "v"}, {"s"}, {"s"}, {"v"}),
        "valid_no_remainder": ({"a", "w"}, {"a"}, {"w"}, {"w"}),
    }
    actual_examples = impl.named_examples()
    assert set(actual_examples) == set(examples)
    expected_examples = {}
    for name, values in examples.items():
        universe, classes = values[0], dict(zip(NAMES, values[1:]))
        compare_model(actual_examples[name], universe, classes)
        argname = "invalid" if name.startswith("invalid_") else "valid"
        expected_examples[name] = {
            **serialize(universe, classes),
            "argument": expected_summary(argname, data, False)["argument"],
            "truth_statuses": [holds(p, universe, classes) for p in FORMS[argname]],
            "conclusion_witnesses": sorted(witnesses(FORMS[argname][2], universe, classes)),
        }
    expected_results = {}
    for key, nonempty, total, premises, counter in (
        ("empty_classes_allowed", False, 255, 32, 16),
        ("all_classes_nonempty", True, 218, 24, 8),
    ):
        expected_results[key] = {}
        for argument in impl.ARGUMENTS:
            result = expected_summary(argument.name, data, nonempty)
            assert result["total_support_models"] == total
            assert result["premise_models"] == premises
            assert result["countermodels"] == (counter if argument.name == "invalid" else 0)
            assert impl.check(argument, nonempty) == result
            expected_results[key][argument.name] = result
    expected_report = {"results": expected_results, "examples": expected_examples}
    assert impl.report() == expected_report
    json_run = subprocess.run([sys.executable, str(ROOT / "euler_cv.py"), "--json"],
                              check=True, text=True, capture_output=True)
    assert json.loads(json_run.stdout) == expected_report
    text_run = subprocess.run([sys.executable, str(ROOT / "euler_cv.py")],
                              check=True, text=True, capture_output=True)
    assert text_run.stdout == impl.text_report(expected_report) + "\n"
    for key, contents in (("report.json", json_run.stdout), ("report.txt", text_run.stdout)):
        assert (ROOT / "logs" / key).read_text(encoding="utf-8") == contents
    malformed_and_edges()
    print(json.dumps({"status": "PASS", "metrics": dict(METRICS), "results": expected_results,
                      "checks": ["all 36 AEIO predicates including same-term cases",
                                 "exact witnesses and quotient witness images",
                                 "all report fields, full countermodel lists, examples, CLI, saved reports",
                                 "invalid inputs, mutable-input freezing, empty and Unicode string labels"],
                      "scope": "Three stated arguments only; finite checks do not replace the general reduction proof."},
                     indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
