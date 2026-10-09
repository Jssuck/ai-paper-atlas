"""Positive checks, counterexamples, and deliberate-error detection (stdlib)."""
from fractions import Fraction
from itertools import product
import unittest

import sheffer as s


class HistoricalModelsTests(unittest.TestCase):
    def setUp(self):
        self.models = s.original_finite_models()

    def test_original_consistency_model(self):
        self.assertEqual(self.models['consistency'].signature(), (True,) * 5)

    def test_original_independence_signatures(self):
        for number in (1, 2, 3, 5):
            with self.subTest(postulate=number):
                expected = tuple(i != number for i in range(1, 6))
                self.assertEqual(self.models[f'independent_P{number}'].signature(), expected)

    def test_closure_is_not_built_into_krule(self):
        model = self.models['independent_P2']
        self.assertEqual(model('m', 'n'), 'outside')
        with self.assertRaises(s.OutsideK):
            model('outside', 'm')
        result = model.check()
        self.assertEqual(result['P2']['outside_count'], 2)
        self.assertEqual(result['P4']['guard_skipped'], 2)
        self.assertEqual(result['P5']['guard_skipped'], 6)

    def test_outside_priming_is_guarded_not_evaluated(self):
        model = s.FiniteKRule(('m', 'n'), ('outside',) * 4)
        result = model.check()
        self.assertEqual(result['P3']['guard_skipped'], 2)
        self.assertEqual(result['P3']['checked'], 0)
        self.assertTrue(result['P3']['holds'])  # conditional has false antecedent

    def test_incomplete_rule_rejected(self):
        with self.assertRaises(ValueError):
            s.FiniteKRule((0, 1), (0, 1))
        with self.assertRaises(ValueError):
            s.FiniteKRule((0, 0), (0, 0, 0, 0))

    def test_p3_failure_witness(self):
        witness = self.models['independent_P3'].check()['P3']['witness']
        self.assertEqual(witness, {'assignment': {'a': 'n'}, 'left': 'm', 'right': 'n'})

    def test_p5_transcription_and_failure_witness(self):
        model = self.models['independent_P5']
        self.assertEqual(model.values, ('l','m','n','n','n','l','m','l','m'))
        result = model.check()['P5']
        self.assertEqual(result['failures'], 16)
        self.assertEqual(result['witness'], {'assignment': {'a': 'l', 'b': 'l', 'c': 'm'},
                                            'left': 'n', 'right': 'm'})

    def test_rational_symbolic_p3_and_p5(self):
        result = s.rational_symbolic_results()
        self.assertTrue(result['P3']['holds_identically'])
        self.assertTrue(result['P5']['holds_identically'])
        self.assertEqual(result['P5']['left_coefficients_a_b_c'], ['1/2','-1/4','-1/4'])
        self.assertFalse(result['P4']['holds_identically'])
        self.assertEqual(result['P4_witness']['left'], '-1/2')
        self.assertEqual(result['P4_witness']['right'], '-1')

    def test_rational_spot_checks_not_a_finite_model_claim(self):
        inputs = [Fraction(-2), Fraction(-1, 2), Fraction(0), Fraction(1, 3), Fraction(2)]
        for a, b, c in product(inputs, repeat=3):
            env = dict(a=a, b=b, c=c)
            for label in ('P3', 'P5'):
                _, left, right = s.IDENTITIES[label]
                self.assertEqual(s.evaluate_term(left, env, s.rational_bar),
                                 s.evaluate_term(right, env, s.rational_bar))
        # A finite sample is not closed under the rule and is never presented as K.
        self.assertNotIn(s.rational_bar(Fraction(2), Fraction(1, 3)), inputs)

    def test_rational_large_integer_inputs_stay_exact(self):
        for value in (2**54 + 1, -(2**54 + 1), 10**100 + 1):
            with self.subTest(value=value):
                first_prime = s.rational_bar(value, value)
                self.assertIsInstance(first_prime, Fraction)
                self.assertEqual(first_prime, -value)
                self.assertEqual(s.rational_bar(first_prime, first_prime), value)
        self.assertEqual(s.rational_bar(2**54 + 1, 0), Fraction(-(2**54 + 1), 2))

    def test_rational_mixed_integer_fraction_inputs_stay_exact(self):
        for a, b in ((1, Fraction(1, 3)), (Fraction(-5, 7), 2), (1, 2)):
            actual = s.rational_bar(a, b)
            self.assertIsInstance(actual, Fraction)
            self.assertEqual(actual, -(Fraction(a) + Fraction(b)) / 2)

    def test_rational_rejects_floats_and_unsupported_inputs(self):
        zero_form = s.Linear((Fraction(0), Fraction(0), Fraction(0)))
        for a, b in ((0.5, 1), (1, 0.5), (float('inf'), 0),
                     (float('nan'), 0), ('1', 1), (True, 1),
                     (zero_form, 1), (1, zero_form)):
            with self.subTest(a=a, b=b), self.assertRaises(TypeError):
                s.rational_bar(a, b)

    def test_p4_holds_exactly_at_zero_a(self):
        _, left, right = s.IDENTITIES['P4']
        for a, b in product(map(Fraction, (-3, 0, 5)), repeat=2):
            env = dict(a=a, b=b)
            equality = (s.evaluate_term(left, env, s.rational_bar) ==
                        s.evaluate_term(right, env, s.rational_bar))
            self.assertEqual(equality, a == 0)


class ExhaustiveTableTests(unittest.TestCase):
    def test_guarded_and_fast_checkers_agree_on_every_small_closed_table(self):
        # Independent generic AST and direct-index evaluators, all 19,700 tables.
        checked = 0
        for n in (1, 2, 3):
            for values in product(range(n), repeat=n*n):
                model = s.FiniteKRule(tuple(range(n)), values)
                self.assertEqual(s.closed_signature(n, values), model.signature())
                checked += 1
        self.assertEqual(checked, 19700)

    def test_measured_small_order_counts_and_truth_tables(self):
        results = [s.enumerate_closed(n) for n in (1, 2, 3)]
        self.assertEqual([r['tables_examined'] for r in results], [1,16,19683])
        self.assertEqual([r['all_five_count'] for r in results], [0,2,0])
        self.assertEqual(results[1]['all_five_tables_row_major'], [[1,0,0,0],[1,1,1,0]])

    def test_enumeration_scope_guard(self):
        with self.assertRaises(ValueError):
            s.enumerate_closed(4)

    def test_nor_and_nand_are_distinct_but_both_models(self):
        nor = s.FiniteKRule((0,1), (1,0,0,0))
        nand = s.FiniteKRule((0,1), (1,1,1,0))
        self.assertEqual(nor.signature(), (True,)*5)
        self.assertEqual(nand.signature(), (True,)*5)
        self.assertNotEqual(nor(0,1), nand(0,1))
        for a,b in product((0,1), repeat=2):
            self.assertEqual(1-nor(1-a,1-b), nand(a,b))


class TranslationTests(unittest.TestCase):
    def test_parser_precedence_and_associativity(self):
        self.assertEqual(s.parse('~p | q & r'),
                         ('or',('not',('var','p')),('and',('var','q'),('var','r'))))
        self.assertEqual(s.parse('p -> q -> r'),
                         ('imp',('var','p'),('imp',('var','q'),('var','r'))))
        self.assertEqual(s.parse('  !p  '), s.parse('~p'))

    def test_parser_rejects_malformed_input(self):
        for text in ('', 'p q', 'p |', '(p | q', 'p)', 'p + q', '__import__(os)', 'p <-> q'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                s.parse(text)

    def test_original_p487_definitions(self):
        p, q = ('var','p'), ('var','q')
        self.assertEqual(s.translate(('not', p)), ('nor', p, p))
        self.assertEqual(s.translate(('or', p, q)), ('nor', ('nor',p,q), ('nor',p,q)))
        self.assertTrue(s.equivalent(s.parse('~p'), s.translate(s.parse('~p')))[0])
        self.assertTrue(s.equivalent(s.parse('p | q'), s.translate(s.parse('p | q')))[0])

    def test_exhaustive_bounded_translation(self):
        result = s.translation_experiment(2)
        self.assertEqual(result['source_formulas'], 74)
        self.assertEqual(result['formula_target_assignment_checks'], 592)
        self.assertEqual(result['mismatches'], 0)

    def test_extended_connectives_both_bases(self):
        examples = ('p', '~p', 'p | q', 'p & q', 'p -> q',
                    '(p -> q) & (q -> p)', '~(p | q) | r',
                    '(p & ~q) | (~p & q)', '(p -> q) -> ((q -> r) -> (p -> r))')
        for text in examples:
            for basis in ('nor', 'nand'):
                with self.subTest(text=text, basis=basis):
                    source = s.parse(text)
                    target = s.translate(source, basis)
                    self.assertTrue(s.gate_only(target, basis))
                    self.assertTrue(s.equivalent(source,target)[0])

    def test_deliberately_wrong_or_encoding_detected(self):
        source = s.parse('p | q')
        wrong = ('nor', ('var','p'), ('var','q'))  # omitted final self-rejection
        same, witness = s.equivalent(source, wrong)
        self.assertFalse(same)
        self.assertEqual(witness, {'p':False, 'q':False})

    def test_silently_swapping_nor_for_nand_is_detected(self):
        source = s.parse('p | q')
        p,q = ('var','p'),('var','q')
        wrong = ('nand', ('nand',p,q), ('nand',p,q))  # original NOR formula with name swapped
        self.assertFalse(s.equivalent(source, wrong)[0])

    def test_structural_validation_rejects_mixed_basis(self):
        self.assertFalse(s.gate_only(s.parse('p | q'), 'nor'))
        with self.assertRaises(ValueError):
            s.translate(s.parse('p'), 'xor')


if __name__ == '__main__':
    unittest.main(verbosity=2)
