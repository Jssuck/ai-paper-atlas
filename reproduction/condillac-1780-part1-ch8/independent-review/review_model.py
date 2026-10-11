"""Independent finite audit. Standard library only; never changes model.py.

Oracle uses integer valuations, explicit affect truth sets and counterexample
bitmasks. It does not call production properties to obtain expected values.
Semantic mismatches have exit status 1; execution/harness failures have status 2.
"""
from collections import Counter
from dataclasses import FrozenInstanceError
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
DEFAULT_MODEL = HERE.parent / "model.py"
AFFECT_FIELDS = ("lacking", "known", "habitual_enjoyment", "habitual_imagination",
                 "faculties_directed", "desire_habit")
# Six bits in AFFECT_FIELDS order. These sets are independently enumerated.
VALID_AFFECT = frozenset((0, 1, 2, 3, 6, 7, 10, 11, 14, 15, 16, 17, 18, 19,
                         22, 23, 26, 27, 30, 31, 32, 33, 34, 35, 38, 39, 42,
                         43, 46, 47, 48, 49, 50, 51, 54, 55, 58, 59, 62, 63))
DEPRIVED = frozenset((7, 11, 15, 23, 27, 31, 39, 43, 47, 55, 59, 63))
DESIRING = frozenset((23, 27, 31, 55, 59, 63))
PASSION_ACTIVE = frozenset((55, 59, 63))
TRUTH_PAIRS = ((False, False), (False, True), (True, False), (True, True))


class AuditFailure(Exception):
    """A returned value or explicit contract disagreed with the oracle."""


def check(condition, label):
    if not condition:
        raise AuditFailure(label)


def equal(actual, expected, label):
    if actual != expected:
        raise AuditFailure(f"{label}: expected {expected!r}; got {actual!r}")


def rejected(expected_exception, call, label):
    try:
        call()
    except expected_exception:
        return
    except Exception as error:
        # An unrelated crash is not evidence of successfully enforcing a rule.
        raise RuntimeError(f"unexpected exception at {label}: {type(error).__name__}") from error
    raise AuditFailure(f"accepted invalid input: {label}")


def expected_labels(affect_bits, habit_bits, valuations, support_bits, actual_index):
    # World encodings 0/1 lack obtains; 0/2 have an obstacle. Locate explicit
    # counterexamples; no production predicates or judgment method are called.
    obtain_counterexamples = sum(1 << i for i, v in enumerate(valuations) if v in (0, 1))
    obstacle_counterexamples = sum(1 << i for i, v in enumerate(valuations) if v in (0, 2))
    bridge_counterexamples = sum(1 << i for i, v in enumerate(valuations) if v == 1)
    obtains_judgment = (support_bits & obtain_counterexamples) == 0
    clear_judgment = (support_bits & obstacle_counterexamples) == 0
    desire = affect_bits in DESIRING
    need = affect_bits in DEPRIVED
    # Tabulated rows rather than calling the corresponding implementation.
    hope_row = (False, False, False, True)[2 * int(desire) + int(obtains_judgment)]
    will_row = (False, False, False, False, False, False, False, True)[
        4 * int(desire) + 2 * int(habit_bits == 3) + int(clear_judgment)]
    return {
        "objective_lack": bool(affect_bits & 1),
        "deprivation": need,
        "deprivation_suffering": need,
        "need": need,
        "desire": desire,
        "passion_disposition": affect_bits >= 32,
        "passion_active": affect_bits in PASSION_ACTIVE,
        "judges_obtaining": obtains_judgment,
        "judges_no_obstacle": clear_judgment,
        "experience_backed_habit": habit_bits == 3,
        "hope": hope_row,
        "narrow_will": will_row,
        "actual_obtaining": valuations[actual_index] in (2, 3),
        "actual_no_obstacle": valuations[actual_index] in (1, 3),
        "actual_in_support": bool(support_bits & (1 << actual_index)),
        "bridge_holds_on_support": (support_bits & bridge_counterexamples) == 0,
    }


def audit(target):
    initial = target.read_bytes()
    spec = importlib.util.spec_from_file_location("independent_target", target)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    counts = Counter()
    affects = {}
    for bits in range(64):
        values = tuple(bool(bits & (1 << i)) for i in range(6))
        if bits in VALID_AFFECT:
            a = mod.Affect(*values)
            affects[bits] = a
            for label, expected in (("deprivation", bits in DEPRIVED), ("need", bits in DEPRIVED),
                                    ("desire", bits in DESIRING),
                                    ("passion_disposition", bits >= 32),
                                    ("passion_active", bits in PASSION_ACTIVE)):
                equal(getattr(a, label), expected, f"affect {bits} {label}")
            counts["valid_affect_rows"] += 1
        else:
            rejected(ValueError, lambda values=values: mod.Affect(*values), f"affect {bits}")
            counts["rejected_affect_rows"] += 1
    habits = {bits: mod.JudgmentHabit(bool(bits & 1), bool(bits & 2)) for bits in range(4)}
    for bits, habit in habits.items():
        equal(habit.experience_backed, bits == 3, f"habit {bits}")
        counts["habit_rows"] += 1

    def make_worlds(valuations, names):
        return tuple(mod.World(name, *TRUTH_PAIRS[v]) for name, v in zip(names, valuations))

    def compare_all(valuations, names, category):
        worlds = make_worlds(valuations, names)
        for support_bits in range(1, 1 << len(names)):
            support = frozenset(names[i] for i in range(len(names)) if support_bits & (1 << i))
            for actual_index, actual in enumerate(names):
                b = mod.Beliefs(worlds, support, actual)
                for a_bits, a in affects.items():
                    for h_bits, h in habits.items():
                        got = mod.evaluate(a, b, h)
                        want = expected_labels(a_bits, h_bits, valuations, support_bits, actual_index)
                        check(type(got) is dict, "evaluate returns dict")
                        equal(set(got), set(want), "exact label schema")
                        check(all(type(x) is bool for x in got.values()), "all labels are bool")
                        equal(got, want, f"{category}: affect={a_bits}, habit={h_bits}, "
                                        f"worlds={valuations}, support={support_bits}, actual={actual_index}")
                        counts[category] += 1
    names = ("zeta", "alpha", "omega", "delta")
    compare_all((0, 1, 2, 3), names, "four_world_complete_label_cases")
    # Exhaustive three-world truth assignments include repeated valuations,
    # covering distinct world identities with indistinguishable predicate values.
    for valuations in itertools.product(range(4), repeat=3):
        compare_all(valuations, ("looks_successful", "looks_obstructed", "中"),
                    "three_world_complete_label_cases")

    worlds = make_worlds((0, 1, 2, 3), names)
    full = frozenset(names)
    desire = affects[23]
    grounded = habits[3]
    # Neither tuple order nor identity spelling may change extensional truth.
    for perm in itertools.permutations(worlds):
        for support_bits in range(1, 16):
            support = frozenset(names[i] for i in range(4) if support_bits & (1 << i))
            for actual_index, actual in enumerate(names):
                got = mod.evaluate(desire, mod.Beliefs(perm, support, actual), grounded)
                equal(got, expected_labels(23, 3, (0, 1, 2, 3), support_bits, actual_index),
                      "world-order invariance")
                counts["world_order_cases"] += 1

    for universe_bits in range(1, 16):
        selected = tuple(worlds[i] for i in range(4) if universe_bits & (1 << i))
        for support_bits in range(1, 16):
            if support_bits & ~universe_bits:
                continue
            support = frozenset(names[i] for i in range(4) if support_bits & (1 << i))
            for actual_index in range(4):
                if not universe_bits & (1 << actual_index):
                    continue
                got = mod.evaluate(desire, mod.Beliefs(selected, support, names[actual_index]), grounded)
                equal(got, expected_labels(23, 3, (0, 1, 2, 3), support_bits, actual_index),
                      "proper-world-universe subset")
                counts["world_universe_cases"] += 1

    for support_bits in range(1, 16):
        support = frozenset(names[i] for i in range(4) if support_bits & (1 << i))
        for actual in names:
            b = mod.Beliefs(worlds, support, actual)
            before = mod.evaluate(desire, b, grounded)
            for retained_bits in range(1, 16):
                retained = frozenset(names[i] for i in range(4) if retained_bits & (1 << i))
                if retained_bits & ~support_bits:
                    rejected(ValueError, lambda retained=retained: b.restrict(retained), "expansion")
                    counts["rejected_expansions"] += 1
                    continue
                r = b.restrict(retained)
                equal(r.worlds, b.worlds, "restriction retains universe")
                equal(r.actual, b.actual, "restriction retains actuality")
                equal(r.support, retained, "restriction exact support")
                after = mod.evaluate(desire, r, grounded)
                for key in ("judges_obtaining", "judges_no_obstacle", "hope", "narrow_will",
                            "bridge_holds_on_support"):
                    check(not before[key] or after[key], f"restriction monotonicity {key}")
                    counts["restriction_monotonicity_label_cases"] += 1
                for key in ("actual_obtaining", "actual_no_obstacle"):
                    equal(after[key], before[key], f"actuality after evidence {key}")
                counts["valid_restrictions"] += 1
            rejected(ValueError, lambda: b.restrict(frozenset()), "contradictory evidence")
            counts["rejected_empty_restrictions"] += 1
            if actual in support:
                for key, actual_key in (("judges_obtaining", "actual_obtaining"),
                                        ("judges_no_obstacle", "actual_no_obstacle")):
                    check(not before[key] or before[actual_key], f"conditional factivity {key}")
                    counts["factivity_predicate_cases"] += 1
            if before["bridge_holds_on_support"] and before["narrow_will"]:
                check(before["hope"], "bridge licenses will-to-hope")
                counts["nonvacuous_bridge_implication_cases"] += 1

    # Directed witnesses establish that one-way results are not overclaimed.
    false_confidence = mod.evaluate(desire, mod.Beliefs(worlds, frozenset([names[3]]), names[0]), grounded)
    check(false_confidence["hope"] and false_confidence["narrow_will"] and
          not false_confidence["actual_obtaining"] and not false_confidence["actual_in_support"],
          "false confidence witness")
    no_bridge = mod.evaluate(desire, mod.Beliefs(worlds, frozenset([names[1]]), names[0]), grounded)
    check(no_bridge["narrow_will"] and not no_bridge["hope"], "will without hope witness")
    hoped = mod.evaluate(desire, mod.Beliefs(worlds, frozenset([names[2]]), names[0]), grounded)
    check(hoped["hope"] and not hoped["narrow_will"], "hope without will witness")
    uncertain = mod.Beliefs(worlds, frozenset([names[0], names[3]]), names[0])
    check(not uncertain.judges("obtains") and uncertain.restrict(frozenset([names[3]])).judges("obtains"),
          "restriction may create categorical judgment")
    latent = mod.evaluate(affects[32], uncertain, habits[0])
    check(latent["passion_disposition"] and not latent["passion_active"] and not latent["desire"],
          "latent passion witness")
    counts["directed_counterexamples"] = 5

    bad_bool = (0, 1, -1, None, "", "true", [], {}, 0.0, object())
    for field in AFFECT_FIELDS:
        for bad in bad_bool:
            rejected(TypeError, lambda field=field, bad=bad: mod.Affect(**{field: bad}), f"Affect.{field}")
            counts["invalid_api_inputs"] += 1
    for field in ("established", "from_experience"):
        for bad in bad_bool:
            rejected(TypeError, lambda field=field, bad=bad: mod.JudgmentHabit(**{field: bad}), f"Habit.{field}")
            counts["invalid_api_inputs"] += 1
    for field in ("obtains", "obstacle_free"):
        for bad in bad_bool:
            kwargs = {"name": "x", "obtains": True, "obstacle_free": True, field: bad}
            rejected(TypeError, lambda kwargs=kwargs: mod.World(**kwargs), f"World.{field}")
            counts["invalid_api_inputs"] += 1
    for bad in ("", 1, None, [], object()):
        rejected(ValueError, lambda bad=bad: mod.World(bad, True, True), "world name")
        counts["invalid_api_inputs"] += 1
    valid_b = mod.Beliefs(worlds, full, names[0])
    invalid_calls = [
        (TypeError, lambda: mod.Beliefs(list(worlds), full, names[0]), "worlds list"),
        (TypeError, lambda: mod.Beliefs(("fake",), full, names[0]), "non-World member"),
        (TypeError, lambda: mod.Beliefs(None, full, names[0]), "worlds None"),
        (TypeError, lambda: mod.Beliefs(worlds, set(names), names[0]), "support set"),
        (TypeError, lambda: mod.Beliefs(worlds, tuple(names), names[0]), "support tuple"),
        (TypeError, lambda: mod.Beliefs(worlds, None, names[0]), "support None"),
        (ValueError, lambda: mod.Beliefs((), frozenset(["x"]), "x"), "empty universe"),
        (ValueError, lambda: mod.Beliefs((worlds[0], worlds[0]), frozenset([names[0]]), names[0]), "duplicate world"),
        (ValueError, lambda: mod.Beliefs((worlds[0], mod.World(names[0], True, True)), frozenset([names[0]]), names[0]), "duplicate conflicting world"),
        (ValueError, lambda: mod.Beliefs(worlds, frozenset(), names[0]), "empty support"),
        (ValueError, lambda: mod.Beliefs(worlds, frozenset(["missing"]), names[0]), "unknown support"),
        (ValueError, lambda: mod.Beliefs(worlds, frozenset([1]), names[0]), "non-string support"),
        (ValueError, lambda: mod.Beliefs(worlds, full, "missing"), "unknown actual"),
        (ValueError, lambda: mod.Beliefs(worlds, full, None), "non-string actual"),
        (TypeError, lambda: valid_b.restrict(set(names)), "restriction set"),
        (TypeError, lambda: valid_b.restrict(None), "restriction None"),
        (ValueError, lambda: valid_b.restrict(frozenset(["missing"])), "restriction unknown"),
        (TypeError, lambda: mod.evaluate({}, valid_b, grounded), "evaluate affect type"),
        (TypeError, lambda: mod.evaluate(desire, {}, grounded), "evaluate beliefs type"),
        (TypeError, lambda: mod.evaluate(desire, valid_b, {}), "evaluate habit type"),
    ]
    for predicate in ("", "probability", "name", "__class__", None, 1, []):
        invalid_calls.append((ValueError, lambda predicate=predicate: valid_b.judges(predicate), "judges predicate"))
        invalid_calls.append((ValueError, lambda predicate=predicate: valid_b.actually(predicate), "actually predicate"))
    for kind, call, label in invalid_calls:
        rejected(kind, call, label)
        counts["invalid_api_inputs"] += 1
    for value, field, replacement in ((desire, "lacking", False), (grounded, "established", False),
                                      (worlds[0], "obtains", True), (valid_b, "actual", names[3])):
        rejected(FrozenInstanceError, lambda value=value, field=field, replacement=replacement:
                 setattr(value, field, replacement), "frozen dataclass")
        counts["immutability_cases"] += 1
    equal(target.read_bytes(), initial, "production code unchanged during run")
    return {"status": "PASS", "optimization": sys.flags.optimize,
            "source_sha256": hashlib.sha256(initial).hexdigest(),
            "review_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "counts": dict(sorted(counts.items())),
            "scope": "Finite explicit affect table, all 4-world supports/actualities, all 3-world truth assignments; no empirical or historical-algorithm claim."}


def main():
    target = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else DEFAULT_MODEL
    if len(sys.argv) > 2:
        raise ValueError("usage: review_model.py [model.py]")
    try:
        result = audit(target)
    except AuditFailure as error:
        print(json.dumps({"status": "SEMANTIC_FAILURE", "detail": str(error),
                          "optimization": sys.flags.optimize}, ensure_ascii=False))
        return 1
    except Exception as error:
        print(json.dumps({"status": "HARNESS_FAILURE", "exception": type(error).__name__,
                          "detail": str(error), "optimization": sys.flags.optimize}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
