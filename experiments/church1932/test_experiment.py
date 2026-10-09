"""Finite regression/property checks, NOT proofs about arbitrary lambda terms."""

import itertools
import unittest

from experiment import (
    ADD, CONSTANT, IDENTITY, MULT, OMEGA, App, Lam, Var,
    alpha_equivalent, church_numeral, decode_numeral, debruijn,
    free_vars, naive_substitute, normalize, run_experiments, step, substitute,
)


class SubstitutionTests(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(substitute(Var("x"), "x", Var("a")), Var("a"))

    def test_absent_variable(self):
        original = Lam("y", Var("z"))
        self.assertEqual(substitute(original, "x", Var("y")), original)

    def test_bound_occurrence_is_not_replaced(self):
        self.assertEqual(substitute(IDENTITY, "x", Var("y")), IDENTITY)

    def test_capture_counterexample(self):
        body = Lam("y", Var("x"))
        good = substitute(body, "x", Var("y"))
        bad = naive_substitute(body, "x", Var("y"))
        self.assertEqual(good, Lam("y_0", Var("y")))
        self.assertEqual(bad, Lam("y", Var("y")))
        self.assertEqual(free_vars(good), {"y"})
        self.assertEqual(free_vars(bad), set())
        self.assertFalse(alpha_equivalent(good, bad))

    def test_fresh_name_avoids_inner_binders(self):
        body = Lam("y", App(App(Var("x"), Var("y")), Lam("y_0", Var("y_0"))))
        expected = Lam("y_1", App(App(Var("y"), Var("y_1")), Lam("y_0", Var("y_0"))))
        self.assertEqual(substitute(body, "x", Var("y")), expected)

    def test_renaming_respects_shadowing(self):
        original = Lam("y", App(Var("x"), Lam("y", Var("y"))))
        expected = Lam("y_0", App(Var("y"), Lam("y", Var("y"))))
        self.assertEqual(substitute(original, "x", Var("y")), expected)

    def test_free_variable_law_on_small_terms(self):
        # 507 source terms of depth <= 2, 3 variables, 4 replacements.
        # Also compare with a separate locally nameless substitution oracle.
        # Only literal free names are replaced; locally bound indices in the
        # replacement are already scoped by its own lambdas and need no shift.
        def replace_free_key(key, variable, replacement_key):
            if key == ("free", variable):
                return replacement_key
            if key[0] == "lam":
                return ("lam", replace_free_key(key[1], variable, replacement_key))
            if key[0] == "app":
                return ("app", replace_free_key(key[1], variable, replacement_key),
                        replace_free_key(key[2], variable, replacement_key))
            return key

        names = ("x", "y", "z")
        terms = [Var(x) for x in names]
        for _ in range(2):
            previous = terms
            terms = ([Var(x) for x in names]
                     + [Lam(x, t) for x, t in itertools.product(names, previous)]
                     + [App(a, b) for a, b in itertools.product(previous, repeat=2)])
        self.assertEqual(len(terms), 507)
        replacements = [Var(x) for x in names] + [Lam("z", App(Var("y"), Var("z")))]
        for term, variable, replacement in itertools.product(terms, names, replacements):
            expected = free_vars(term)
            if variable in expected:
                expected = (expected - {variable}) | free_vars(replacement)
            substituted = substitute(term, variable, replacement)
            actual = free_vars(substituted)
            self.assertEqual(actual, expected, (term, variable, replacement))
            self.assertEqual(debruijn(substituted),
                             replace_free_key(debruijn(term), variable, debruijn(replacement)),
                             (term, variable, replacement))


class AlphaTests(unittest.TestCase):
    def test_identity_rename(self):
        self.assertTrue(alpha_equivalent(IDENTITY, Lam("z", Var("z"))))

    def test_literal_free_names_matter(self):
        self.assertFalse(alpha_equivalent(Lam("x", Var("y")), Lam("x", Var("z"))))

    def test_free_and_bound_differ(self):
        self.assertFalse(alpha_equivalent(IDENTITY, Lam("z", Var("x"))))

    def test_shadowing_uses_nearest_binder(self):
        self.assertEqual(debruijn(Lam("x", Lam("x", Var("x")))),
                         ("lam", ("lam", ("bound", 0))))
        self.assertTrue(alpha_equivalent(Lam("x", Lam("x", Var("x"))),
                                         Lam("a", Lam("b", Var("b")))))
        self.assertFalse(alpha_equivalent(Lam("x", Lam("x", Var("x"))),
                                          Lam("a", Lam("b", Var("a")))))

    def test_alpha_is_not_beta_equivalence(self):
        self.assertFalse(alpha_equivalent(App(IDENTITY, Var("a")), Var("a")))


class ReductionTests(unittest.TestCase):
    def test_identity_both_strategies_and_modes(self):
        for strategy, mode in itertools.product(("normal", "applicative"),
                                                 ("modern", "non_erasing")):
            result = normalize(App(IDENTITY, Var("a")), strategy, mode)
            self.assertEqual((result.status, result.steps, result.term),
                             ("normal_form", 1, Var("a")))

    def test_reduces_beneath_lambda(self):
        for strategy in ("normal", "applicative"):
            self.assertEqual(step(Lam("z", App(IDENTITY, Var("y"))), strategy),
                             Lam("z", Var("y")))

    def test_capture_avoiding_beta(self):
        result = normalize(App(Lam("x", Lam("y", Var("x"))), Var("y")))
        self.assertTrue(alpha_equivalent(result.term, Lam("z", Var("y"))))
        self.assertEqual(free_vars(result.term), {"y"})

    def test_constant_omega_modern_normal(self):
        result = normalize(App(App(CONSTANT, Var("y")), OMEGA))
        self.assertEqual((result.status, result.steps, result.term),
                         ("normal_form", 2, Var("y")))

    def test_constant_omega_modern_applicative(self):
        result = normalize(App(App(CONSTANT, Var("y")), OMEGA), "applicative")
        self.assertEqual((result.status, result.steps, result.cycle_length),
                         ("cycle_detected", 2, 1))

    def test_constant_omega_non_erasing_normal(self):
        result = normalize(App(App(CONSTANT, Var("y")), OMEGA), mode="non_erasing")
        self.assertEqual((result.status, result.steps, result.cycle_length),
                         ("cycle_detected", 2, 1))

    def test_erasure_grammar_allowed_but_conversion_blocked(self):
        term = App(Lam("x", Var("y")), Var("z"))
        self.assertEqual(step(term), Var("y"))
        self.assertIsNone(step(term, mode="non_erasing"))
        result = normalize(term, mode="non_erasing")
        self.assertEqual((result.status, result.steps, result.term),
                         ("normal_form", 0, term))

    def test_shadowed_occurrence_does_not_satisfy_occurrence_condition(self):
        term = App(Lam("x", Lam("x", Var("x"))), Var("z"))
        self.assertIsNone(step(term, mode="non_erasing"))
        self.assertEqual(step(term), Lam("x", Var("x")))

    def test_restricted_mode_still_avoids_capture(self):
        term = App(Lam("x", Lam("y", Var("x"))), Var("y"))
        self.assertTrue(alpha_equivalent(step(term, mode="non_erasing"),
                                         Lam("z", Var("y"))))

    def test_omega_step_is_not_confused_with_normal_form(self):
        self.assertEqual(step(OMEGA), OMEGA)
        result = normalize(OMEGA)
        self.assertEqual((result.status, result.steps, result.cycle_start, result.cycle_length),
                         ("cycle_detected", 1, 0, 1))

    def test_budget_only_is_inconclusive(self):
        result = normalize(OMEGA, max_steps=8, detect_cycles=False)
        self.assertEqual((result.status, result.steps, result.cycle_start),
                         ("step_limit", 8, None))

    def test_nonrepeating_growth_reaches_step_limit(self):
        grow = Lam("x", App(App(Var("x"), Var("x")), Var("x")))
        result = normalize(App(grow, grow), max_steps=8)
        self.assertEqual((result.status, result.steps), ("step_limit", 8))
        self.assertEqual(len(set(result.trace)), 9)

    def test_zero_budget_distinguishes_normal_form(self):
        self.assertEqual(normalize(Var("x"), max_steps=0).status, "normal_form")
        self.assertEqual(normalize(OMEGA, max_steps=0).status, "step_limit")

    def test_exact_budget_still_recognizes_result(self):
        self.assertEqual(normalize(App(IDENTITY, Var("a")), max_steps=1).status,
                         "normal_form")

    def test_invalid_options(self):
        for value in (-1, 1.5, True):
            with self.assertRaises(ValueError):
                normalize(IDENTITY, max_steps=value)
        with self.assertRaises(ValueError):
            step(IDENTITY, strategy="weak_cbv")
        with self.assertRaises(ValueError):
            step(IDENTITY, mode="exact_1932")


class NumeralTests(unittest.TestCase):
    def test_round_trip(self):
        for n in range(8):
            self.assertEqual(decode_numeral(church_numeral(n)), n)

    def test_alpha_renamed_numeral(self):
        self.assertEqual(decode_numeral(Lam("g", Lam("u", App(Var("g"), Var("u"))))), 1)

    def test_modern_addition_and_multiplication_small_grid(self):
        for operator, operation in ((ADD, lambda a, b: a + b),
                                    (MULT, lambda a, b: a * b)):
            for left, right, strategy in itertools.product(range(4), range(4),
                                                            ("normal", "applicative")):
                term = App(App(operator, church_numeral(left)), church_numeral(right))
                result = normalize(term, strategy, max_steps=256)
                self.assertEqual(result.status, "normal_form")
                self.assertEqual(decode_numeral(result.term), operation(left, right))
                self.assertTrue(alpha_equivalent(result.term, church_numeral(operation(left, right))))

    def test_invalid_numerals(self):
        for n in (-1, 1.5, True):
            with self.assertRaises(ValueError):
                church_numeral(n)
        for term in (Var("x"), IDENTITY, Lam("f", Lam("x", Var("f"))),
                     Lam("f", Lam("x", Var("y")))):
            with self.assertRaises(ValueError):
                decode_numeral(term)

    def test_saved_experiment_contract(self):
        data = run_experiments()
        self.assertEqual(data["capture_counterexample"]["alpha_equivalent"], False)
        self.assertEqual([row["decoded"] for row in data["arithmetic"]], [5, 6, 0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
