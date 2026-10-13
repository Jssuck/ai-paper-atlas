"""Regression and adversarial-input checks. unittest checks survive -O/-OO."""

import ast
import itertools
import json
from pathlib import Path
from fractions import Fraction
import sys
import unittest

from model import (
    Add, Certificate, Const, Equation, Expr, FiniteSign, Mul, Polynomial, Premise,
    Triangle, Var, check_certificate, evaluate_expr, evaluate_polynomial, exact,
    first_counterexample, normalize, restrict_certificate, section16_example, substitute, triangle_cases,
)

FINITE_CASE_COUNTS = {"distributivity_assignments": 0, "normalization_tree_assignments": 0,
                     "simultaneous_substitution_assignments": 0}


class ExactInputTests(unittest.TestCase):
    def test_fraction_and_integer_are_exact(self):
        self.assertEqual(exact(Fraction(2, 6)), Fraction(1, 3))
        self.assertEqual(exact(-7), Fraction(-7))

    def test_approximate_or_implicit_numbers_rejected(self):
        for bad in (True, False, 0.5, "1/2", None, complex(1, 0)):
            with self.subTest(value=bad), self.assertRaises(TypeError):
                exact(bad)

    def test_safety_does_not_depend_on_python_assert(self):
        source = Path(__file__).with_name("model.py").read_text(encoding="utf-8")
        self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(source))))


class CertificateTests(unittest.TestCase):
    def setUp(self):
        self.premises, self.target, self.certificate = section16_example()
        self.keep = ("alternate_a", "alternate_c", "straight_angle")

    def test_sum_recomputes_coefficients_and_rhs(self):
        result = check_certificate(self.premises, self.target, self.certificate)
        self.assertTrue(result.valid)
        self.assertEqual(result.combined.coefficients, (1, 1, 1, 0, 0))
        self.assertEqual(result.combined.rhs, Fraction(180))

    def test_zero_weight_rows_are_not_dependencies(self):
        result = check_certificate(self.premises, self.target, self.certificate)
        self.assertEqual(result.dependencies, self.keep)

    def test_general_certificate_transfers_and_is_rechecked(self):
        reduced, certificate = restrict_certificate(
            self.premises, self.target, self.certificate, self.keep)
        self.assertEqual(len(reduced), 3)
        self.assertEqual(certificate.weights, (1, 1, 1))
        self.assertTrue(check_certificate(reduced, self.target, certificate).valid)

    def test_special_target_depends_on_special_fact(self):
        target = Equation(self.target.variables, (0, 1, 0, 0, 0), 90)
        certificate = Certificate((0, 0, 0, 1, 0))
        result = check_certificate(self.premises, target, certificate)
        self.assertTrue(result.valid)
        self.assertEqual(result.dependencies, ("drawing_right",))
        with self.assertRaisesRegex(ValueError, "drawing_right"):
            restrict_certificate(self.premises, target, certificate, self.keep)
        self.assertFalse(check_certificate(self.premises[:3], target, Certificate((0, 0, 0))).valid)

    def test_general_premises_have_nonright_model(self):
        # An exact semantic countermodel to deriving b=90, stronger than one
        # failed certificate. It satisfies every remaining linear equation.
        values = (Fraction(60),) * 5
        for premise in self.premises[:3]:
            self.assertEqual(sum(c * x for c, x in zip(premise.equation.coefficients, values)),
                             premise.equation.rhs)
        self.assertNotEqual(values[1], 90)
        self.assertEqual(values[0], values[2])  # Even the isosceles fact is preserved.

    def test_wrong_weight_is_rejected_as_a_proof(self):
        result = check_certificate(self.premises, self.target, Certificate((1, 1, 2, 0, 0)))
        self.assertFalse(result.valid)
        self.assertNotEqual(result.combined.rhs, self.target.rhs)

    def test_right_coefficients_wrong_rhs_fails(self):
        bad = Equation(self.target.variables, self.target.coefficients, 181)
        self.assertFalse(check_certificate(self.premises, bad, self.certificate).valid)

    def test_right_rhs_wrong_coefficients_fails(self):
        bad = Equation(self.target.variables, (1, 0, 1, 0, 0), 180)
        self.assertFalse(check_certificate(self.premises, bad, self.certificate).valid)

    def test_fractional_and_negative_weights(self):
        premises = (Premise("twice", Equation(("x",), (2,), 6)),
                    Premise("minus", Equation(("x",), (-1,), -3)))
        result = check_certificate(premises, Equation(("x",), (2,), 6),
                                   Certificate((Fraction(1, 2), -1)))
        self.assertTrue(result.valid)
        self.assertEqual(result.dependencies, ("twice", "minus"))

    def test_cancelled_nonzero_rows_still_count_as_dependencies(self):
        equation = Equation(("x",), (1,), 2)
        premises = (Premise("one", equation), Premise("two", equation))
        result = check_certificate(premises, Equation(("x",), (0,), 0), Certificate((1, -1)))
        self.assertTrue(result.valid)
        self.assertEqual(result.dependencies, ("one", "two"))
        with self.assertRaises(ValueError):
            restrict_certificate(premises, Equation(("x",), (0,), 0), Certificate((1, -1)), ())

    def test_empty_certificate_proves_only_zero_equation(self):
        self.assertTrue(check_certificate((), Equation(("x",), (0,), 0), Certificate(())).valid)
        self.assertFalse(check_certificate((), Equation(("x",), (0,), 1), Certificate(())).valid)

    def test_restriction_cannot_repair_an_invalid_proof(self):
        with self.assertRaisesRegex(ValueError, "invalid certificate"):
            restrict_certificate(self.premises, self.target, Certificate((0, 0, 0, 0, 0)), self.keep)

    def test_restriction_checks_unknown_duplicate_and_typed_labels(self):
        for keep in (("unknown",), self.keep + ("alternate_a",), (1,), ["alternate_a"]):
            with self.subTest(keep=keep), self.assertRaises((ValueError, TypeError)):
                restrict_certificate(self.premises, self.target, self.certificate, keep)

    def test_schema_order_is_significant(self):
        target = Equation(("b", "a", "c", "u", "v"), self.target.coefficients, 180)
        with self.assertRaises(ValueError):
            check_certificate(self.premises, target, self.certificate)

    def test_equation_rejects_bad_schema_dimension_and_types(self):
        bad_cases = (
            ((), (), 0), (["x"], (1,), 0), (("x", "x"), (1, 2), 0),
            (("x",), (), 0), (("x",), [1], 0), (("",), (1,), 0),
            (("x",), (True,), 0), (("x",), (1,), 0.0),
        )
        for variables, coefficients, rhs in bad_cases:
            with self.subTest(case=(variables, coefficients, rhs)), self.assertRaises((TypeError, ValueError)):
                Equation(variables, coefficients, rhs)

    def test_certificate_rejects_bad_weight_type_and_length(self):
        for weights in ([1, 1], (True,), (0.5,)):
            with self.subTest(weights=weights), self.assertRaises(TypeError):
                Certificate(weights)
        with self.assertRaises(ValueError):
            check_certificate(self.premises, self.target, Certificate((1,)))

    def test_premise_and_checker_reject_bad_objects(self):
        with self.assertRaises(TypeError):
            Premise("p", "x=1")
        with self.assertRaises(ValueError):
            Premise("", self.target)
        for premises, target, certificate in (
            (list(self.premises), self.target, self.certificate),
            (("bad",), self.target, Certificate((1,))),
            (self.premises, "bad", self.certificate),
            (self.premises, self.target, (1, 1, 1, 0, 0)),
        ):
            with self.subTest(case=(premises, target, certificate)), self.assertRaises(TypeError):
                check_certificate(premises, target, certificate)
        with self.assertRaises(ValueError):
            check_certificate((self.premises[0], self.premises[0]), self.target, Certificate((1, 1)))


class SignTests(unittest.TestCase):
    def setUp(self):
        self.cases = triangle_cases()
        self.general = FiniteSign("triangle", self.cases, frozenset(self.cases))

    def test_squared_sides_and_nonright_counterexamples(self):
        self.assertEqual([t.squared_sides() for t in self.cases], [(9, 16, 25), (4, 5, 5), (2, 10, 16)])
        self.assertEqual([t.is_right() for t in self.cases], [True, False, False])

    def test_one_case_does_not_cover_three_cases(self):
        representative = FiniteSign("one", self.cases, frozenset((self.cases[0],)))
        self.assertTrue(self.general.covers_domain())
        self.assertFalse(representative.covers_domain())
        self.assertIsNone(first_counterexample(representative, lambda t: t.is_right()))
        self.assertEqual(first_counterexample(self.general, lambda t: t.is_right()), self.cases[1])

    def test_coverage_is_relative_to_declared_domain(self):
        singleton_domain = (self.cases[0],)
        singleton = FiniteSign("only", singleton_domain, frozenset(singleton_domain))
        self.assertTrue(singleton.covers_domain())
        self.assertFalse(FiniteSign("same", self.cases, singleton.denotation).covers_domain())

    def test_empty_denotation_is_vacuous_but_not_general(self):
        empty = FiniteSign("empty", self.cases, frozenset())
        self.assertFalse(empty.covers_domain())
        self.assertIsNone(first_counterexample(empty, lambda t: False))

    def test_counterexample_order_is_domain_order(self):
        reversed_cases = tuple(reversed(self.cases))
        sign = FiniteSign("reverse", reversed_cases, frozenset(reversed_cases))
        self.assertEqual(first_counterexample(sign, lambda t: t.is_right()), self.cases[2])

    def test_degenerate_triangles_are_rejected(self):
        for vertices in (((0, 0), (1, 1), (2, 2)), ((0, 0), (0, 0), (1, 2))):
            with self.subTest(vertices=vertices), self.assertRaises(ValueError):
                Triangle(vertices)

    def test_bad_triangle_dimensions_and_coordinates_are_rejected(self):
        for vertices in ((), ((0, 0), (1, 1)), [(0, 0), (1, 0), (0, 1)],
                         ((0, 0), (1.0, 0), (0, 1)), ((False, 0), (1, 0), (0, 1)),
                         ((0, 0, 0), (1, 0), (0, 1))):
            with self.subTest(vertices=vertices), self.assertRaises(TypeError):
                Triangle(vertices)

    def test_large_integer_translation_is_exact(self):
        offset = 10 ** 100
        triangle = Triangle(((offset, offset), (offset + 3, offset), (offset, offset + 4)))
        self.assertEqual(triangle.squared_sides(), (9, 16, 25))
        self.assertTrue(triangle.is_right())

    def test_sign_rejects_duplicate_or_outside_cases(self):
        with self.assertRaises(ValueError):
            FiniteSign("bad", (self.cases[0], self.cases[0]), frozenset())
        with self.assertRaises(ValueError):
            FiniteSign("bad", (self.cases[0],), frozenset((self.cases[1],)))

    def test_sign_rejects_malformed_domain_or_denotation(self):
        for domain, denotation in (((), frozenset()), ([self.cases[0]], frozenset()),
                                  (("triangle",), frozenset()), (self.cases, set(self.cases)),
                                  (self.cases, frozenset(("triangle",)))):
            with self.subTest(case=(domain, denotation)), self.assertRaises(TypeError):
                FiniteSign("bad", domain, denotation)

    def test_predicate_and_sign_are_checked(self):
        with self.assertRaises(TypeError):
            first_counterexample(self.general, lambda t: 1)
        with self.assertRaises(TypeError):
            first_counterexample(self.general, "right")
        with self.assertRaises(TypeError):
            first_counterexample("triangle", lambda t: True)


class PolynomialTests(unittest.TestCase):
    def setUp(self):
        self.x, self.y, self.z = Var("x"), Var("y"), Var("z")

    def test_distributivity_has_identical_canonical_forms(self):
        left = Mul(self.x, Add(self.y, self.z))
        right = Add(Mul(self.x, self.y), Mul(self.x, self.z))
        expected = Polynomial((((('x', 1), ('y', 1)), Fraction(1)),
                               ((('x', 1), ('z', 1)), Fraction(1))))
        self.assertEqual(normalize(left), expected)
        self.assertEqual(normalize(right), expected)

    def test_commutativity_and_associativity(self):
        self.assertEqual(normalize(Mul(self.x, self.y)), normalize(Mul(self.y, self.x)))
        self.assertEqual(normalize(Add(self.x, self.y)), normalize(Add(self.y, self.x)))
        self.assertEqual(normalize(Add(self.x, Add(self.y, self.z))),
                         normalize(Add(Add(self.x, self.y), self.z)))
        self.assertEqual(normalize(Mul(self.x, Mul(self.y, self.z))),
                         normalize(Mul(Mul(self.x, self.y), self.z)))

    def test_fraction_coefficients_collect_exactly(self):
        expression = Add(Mul(Const(Fraction(1, 3)), self.x), Mul(Const(Fraction(1, 6)), self.x))
        self.assertEqual(normalize(expression), Polynomial((((('x', 1),), Fraction(1, 2)),)))

    def test_cancellation_removes_zero_terms(self):
        self.assertEqual(normalize(Add(self.x, Mul(Const(-1), self.x))), Polynomial(()))
        self.assertEqual(normalize(Mul(Const(0), self.x)), Polynomial(()))
        self.assertEqual(normalize(Const(0)), Polynomial(()))

    def test_powers_are_added_and_terms_are_sorted(self):
        expression = Mul(Mul(self.y, self.x), Mul(self.x, self.y))
        self.assertEqual(normalize(expression), Polynomial((((('x', 2), ('y', 2)), Fraction(1)),)))

    def test_nonidentity_is_distinguished(self):
        self.assertNotEqual(normalize(Add(self.x, self.y)), normalize(Mul(self.x, self.y)))
        self.assertNotEqual(normalize(Const(1)), normalize(Const(2)))

    def test_one_successful_substitution_is_not_an_identity(self):
        left, right = self.x, Mul(self.x, self.x)
        self.assertEqual(evaluate_expr(left, {"x": 1}), evaluate_expr(right, {"x": 1}))
        self.assertNotEqual(normalize(left), normalize(right))
        self.assertNotEqual(evaluate_expr(left, {"x": 2}), evaluate_expr(right, {"x": 2}))

    def test_125_assignments_for_distributivity(self):
        left = Mul(self.x, Add(self.y, self.z))
        right = Add(Mul(self.x, self.y), Mul(self.x, self.z))
        values = (Fraction(-2), Fraction(-1, 2), Fraction(0), Fraction(2, 3), Fraction(3))
        for x, y, z in itertools.product(values, repeat=3):
            FINITE_CASE_COUNTS["distributivity_assignments"] += 1
            with self.subTest(x=x, y=y, z=z):
                environment = {"x": x, "y": y, "z": z}
                self.assertEqual(evaluate_expr(left, environment), evaluate_expr(right, environment))
                self.assertEqual(evaluate_expr(left, environment), evaluate_polynomial(normalize(left), environment))

    def test_generated_expression_normalization_agrees_on_1445_cases(self):
        # Five atoms; all 50 depth-one Add/Mul trees; 30 depth-two trees.
        atoms = (Const(Fraction(1, 2)), Const(-2), Const(0), self.x, self.y)
        trees = list(atoms)
        trees.extend(op(a, b) for op in (Add, Mul) for a in atoms for b in atoms)
        trees.extend(op(tree, self.x) for op in (Add, Mul) for tree in trees[5:20])
        self.assertEqual(len(trees), 85)
        environments = [{"x": Fraction(i, 3), "y": Fraction(2 - i, 5)} for i in range(-8, 9)]
        count = 0
        for index, tree in enumerate(trees):
            polynomial = normalize(tree)
            for environment in environments:
                FINITE_CASE_COUNTS["normalization_tree_assignments"] += 1
                with self.subTest(tree=index, environment=environment):
                    self.assertEqual(evaluate_expr(tree, environment), evaluate_polynomial(polynomial, environment))
                count += 1
        self.assertEqual(count, 1445)

    def test_constants_and_missing_variables(self):
        self.assertEqual(evaluate_expr(Const(Fraction(1, 3)), {}), Fraction(1, 3))
        self.assertEqual(evaluate_polynomial(Polynomial(()), {}), Fraction(0))
        with self.assertRaises(KeyError):
            evaluate_expr(self.x, {})
        with self.assertRaises(KeyError):
            evaluate_polynomial(normalize(self.x), {})

    def test_normalization_law_requires_original_variables_assigned(self):
        expression = Add(self.x, Mul(Const(-1), self.x))
        with self.assertRaises(KeyError):
            evaluate_expr(expression, {})
        self.assertEqual(evaluate_polynomial(normalize(expression), {}), 0)
        self.assertEqual(evaluate_expr(expression, {"x": 7}),
                         evaluate_polynomial(normalize(expression), {"x": 7}))

    def test_environment_requires_exact_values_and_names(self):
        for environment in ({"x": 0.5}, {"x": True}, {"bad name": 1}, [1, 2]):
            with self.subTest(environment=environment), self.assertRaises((TypeError, ValueError)):
                evaluate_expr(self.x, environment)
            with self.subTest(environment=environment), self.assertRaises((TypeError, ValueError)):
                evaluate_polynomial(normalize(self.x), environment)

    def test_expression_constructors_reject_unsupported_objects(self):
        with self.assertRaises(TypeError):
            Const(0.5)
        with self.assertRaises(ValueError):
            Var("")
        for constructor in (Add, Mul):
            with self.assertRaises(TypeError):
                constructor(self.x, 1)
        for expression in (Expr(), "x/y", 1):
            with self.subTest(expression=expression), self.assertRaises(TypeError):
                normalize(expression)
            with self.subTest(expression=expression), self.assertRaises(TypeError):
                evaluate_expr(expression, {})
        with self.assertRaises(TypeError):
            evaluate_polynomial(self.x, {"x": 1})

    def test_canonical_form_rejects_zero_duplicate_or_unsorted_terms(self):
        bad_terms = (
            (((), Fraction(0)),),
            (((), Fraction(1)), ((), Fraction(2))),
            (((('y', 1),), Fraction(1)), ((('x', 1),), Fraction(1))),
            (((('x', 1), ('x', 2)), Fraction(1)),),
            (((('y', 1), ('x', 1)), Fraction(1)),),
        )
        for terms in bad_terms:
            with self.subTest(terms=terms), self.assertRaises(ValueError):
                Polynomial(terms)

    def test_canonical_form_rejects_bad_dimensions_and_types(self):
        bad_terms = ([], (1,), (((),),), (([], 1),), ((('x',), 1),),
                     (((('x', 0),), 1),), (((('x', -1),), 1),),
                     (((('x', True),), 1),), (((('x', 1),), 0.5),))
        for terms in bad_terms:
            with self.subTest(terms=terms), self.assertRaises((ValueError, TypeError)):
                Polynomial(terms)

    def test_substitution_is_simultaneous_not_recursive_rewriting(self):
        replacement = Add(self.y, Const(1))
        replacements = {"x": replacement, "y": Const(2)}
        result = substitute(self.x, replacements)
        self.assertEqual(result, replacement)
        self.assertNotEqual(result, Add(Const(2), Const(1)))
        self.assertEqual(substitute(self.y, replacements), Const(2))

    def test_substitution_can_swap_variables_without_looping(self):
        expression = Add(self.x, self.y)
        self.assertEqual(substitute(expression, {"x": self.y, "y": self.x}), Add(self.y, self.x))

    def test_substitution_empty_mapping_constants_and_unmapped_variables(self):
        expression = Mul(Add(self.x, Const(Fraction(1, 2))), self.z)
        self.assertEqual(substitute(expression, {}), expression)
        self.assertEqual(substitute(Const(3), {"x": self.y}), Const(3))
        self.assertEqual(substitute(self.z, {"x": self.y}), self.z)

    def test_substitution_rejects_bad_objects(self):
        for replacements in ([1, 2], {"x": 1}, {"bad name": self.y}):
            with self.subTest(replacements=replacements), self.assertRaises((TypeError, ValueError)):
                substitute(self.x, replacements)
        with self.assertRaises(TypeError):
            substitute("x", {})

    def test_125_simultaneous_substitutions_match_induced_environment(self):
        expression = Mul(self.x, Add(self.y, self.z))
        replacements = {"x": Add(self.y, Const(1)), "y": Mul(Const(2), self.x)}
        replaced = substitute(expression, replacements)
        values = (Fraction(-2), Fraction(-1, 2), Fraction(0), Fraction(2, 3), Fraction(3))
        for x, y, z in itertools.product(values, repeat=3):
            FINITE_CASE_COUNTS["simultaneous_substitution_assignments"] += 1
            with self.subTest(x=x, y=y, z=z):
                environment = {"x": x, "y": y, "z": z}
                induced = {name: evaluate_expr(replacements.get(name, Var(name)), environment)
                           for name in ("x", "y", "z")}
                self.assertEqual(evaluate_expr(replaced, environment), evaluate_expr(expression, induced))
                self.assertEqual(evaluate_expr(replaced, environment),
                                 evaluate_polynomial(normalize(replaced), environment))

    def test_substitution_preserves_distributivity_canonical_identity(self):
        left = Mul(self.x, Add(self.y, self.z))
        right = Add(Mul(self.x, self.y), Mul(self.x, self.z))
        replacements = {"x": Add(self.x, self.y), "y": Mul(self.y, self.z), "z": Const(Fraction(-2, 3))}
        self.assertEqual(normalize(substitute(left, replacements)), normalize(substitute(right, replacements)))


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "successful": result.wasSuccessful(),
        "finite_case_groups_attempted": FINITE_CASE_COUNTS,
        "count_note": "tests_run counts unittest methods; finite cases count attempted nested checks, not extra methods",
        "optimization": sys.flags.optimize,
    }, sort_keys=True))
    sys.exit(0 if result.wasSuccessful() else 1)
