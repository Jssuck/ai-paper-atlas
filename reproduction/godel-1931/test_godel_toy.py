"""Adversarial unit tests and small exhaustive checks; no third-party packages."""

import itertools
import unittest

from godel_toy import (
    MAX_AST_NODES, MAX_CODE, MAX_LENGTH, MAX_PROOF_LINES, MAX_SYMBOL, PRIMES,
    Add, And, Eq, Nat, Not, Var, ProofStep, bounded_search, check_proof,
    component, concatenate, decode, encode, encode_proof, evaluate,
    formula_code, formula_tokens, proof_relation, substitute_numeral,
    validate_formula,
)


class SequenceCodingTests(unittest.TestCase):
    def test_hand_computed_code(self):
        self.assertEqual(encode((0, 2, 1)), 1350)
        self.assertEqual(decode(1350), (0, 2, 1))

    def test_empty_and_zero_are_distinct(self):
        self.assertEqual(encode(()), 1)
        self.assertEqual(decode(1), ())
        self.assertEqual(encode((0,)), 2)
        self.assertEqual(decode(2), (0,))

    def test_exhaustive_roundtrip_and_injectivity(self):
        seen = {}
        for length in range(5):
            for sequence in itertools.product(range(4), repeat=length):
                code = encode(sequence)
                self.assertNotIn(code, seen)
                self.assertEqual(decode(code), sequence)
                seen[code] = sequence
        self.assertEqual(len(seen), 341)

    def test_full_teaching_bounds_roundtrip(self):
        seq = (MAX_SYMBOL,) * MAX_LENGTH
        self.assertEqual(encode(seq), MAX_CODE)
        self.assertEqual(decode(MAX_CODE), seq)

    def test_decode_encode_identity_for_all_small_valid_codes(self):
        for number in range(1, 2001):
            try:
                sequence = decode(number)
            except ValueError:
                continue
            self.assertEqual(encode(sequence), number)

    def test_holes_rejected(self):
        for code in (3, 5, 10, 14, 2 * 3 * 7, 2 * 3 * 5 * 11):
            with self.subTest(code=code), self.assertRaises(ValueError):
                decode(code)

    def test_extra_prime_rejected(self):
        from math import prod
        with self.assertRaises(ValueError):
            decode(prod(PRIMES) * 97)

    def test_excess_exponent_rejected(self):
        with self.assertRaises(ValueError):
            decode(2 ** (MAX_SYMBOL + 2))

    def test_bad_decode_inputs(self):
        for code in (0, -1, True, False, 1.0, "2", None, MAX_CODE + 1):
            with self.subTest(code=code), self.assertRaises(ValueError):
                decode(code)

    def test_bad_symbol_values(self):
        for value in (-1, MAX_SYMBOL + 1, True, 0.5, "0", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                encode([value])

    def test_length_limit(self):
        with self.assertRaises(ValueError):
            encode([0] * (MAX_LENGTH + 1))

    def test_non_sequence_rejected_before_iteration(self):
        for value in (None, "123", iter([1, 2])):
            with self.assertRaises(TypeError):
                encode(value)

    def test_component(self):
        self.assertEqual(component(1350, 0), 0)
        self.assertEqual(component(1350, 1), 2)
        with self.assertRaises(IndexError):
            component(1350, 3)
        with self.assertRaises(IndexError):
            component(1, 0)
        for index in (-1, True, 1.5):
            with self.assertRaises(ValueError):
                component(1350, index)

    def test_concatenation(self):
        self.assertEqual(concatenate(encode((0, 2)), encode((1,))), 1350)
        for seq in ((), (0,), (0, 2, 1)):
            self.assertEqual(concatenate(1, encode(seq)), encode(seq))
            self.assertEqual(concatenate(encode(seq), 1), encode(seq))
        self.assertNotEqual(encode((0, 2)) * encode((1,)), 1350)

    def test_concatenation_enforces_bound(self):
        with self.assertRaises(ValueError):
            concatenate(encode([0] * MAX_LENGTH), encode([0]))


class QuantifierFreeSyntaxTests(unittest.TestCase):
    def setUp(self):
        self.formula = Eq(Add(Var("x"), Nat(1)), Nat(3))

    def test_substitution_correct_and_immutable(self):
        replaced = substitute_numeral(self.formula, "x", 2)
        self.assertEqual(replaced, Eq(Add(Nat(2), Nat(1)), Nat(3)))
        self.assertEqual(self.formula.left.left, Var("x"))
        self.assertTrue(evaluate(replaced))

    def test_multiple_occurrences_and_other_variable(self):
        formula = Eq(Add(Var("x"), Var("x")), Var("y"))
        result = substitute_numeral(formula, "x", 2)
        self.assertEqual(result, Eq(Add(Nat(2), Nat(2)), Var("y")))
        self.assertTrue(evaluate(result, {"y": 4}))

    def test_absent_variable_leaves_formula_equal(self):
        self.assertEqual(substitute_numeral(self.formula, "z", 5), self.formula)

    def test_substitution_agrees_with_evaluation_exhaustively(self):
        formula = Eq(Add(Var("x"), Nat(1)), Var("y"))
        for x in range(5):
            for y in range(7):
                substituted = substitute_numeral(formula, "x", x)
                self.assertEqual(evaluate(formula, {"x": x, "y": y}),
                                 evaluate(substituted, {"y": y}))

    def test_logical_nodes(self):
        formula = And(Eq(Var("x"), Nat(2)), Not(Eq(Var("x"), Nat(1))))
        self.assertTrue(evaluate(substitute_numeral(formula, "x", 2)))
        self.assertFalse(evaluate(substitute_numeral(formula, "x", 1)))

    def test_prefix_encoding(self):
        expected = (3, 2, 1, 0, 0, 1, 0, 3)
        self.assertEqual(formula_tokens(self.formula), expected)
        self.assertEqual(decode(formula_code(self.formula)), expected)
        replaced = substitute_numeral(self.formula, "x", 2)
        self.assertNotEqual(formula_code(self.formula), formula_code(replaced))

    def test_missing_environment_variable(self):
        with self.assertRaises(KeyError):
            evaluate(self.formula)

    def test_both_boolean_branches_checked(self):
        formula = And(Eq(Nat(0), Nat(1)), Eq(Var("x"), Nat(0)))
        with self.assertRaises(KeyError):
            evaluate(formula)

    def test_invalid_environment_values(self):
        for value in (-1, 32, True, 1.0):
            with self.assertRaises(ValueError):
                evaluate(self.formula, {"x": value})

    def test_invalid_substitution_arguments(self):
        for variable, value in (("w", 2), ([], 2), ("x", -1), ("x", 32), ("x", True)):
            with self.assertRaises(ValueError):
                substitute_numeral(self.formula, variable, value)

    def test_unsupported_and_ill_typed_syntax(self):
        bad = ("forall x", Eq(Nat(0), "x"), Add(Nat(0), Nat(1)),
               Not(Nat(0)), And(Nat(0), Nat(1)), Eq(Nat(True), Nat(0)),
               Eq(Nat(32), Nat(0)), Eq(Var("w"), Nat(0)),
               Eq(Var([]), Nat(0)), Eq(Eq(Nat(0), Nat(0)), Nat(0)))
        for formula in bad:
            with self.subTest(formula=formula), self.assertRaises(ValueError):
                validate_formula(formula)

    def test_ast_size_bound(self):
        formula = Eq(Nat(0), Nat(0))
        for _ in range(MAX_AST_NODES):
            formula = Not(formula)
        with self.assertRaises(ValueError):
            validate_formula(formula)


class ProofTests(unittest.TestCase):
    def setUp(self):
        self.valid = (ProofStep(0, 0, 0), ProofStep(1, 1, 1), ProofStep(2, 2, 2))

    def test_valid_proof_and_its_code(self):
        self.assertTrue(check_proof(self.valid, 2))
        self.assertTrue(proof_relation(encode_proof(self.valid), 2))

    def test_target_is_last_line(self):
        self.assertFalse(check_proof(self.valid, 1))
        self.assertFalse(proof_relation(encode_proof(self.valid), 1))

    def test_false_axiom_rejected(self):
        self.assertFalse(check_proof((ProofStep(1, 0, 0),), 1))

    def test_axiom_reference_must_be_zero(self):
        self.assertFalse(check_proof((ProofStep(0, 0, 1),), 0))

    def test_future_or_self_reference_rejected(self):
        for ref in (0, 2, 3):
            self.assertFalse(check_proof((self.valid[0], ProofStep(1, 1, ref)), 1))

    def test_wrong_premise_rejected(self):
        self.assertFalse(check_proof((self.valid[0], ProofStep(2, 2, 1)), 2))

    def test_wrong_conclusion_rejected(self):
        self.assertFalse(check_proof((self.valid[0], ProofStep(2, 1, 1)), 2))

    def test_unknown_rule_rejected(self):
        self.assertFalse(check_proof((self.valid[0], ProofStep(1, 4, 1)), 1))

    def test_nonadjacent_prior_reference_allowed(self):
        proof = (ProofStep(0, 0, 0), ProofStep(0, 0, 0), ProofStep(1, 1, 1))
        self.assertTrue(check_proof(proof, 1))

    def test_empty_and_malformed_proofs(self):
        for proof in ((), None, "A", (None,), (ProofStep(True, 0, 0),),
                      (ProofStep(-1, 0, 0),), (ProofStep(4, 0, 0),),
                      (ProofStep(0, True, 0),), (ProofStep(0, 0, False),)):
            with self.subTest(proof=proof):
                self.assertFalse(check_proof(proof, 0))

    def test_invalid_target(self):
        for target in (-1, 4, True, "C", None):
            self.assertFalse(check_proof(self.valid, target))

    def test_malformed_proof_codes(self):
        for code in (0, 1, 10, True, None, encode((0,)), encode((0, 0)),
                     encode((0, 31, 0))):
            self.assertFalse(proof_relation(code, 0))

    def test_encoding_is_not_validation(self):
        bad = (ProofStep(1, 0, 0),)
        code = encode_proof(bad)
        self.assertEqual(decode(code), (1, 0, 0))
        self.assertFalse(proof_relation(code, 1))

    def test_proof_line_bound(self):
        proof = (ProofStep(0, 0, 0),) * (MAX_PROOF_LINES + 1)
        self.assertFalse(check_proof(proof, 0))
        with self.assertRaises(ValueError):
            encode_proof(proof)
        with self.assertRaises(ValueError):
            encode_proof(("A",))

    def test_bounded_failure_does_not_mean_unprovable(self):
        short = bounded_search(2, 2)
        longer = bounded_search(2, 3)
        self.assertIsNone(short.proof)
        self.assertIsNotNone(longer.proof)
        self.assertEqual(len(longer.proof), 3)
        self.assertTrue(check_proof(longer.proof, 2))

    def test_every_target_found_at_its_minimal_bound(self):
        for target in range(4):
            self.assertIsNone(bounded_search(target, target).proof)
            found = bounded_search(target, target + 1)
            self.assertTrue(check_proof(found.proof, target))
            self.assertEqual(len(found.proof), target + 1)

    def test_zero_bound(self):
        result = bounded_search(0, 0)
        self.assertIsNone(result.proof)
        self.assertEqual(result.candidates_checked, 0)

    def test_search_bounds_and_targets_validated(self):
        for bound in (-1, 9, True, 1.0):
            with self.assertRaises(ValueError):
                bounded_search(0, bound)
        for target in (-1, 4, True, "A"):
            with self.assertRaises(ValueError):
                bounded_search(target, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
