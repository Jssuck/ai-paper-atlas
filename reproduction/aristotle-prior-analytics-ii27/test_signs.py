import unittest
from signs import evaluate, enumerate_models, mappings, majority_example, identification_example


class SignsTests(unittest.TestCase):
    def test_first_chain(self):
        self.assertEqual(evaluate(7, 3, 1)['first'], (True, True))

    def test_false_bridge_not_proof(self):
        self.assertEqual(evaluate(1, 3, 2)['first'], (False, False))

    def test_second_nonempty_countermodel(self):
        self.assertEqual(evaluate(3, 1, 2)['second_affirmative'], (True, False))

    def test_second_can_have_true_conclusion(self):
        self.assertEqual(evaluate(3, 1, 1)['second_affirmative'], (True, True))

    def test_third_witness(self):
        self.assertEqual(evaluate(1, 3, 1)['third_particular'], (True, True))

    def test_third_universal_countermodel(self):
        self.assertEqual(evaluate(1, 3, 1)['third_universal_overreach'], (True, False))

    def test_empty_middle_not_witness(self):
        self.assertEqual(evaluate(0, 0, 0)['third_particular'], (False, False))
        self.assertEqual(evaluate(0, 0, 0)['third_missing_existence'], (True, False))

    def test_correlative_with_strictly_smaller_kind(self):
        self.assertEqual(evaluate(3, 3, 1)['correlative_sign'], (True, True))

    def test_converse_only_countermodel(self):
        self.assertEqual(evaluate(1, 3, 2)['one_way_sign_inverse'], (True, False))

    def test_invalid_masks(self):
        for masks in ((-1, 0, 0), (True, 0, 0), (0.0, 0, 0)):
            with self.assertRaises(ValueError):
                evaluate(*masks)

    def test_majority_is_not_universal(self):
        result = majority_example()
        self.assertEqual(result['frequency'], '9/10')
        self.assertTrue(result['strict_majority'])
        self.assertFalse(result['universal'])
        self.assertEqual(result['exception_index'], 9)

    def test_mapping_no_observations(self):
        self.assertEqual(mappings([]), [[0, 1], [1, 0]])

    def test_mapping_cooccurrence_ambiguous(self):
        self.assertEqual(identification_example()['cooccurrence_mappings'], [[0, 1], [1, 0]])

    def test_mapping_separation_conditional(self):
        self.assertEqual(identification_example()['separated_mappings'], [[0, 1]])

    def test_mapping_extension_can_refute(self):
        self.assertEqual(identification_example()['extended_mappings'], [])

    def test_mapping_input_validation(self):
        for rows in ([(True,)], [(1, True, False, True)]):
            with self.assertRaises(ValueError):
                mappings(rows)

    def test_enumeration_boundary(self):
        self.assertEqual(enumerate_models(0)['worlds'], 1)
        for n in (-1, 7, True, 1.5):
            with self.assertRaises(ValueError):
                enumerate_models(n)

    def test_complete_small_domain_routes(self):
        result = enumerate_models(4)
        self.assertEqual(result['worlds'], sum(8 ** n for n in range(5)))
        for name in ('first', 'third_particular', 'correlative_sign'):
            self.assertEqual(result['routes'][name]['countermodels'], 0)
            self.assertGreater(result['routes'][name]['premise_models'], 0)
        for name in ('second_affirmative', 'third_universal_overreach',
                     'third_missing_existence', 'one_way_sign_inverse'):
            self.assertGreater(result['routes'][name]['countermodels'], 0)
        for name in ('second_affirmative', 'third_universal_overreach', 'one_way_sign_inverse'):
            self.assertEqual(result['routes'][name]['first_all_nonempty_countermodel']['n'], 2)


if __name__ == '__main__':
    unittest.main()
