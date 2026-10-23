import unittest
from model import Model, MOODS, classify, evaluate, examples, make, proposition, signature, type_models
from run_experiment import run


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.m = make({0}, {0, 1}, {0})

    def test_A_direction(self):
        self.assertTrue(proposition(self.m, 'A', 'C', 'A'))
        self.assertFalse(proposition(self.m, 'A', 'B', 'A'))

    def test_E(self):
        self.assertFalse(proposition(self.m, 'E', 'B', 'A'))

    def test_I(self):
        self.assertTrue(proposition(self.m, 'I', 'B', 'A'))

    def test_O(self):
        self.assertTrue(proposition(self.m, 'O', 'B', 'A'))

    def test_empty_subject_not_wholly_false(self):
        m = make({0}, set(), set())
        for k in ('A', 'E'):
            self.assertEqual(classify(m, k, 'B', 'A'), 'vacuous_true')
        self.assertEqual(classify(m, 'I', 'B', 'A'), 'false')
        self.assertEqual(classify(m, 'O', 'B', 'A'), 'false')

    def test_wholly_false_A(self):
        self.assertEqual(classify(make({0}, {1}, {0}), 'A', 'B', 'A'), 'wholly_false')

    def test_wholly_false_E(self):
        self.assertEqual(classify(make({0}, {0}, {1}), 'E', 'B', 'A'), 'wholly_false')

    def test_mixed_is_partly_false_for_both_universals(self):
        for k in ('A', 'E'):
            self.assertEqual(classify(self.m, k, 'B', 'A'), 'partly_false')

    def test_true_universal(self):
        self.assertEqual(classify(self.m, 'A', 'C', 'A'), 'true')

    def test_all_sound(self):
        for m in type_models():
            for mood in MOODS:
                self.assertNotEqual(evaluate(m, mood), (True, True, False))

    def test_universal_major_restriction(self):
        for m in type_models(True):
            for mood in ('Barbara', 'Celarent'):
                major, minor, conclusion = evaluate(m, mood)
                if classify(m, *MOODS[mood][0]) == 'wholly_false' and minor:
                    self.assertFalse(conclusion)

    def test_empty_C_exception(self):
        for name in ('empty_C_Barbara_exception', 'empty_C_Celarent_exception'):
            m, mood = examples()[name]
            self.assertEqual(signature(m, mood), 'FTT')
            self.assertEqual(classify(m, *MOODS[mood][0]), 'wholly_false')

    def test_both_wholly_false_true(self):
        for name in ('both_wholly_false_Barbara', 'both_wholly_false_Celarent'):
            m, mood = examples()[name]
            self.assertEqual(signature(m, mood), 'FFT')
            self.assertEqual(classify(m, *MOODS[mood][0]), 'wholly_false')
            self.assertEqual(classify(m, *MOODS[mood][1]), 'wholly_false')

    def test_distinct_existential_witnesses(self):
        for name in ('Darii_distinct_witnesses', 'Ferio_distinct_witnesses'):
            m, mood = examples()[name]
            self.assertEqual(signature(m, mood), 'FTT')
            expected = m.C & m.A if mood == 'Darii' else m.C - m.A
            self.assertTrue(expected)
            self.assertTrue(m.C & m.B)
            self.assertFalse(expected & m.B)

    def test_false_particular_minor_true_conclusion(self):
        for name in ('Darii_false_minor', 'Ferio_false_minor'):
            m, mood = examples()[name]
            self.assertEqual(signature(m, mood), 'TFT')

    def test_type_models_unique(self):
        models = list(type_models())
        self.assertEqual(len(models), 255)
        self.assertEqual(len(set(models)), 255)
        self.assertTrue(all(m.B and m.C for m in type_models(True)))

    def test_no_empty_universe(self):
        with self.assertRaises(ValueError):
            make([], [], [])

    def test_outside_universe(self):
        with self.assertRaises(ValueError):
            make({1}, set(), set(), {0})

    def test_input_types(self):
        with self.assertRaises(TypeError):
            Model({0}, frozenset(), frozenset(), frozenset())
        with self.assertRaises(TypeError):
            make({True}, set(), set())
        with self.assertRaises(TypeError):
            proposition(None, 'A', 'A', 'B')
        with self.assertRaises(TypeError):
            list(type_models(1))

    def test_bad_syntax(self):
        with self.assertRaises(ValueError):
            proposition(self.m, 'X', 'A', 'B')
        with self.assertRaises(ValueError):
            proposition(self.m, 'A', 'X', 'B')
        with self.assertRaises(ValueError):
            evaluate(self.m, 'unknown')

    def test_full_experiment(self):
        data = run()
        self.assertEqual(data['empty_terms_allowed']['mood_evaluations'], 1020)
        self.assertEqual(len(data['examples']), 12)

if __name__ == '__main__':
    unittest.main()
