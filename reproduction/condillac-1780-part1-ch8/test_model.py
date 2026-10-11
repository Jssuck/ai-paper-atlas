"""Deterministic finite checks; unittest checks survive -O and -OO."""
import itertools
import json
import sys
import unittest

from model import Affect, Beliefs, JudgmentHabit, World, evaluate

WORLDS = (
    World("failure_obstacle", False, False),
    World("failure_clear", False, True),
    World("success_obstacle", True, False),
    World("success_clear", True, True),
)
NAMES = tuple(w.name for w in WORLDS)
DESIRE = Affect(True, True, False, True, True)
GROUNDED = JudgmentHabit(True, True)


def subsets(names, nonempty=True):
    return tuple(frozenset(part) for n in range(int(nonempty), len(names) + 1)
                 for part in itertools.combinations(names, n))


def beliefs(*support, actual="failure_obstacle"):
    return Beliefs(WORLDS, frozenset(support), actual)


class ModelTests(unittest.TestCase):
    def test_01_boolean_inputs_are_strict(self):
        for name in Affect.__dataclass_fields__:
            with self.subTest(field=name), self.assertRaises(TypeError):
                Affect(**{name: 1})
        for name in JudgmentHabit.__dataclass_fields__:
            with self.subTest(field=name), self.assertRaises(TypeError):
                JudgmentHabit(**{name: "yes"})

    def test_02_pleasure_context_requires_known_object(self):
        for fields in ({"habitual_enjoyment": True}, {"habitual_imagination": True}):
            with self.assertRaises(ValueError):
                Affect(**fields)

    def test_03_unknown_objective_lack_is_not_need(self):
        a = Affect(lacking=True)
        self.assertTrue(a.lacking)
        self.assertFalse(a.deprivation)
        self.assertFalse(a.need)

    def test_04_known_but_unvalued_lack_is_not_need(self):
        self.assertFalse(Affect(lacking=True, known=True).need)

    def test_05_habitual_imagination_needs_no_past_enjoyment(self):
        a = Affect(lacking=True, known=True, habitual_imagination=True)
        self.assertFalse(a.habitual_enjoyment)
        self.assertTrue(a.deprivation)
        self.assertTrue(a.need)

    def test_06_habitual_enjoyment_is_another_path(self):
        a = Affect(lacking=True, known=True, habitual_enjoyment=True)
        self.assertFalse(a.habitual_imagination)
        self.assertTrue(a.need)

    def test_07_present_object_is_not_deprivation(self):
        for enjoyed, imagined in itertools.product((False, True), repeat=2):
            self.assertFalse(Affect(False, True, enjoyed, imagined).deprivation)

    def test_08_direction_is_explicit(self):
        self.assertTrue(DESIRE.desire)
        self.assertFalse(Affect(True, True, False, True, False).desire)
        self.assertFalse(Affect(faculties_directed=True).desire)

    def test_09_passion_can_be_latent(self):
        a = Affect(desire_habit=True)
        self.assertTrue(a.passion_disposition)
        self.assertFalse(a.passion_active)
        active = Affect(True, True, False, True, True, True)
        self.assertTrue(active.passion_active)

    def test_10_empty_support_is_rejected(self):
        with self.assertRaises(ValueError):
            beliefs()

    def test_11_world_universe_is_validated(self):
        for worlds, support, actual in (
            ((), frozenset(), "none"),
            ((WORLDS[0], WORLDS[0]), frozenset([NAMES[0]]), NAMES[0]),
            (WORLDS, frozenset(["missing"]), NAMES[0]),
            (WORLDS, frozenset([NAMES[0]]), "missing"),
        ):
            with self.assertRaises(ValueError):
                Beliefs(worlds, support, actual)

    def test_12_wrong_types_and_unknown_predicates_are_rejected(self):
        with self.assertRaises(TypeError):
            Beliefs(list(WORLDS), frozenset([NAMES[0]]), NAMES[0])
        with self.assertRaises(TypeError):
            Beliefs(WORLDS, set([NAMES[0]]), NAMES[0])
        b = beliefs(NAMES[0])
        with self.assertRaises(ValueError):
            b.judges("probability")
        with self.assertRaises(ValueError):
            b.actually("probability")
        with self.assertRaises(TypeError):
            evaluate({}, b, GROUNDED)

    def test_13_judgment_is_universal_not_existential(self):
        b = beliefs("success_clear", "failure_obstacle")
        self.assertFalse(b.judges("obtains"))
        self.assertFalse(b.judges("obstacle_free"))
        self.assertTrue(beliefs("success_clear").judges("obtains"))

    def test_14_hope_requires_desire(self):
        b = beliefs("success_clear")
        self.assertTrue(evaluate(DESIRE, b, GROUNDED)["hope"])
        self.assertFalse(evaluate(Affect(), b, GROUNDED)["hope"])

    def test_15_narrow_will_requires_both_habit_qualifications(self):
        b = beliefs("success_clear")
        for established, experienced in itertools.product((False, True), repeat=2):
            e = evaluate(DESIRE, b, JudgmentHabit(established, experienced))
            self.assertEqual(e["narrow_will"], established and experienced)

    def test_16_hope_does_not_require_no_obstacle(self):
        e = evaluate(DESIRE, beliefs("success_obstacle"), GROUNDED)
        self.assertTrue(e["hope"])
        self.assertFalse(e["narrow_will"])

    def test_17_no_implicit_success_bridge(self):
        e = evaluate(DESIRE, beliefs("failure_clear"), GROUNDED)
        self.assertTrue(e["narrow_will"])
        self.assertFalse(e["hope"])
        self.assertFalse(e["bridge_holds_on_support"])

    def test_18_false_confidence_is_representable(self):
        e = evaluate(DESIRE, beliefs("success_clear", actual="failure_obstacle"), GROUNDED)
        self.assertTrue(e["hope"])
        self.assertTrue(e["narrow_will"])
        self.assertFalse(e["actual_obtaining"])
        self.assertFalse(e["actual_no_obstacle"])
        self.assertFalse(e["actual_in_support"])

    def test_19_actual_in_support_gives_factivity_finite_check(self):
        count = 0
        for support in subsets(NAMES):
            for actual in support:
                b = Beliefs(WORLDS, support, actual)
                for predicate in ("obtains", "obstacle_free"):
                    if b.judges(predicate):
                        self.assertTrue(b.actually(predicate))
                    count += 1
        self.assertEqual(count, 64)

    def test_20_support_restriction_preserves_judgments_finite_check(self):
        count = 0
        for support in subsets(NAMES):
            b = Beliefs(WORLDS, support, NAMES[0])
            for smaller in subsets(tuple(sorted(support))):
                restricted = b.restrict(smaller)
                self.assertEqual(restricted.support, smaller)
                self.assertEqual(restricted.actual, b.actual)
                for predicate in ("obtains", "obstacle_free"):
                    if b.judges(predicate):
                        self.assertTrue(restricted.judges(predicate))
                    count += 1
        self.assertEqual(count, 130)

    def test_21_invalid_restriction_cannot_vacuously_validate_everything(self):
        b = beliefs("failure_obstacle")
        with self.assertRaises(ValueError):
            b.restrict(frozenset())
        with self.assertRaises(ValueError):
            b.restrict(frozenset(NAMES))
        with self.assertRaises(TypeError):
            b.restrict(set(b.support))

    def test_22_bridge_supports_will_to_hope_finite_check(self):
        count = 0
        for support in subsets(NAMES):
            b = Beliefs(WORLDS, support, NAMES[0])
            expected_bridge = all(not w.obstacle_free or w.obtains for w in WORLDS if w.name in support)
            self.assertEqual(b.obstacle_implies_obtains_on_support, expected_bridge)
            e = evaluate(DESIRE, b, GROUNDED)
            if expected_bridge and e["narrow_will"]:
                self.assertTrue(e["hope"])
            count += 1
        self.assertEqual(count, 15)

    def test_23_finite_cross_product_matches_independent_truth_table(self):
        count = 0
        for support, actual, desire_on, established, experienced in itertools.product(
            subsets(NAMES), NAMES, (False, True), (False, True), (False, True)
        ):
            a = DESIRE if desire_on else Affect()
            e = evaluate(a, Beliefs(WORLDS, support, actual), JudgmentHabit(established, experienced))
            successes = {"success_obstacle", "success_clear"}
            clear = {"failure_clear", "success_clear"}
            self.assertEqual(e["hope"], desire_on and support.issubset(successes))
            self.assertEqual(e["narrow_will"], desire_on and established and experienced and support.issubset(clear))
            self.assertEqual(e["actual_obtaining"], actual in successes)
            self.assertEqual(e["actual_no_obstacle"], actual in clear)
            count += 1
        self.assertEqual(count, 480)

    def test_24_habit_does_not_replace_current_judgment(self):
        e = evaluate(DESIRE, beliefs("success_obstacle"), GROUNDED)
        self.assertTrue(e["experience_backed_habit"])
        self.assertFalse(e["narrow_will"])

    def test_25_actual_world_does_not_silently_rewrite_support(self):
        e1 = evaluate(DESIRE, beliefs("success_clear", actual=NAMES[0]), GROUNDED)
        e2 = evaluate(DESIRE, beliefs("success_clear", actual=NAMES[3]), GROUNDED)
        for key in ("judges_obtaining", "judges_no_obstacle", "hope", "narrow_will"):
            self.assertEqual(e1[key], e2[key])
        self.assertNotEqual(e1["actual_obtaining"], e2["actual_obtaining"])

    def test_26_world_values_are_strict(self):
        with self.assertRaises(ValueError):
            World("", True, True)
        with self.assertRaises(TypeError):
            World("x", 1, True)
        with self.assertRaises(TypeError):
            World("x", True, "yes")

    def test_27_enjoyment_habit_is_not_automatically_desire_habit(self):
        a = Affect(True, True, True, False, True, False)
        self.assertTrue(a.desire)
        self.assertFalse(a.passion_disposition)
        self.assertFalse(a.passion_active)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ModelTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"tests_run": result.testsRun, "failures": len(result.failures),
              "errors": len(result.errors), "skipped": len(result.skipped),
              "successful": result.wasSuccessful(), "optimization": sys.flags.optimize,
              "finite_checks": {"factivity_predicate_cases": 64,
                                "restriction_predicate_cases": 130,
                                "bridge_supports": 15, "classification_cases": 480}}
    print(json.dumps(report, sort_keys=True))
    sys.exit(0 if result.wasSuccessful() else 1)
