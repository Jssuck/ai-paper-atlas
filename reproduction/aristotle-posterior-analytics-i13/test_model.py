"""Independent membership and equation-solving oracles, plus input tests."""

from fractions import Fraction
from itertools import product
import unittest

import model


def set_oracle_report():
    """No bit masks or calls to model predicates: enumerate member choices."""
    sets = [
        frozenset(i for i, present in enumerate(flags) if present)
        for flags in product((False, True), repeat=3)
    ]

    def subset(left, right):
        return all(element in right for element in left)

    def separate(left, right):
        return all(element not in right for element in left)

    output = {"universe_size": 3, "triples": 0}
    for key in (
        "fact_chain_premises", "fact_chain_countermodels",
        "reversed_inclusion_premises", "reversed_inclusion_countermodels",
        "reversed_inclusion_nonempty_countermodels", "reciprocal_premises",
        "reciprocal_countermodels", "negative_premises", "negative_countermodels",
        "negative_with_broad_middle", "negative_with_broad_middle_all_nonempty",
    ):
        output[key] = 0
    for s, c, e in product(sets, repeat=3):
        output["triples"] += 1
        if subset(s, e) and subset(e, c):
            output["fact_chain_premises"] += 1
            output["fact_chain_countermodels"] += int(not subset(s, c))
        if subset(c, e) and subset(s, e):
            output["reversed_inclusion_premises"] += 1
            if not subset(s, c):
                output["reversed_inclusion_countermodels"] += 1
                output["reversed_inclusion_nonempty_countermodels"] += int(
                    bool(s) and bool(c) and bool(e)
                )
        if subset(c, e) and subset(e, c) and subset(s, e):
            output["reciprocal_premises"] += 1
            output["reciprocal_countermodels"] += int(not subset(s, c))
        if subset(e, c) and separate(s, c):
            output["negative_premises"] += 1
            output["negative_countermodels"] += int(not separate(s, e))
            if any(element not in e for element in c):
                output["negative_with_broad_middle"] += 1
                output["negative_with_broad_middle_all_nonempty"] += int(
                    bool(s) and bool(c) and bool(e)
                )
    return output


def scm_oracle(name, u, intervention):
    """Enumerate all candidate assignments, not topological computation."""
    solutions = []
    for x, y in product((0, 1), repeat=2):
        assignment = {"X": x, "Y": y}
        if any(assignment[var] != value for var, value in intervention.items()):
            continue
        x_equation = (x == u) if name == "X_to_Y" else (x == y)
        y_equation = (y == x) if name == "X_to_Y" else (y == u)
        if ("X" in intervention or x_equation) and (
            "Y" in intervention or y_equation
        ):
            solutions.append((x, y))
    if len(solutions) != 1:
        raise ValueError("oracle expected exactly one solution")
    return solutions[0]


class SetTests(unittest.TestCase):
    def test_predicates_against_membership_oracle(self):
        for size in range(5):
            for a, b in product(range(1 << size), repeat=2):
                left = set(i for i in range(size) if (a // (2 ** i)) % 2)
                right = set(i for i in range(size) if (b // (2 ** i)) % 2)
                with self.subTest(size=size, a=a, b=b):
                    self.assertEqual(model.included(a, b, size), left <= right)
                    self.assertEqual(model.disjoint(a, b, size), not (left & right))
                    self.assertEqual(model.members(a, size), sorted(left))

    def test_complete_counts_against_independent_set_oracle(self):
        self.assertEqual(model.finite_report(), set_oracle_report())

    def test_valid_fact_chain(self):
        self.assertTrue(model.included(1, 3))
        self.assertTrue(model.included(3, 7))
        self.assertTrue(model.included(1, 7))
        self.assertEqual(model.finite_report()["fact_chain_countermodels"], 0)

    def test_nonempty_reverse_counterexample(self):
        s, c, e = 2, 1, 3
        self.assertTrue(model.included(c, e))
        self.assertTrue(model.included(s, e))
        self.assertFalse(model.included(s, c))

    def test_reciprocal_bridge(self):
        self.assertEqual(model.finite_report()["reciprocal_countermodels"], 0)
        self.assertTrue(model.included(1, 3))
        self.assertTrue(model.included(3, 3))

    def test_reciprocity_not_necessary_for_a_particular_subject(self):
        s, c, e = 1, 1, 3
        self.assertTrue(model.included(s, e))
        self.assertTrue(model.included(s, c))
        self.assertFalse(model.included(e, c))

    def test_broad_negative_middle(self):
        w, a, b = 1, 6, 4
        self.assertTrue(model.included(b, a))
        self.assertTrue(model.disjoint(w, a))
        self.assertTrue(model.disjoint(w, b))
        self.assertFalse(model.included(a, b))
        self.assertEqual(model.members(a & ~b), [1])

    def test_negative_does_not_need_reciprocity(self):
        report = model.finite_report()
        self.assertEqual(report["negative_countermodels"], 0)
        self.assertGreater(report["negative_with_broad_middle_all_nonempty"], 0)

    def test_empty_universe_and_subject(self):
        self.assertTrue(model.included(0, 0, 0))
        self.assertTrue(model.disjoint(0, 0, 0))
        self.assertEqual(model.members(0, 0), [])
        self.assertTrue(model.included(0, 7))

    def test_maximum_supported_universe(self):
        self.assertEqual(model.members(255, 8), list(range(8)))
        self.assertTrue(model.included(128, 255, 8))

    def test_mask_types_rejected(self):
        for bad in (True, False, 1.0, "1", None, [], {}):
            for func in (model.included, model.disjoint):
                with self.subTest(bad=bad, func=func.__name__):
                    with self.assertRaises(TypeError):
                        func(bad, 0)
                    with self.assertRaises(TypeError):
                        func(0, bad)
            with self.assertRaises(TypeError):
                model.members(bad)

    def test_mask_ranges_rejected(self):
        for bad in (-1, 8, 1000):
            for func in (model.included, model.disjoint):
                with self.assertRaises(ValueError):
                    func(bad, 0)
                with self.assertRaises(ValueError):
                    func(0, bad)
            with self.assertRaises(ValueError):
                model.members(bad)
        with self.assertRaises(ValueError):
            model.members(1, 0)

    def test_size_types_rejected(self):
        for bad in (True, False, 3.0, "3", None):
            with self.assertRaises(TypeError):
                model.members(0, bad)
            with self.assertRaises(TypeError):
                model.included(0, 0, bad)
            with self.assertRaises(TypeError):
                model.disjoint(0, 0, bad)

    def test_size_range_rejected(self):
        for bad in (-1, 9, 1000):
            with self.assertRaises(ValueError):
                model.members(0, bad)


class SCMTests(unittest.TestCase):
    def test_all_responses_against_equation_oracle(self):
        checked = 0
        # Independent intervention construction, not model.intervention_grid().
        for dx, dy in product((-1, 0, 1), repeat=2):
            intervention = {}
            if dx != -1:
                intervention["X"] = dx
            if dy != -1:
                intervention["Y"] = dy
            for name, u in product(("X_to_Y", "Y_to_X"), (0, 1)):
                with self.subTest(name=name, u=u, do=intervention):
                    self.assertEqual(
                        model.evaluate(name, u, intervention),
                        scm_oracle(name, u, intervention),
                    )
                checked += 1
        self.assertEqual(checked, 36)

    def test_all_distributions_against_equation_oracle(self):
        for dx, dy in product((-1, 0, 1), repeat=2):
            intervention = {v: x for v, x in (("X", dx), ("Y", dy)) if x != -1}
            for name in ("X_to_Y", "Y_to_X"):
                expected = {p: Fraction(0) for p in product((0, 1), repeat=2)}
                for u in (0, 1):
                    expected[scm_oracle(name, u, intervention)] += Fraction(1, 2)
                self.assertEqual(model.distribution(name, intervention), expected)

    def test_same_observation(self):
        expected = {(0, 0): Fraction(1, 2), (0, 1): 0,
                    (1, 0): 0, (1, 1): Fraction(1, 2)}
        self.assertEqual(model.distribution("X_to_Y"), expected)
        self.assertEqual(model.distribution("Y_to_X"), expected)

    def test_do_x_separates_models(self):
        fwd = model.distribution("X_to_Y", {"X": 0})
        rev = model.distribution("Y_to_X", {"X": 0})
        self.assertEqual(fwd[(0, 0)], 1)
        self.assertEqual(fwd[(0, 1)], 0)
        self.assertEqual(rev[(0, 0)], Fraction(1, 2))
        self.assertEqual(rev[(0, 1)], Fraction(1, 2))
        self.assertNotEqual(fwd, rev)

    def test_do_y_separates_models(self):
        self.assertEqual(model.evaluate("X_to_Y", 0, {"Y": 1}), (0, 1))
        self.assertEqual(model.evaluate("Y_to_X", 0, {"Y": 1}), (1, 1))

    def test_joint_intervention_overwrites_both_equations(self):
        for name, u, x, y in product(model.MODELS, (0, 1), (0, 1), (0, 1)):
            self.assertEqual(model.evaluate(name, u, {"X": x, "Y": y}), (x, y))

    def test_probabilities_normalized_nonnegative_and_exact(self):
        for name, intervention in product(model.MODELS, model.intervention_grid()):
            probabilities = model.distribution(name, intervention)
            self.assertEqual(set(probabilities), {(0, 0), (0, 1), (1, 0), (1, 1)})
            self.assertEqual(sum(probabilities.values()), 1)
            for value in probabilities.values():
                self.assertIsInstance(value, Fraction)
                self.assertGreaterEqual(value, 0)

    def test_intervention_grid_is_complete_and_unique(self):
        grid = model.intervention_grid()
        self.assertEqual(len(grid), 9)
        self.assertEqual(len({tuple(sorted(d.items())) for d in grid}), 9)

    def test_input_intervention_not_mutated(self):
        intervention = {"X": 0}
        model.evaluate("X_to_Y", 1, intervention)
        model.distribution("Y_to_X", intervention)
        self.assertEqual(intervention, {"X": 0})

    def test_unknown_model_rejected(self):
        for bad in ("", "Z_to_X", "x_to_y"):
            with self.assertRaises(ValueError):
                model.evaluate(bad, 0)
            with self.assertRaises(ValueError):
                model.distribution(bad)

    def test_model_type_rejected(self):
        for bad in (None, 1, True, []):
            with self.assertRaises(TypeError):
                model.evaluate(bad, 0)
            with self.assertRaises(TypeError):
                model.distribution(bad)

    def test_binary_type_rejected(self):
        for bad in (True, False, 0.0, "0", None):
            with self.assertRaises(TypeError):
                model.evaluate("X_to_Y", bad)
            for variable in ("X", "Y"):
                with self.assertRaises(TypeError):
                    model.evaluate("X_to_Y", 0, {variable: bad})
                with self.assertRaises(TypeError):
                    model.distribution("Y_to_X", {variable: bad})

    def test_binary_range_rejected(self):
        for bad in (-1, 2, 1000):
            with self.assertRaises(ValueError):
                model.evaluate("X_to_Y", bad)
            with self.assertRaises(ValueError):
                model.distribution("X_to_Y", {"X": bad})

    def test_intervention_container_rejected(self):
        for bad in ([], (), (("X", 0),), "X=0", 0, True):
            with self.assertRaises(TypeError):
                model.evaluate("X_to_Y", 0, bad)
            with self.assertRaises(TypeError):
                model.distribution("X_to_Y", bad)

    def test_unknown_intervention_variable_rejected(self):
        for bad in ("U", "Z", "x", ""):
            with self.assertRaises(ValueError):
                model.distribution("X_to_Y", {bad: 0})

    def test_intervention_variable_type_rejected(self):
        for bad in (None, 0, True, ("X",)):
            with self.assertRaises(TypeError):
                model.evaluate("Y_to_X", 0, {bad: 0})

    def test_none_and_empty_intervention_equivalent(self):
        for name, u in product(model.MODELS, (0, 1)):
            self.assertEqual(model.evaluate(name, u), model.evaluate(name, u, {}))

    def test_published_results_consistent(self):
        result = model.results()
        self.assertTrue(result["scm"]["observational_distributions_equal"])
        self.assertFalse(result["scm"]["do_X_0_distributions_equal"])
        self.assertEqual(len(result["scm"]["intervention_cases"]), 9)


if __name__ == "__main__":
    unittest.main()
