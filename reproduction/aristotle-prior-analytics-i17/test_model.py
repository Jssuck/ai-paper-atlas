import unittest
from dataclasses import FrozenInstanceError
from itertools import product
from model import Model, FORMS, MODALITIES, models, examples
from demo import endpoint_checks, require


class TeachingTests(unittest.TestCase):
    def setUp(self):
        self.e = examples()

    def test_01_masks(self):
        self.assertEqual(self.e['disjoint'].extension('A'), frozenset((0, 1)))
        self.assertEqual(self.e['disjoint'].extension('A', 1), frozenset())

    def test_02_profile(self):
        self.assertEqual(self.e['conversion_failure'].profile('A', 0), (True, False))
        self.assertEqual(self.e['conversion_failure'].profile('A', 1), (True, True))

    def test_03_actual_forms(self):
        self.assertEqual([self.e['disjoint'].categorical('B', 'C', f) for f in FORMS],
                         [False, True, False, True])

    def test_04_necessary_forms(self):
        self.assertEqual([self.e['identical'].categorical('B', 'C', f, 'necessary') for f in FORMS],
                         [True, False, True, False])

    def test_05_contingency_quality(self):
        for m in self.e.values():
            self.assertEqual(m.categorical('A', 'B', 'A', 'contingent'), m.categorical('A', 'B', 'E', 'contingent'))
            self.assertEqual(m.categorical('A', 'B', 'I', 'contingent'), m.categorical('A', 'B', 'O', 'contingent'))

    def test_06_conversion_fails(self):
        m = self.e['conversion_failure']
        self.assertTrue(m.categorical('A', 'B', 'E', 'contingent'))
        self.assertFalse(m.categorical('B', 'A', 'E', 'contingent'))

    def test_07_positive_branch(self):
        self.assertEqual(self.e['necessary_positive'].noncontingency_witnesses('A', 'B'),
                         {'necessary_positive': [0], 'necessary_negative': []})

    def test_08_negative_branch(self):
        self.assertEqual(self.e['necessary_negative'].noncontingency_witnesses('A', 'B'),
                         {'necessary_positive': [], 'necessary_negative': [0]})

    def test_09_both_branches(self):
        self.assertEqual(self.e['mixed_fixed'].noncontingency_witnesses('A', 'B'),
                         {'necessary_positive': [0], 'necessary_negative': [1]})

    def test_10_fixed_not_contingent(self):
        for name in ('necessary_positive', 'necessary_negative', 'mixed_fixed'):
            self.assertFalse(self.e[name].categorical('A', 'B', 'A', 'contingent'))

    def test_11_weak_not_strong(self):
        self.assertTrue(self.e['necessary_negative'].categorical('A', 'B', 'E', 'possible'))
        self.assertFalse(self.e['necessary_negative'].categorical('A', 'B', 'E', 'contingent'))

    def test_12_not_necessary_not_necessary_negative(self):
        m = self.e['alternating_witnesses']
        self.assertFalse(m.categorical('A', 'B', 'A', 'necessary'))
        self.assertFalse(m.categorical('A', 'B', 'E', 'necessary'))

    def test_13_joint_quantifier_failure(self):
        m = self.e['alternating_witnesses']
        self.assertTrue(m.categorical('A', 'B', 'A', 'contingent'))
        self.assertFalse(m.jointly_possible('A', 'B'))
        self.assertFalse(m.jointly_possible('A', 'B', False))

    def test_14_all_second_figure_pairs(self):
        rows = endpoint_checks()
        self.assertEqual(len(rows), 16)
        self.assertTrue(all(len(r['countermodels']) == 16 for r in rows))

    def test_15_no_contingent_endpoint(self):
        for name, form in product(('disjoint', 'identical'), FORMS):
            self.assertFalse(self.e[name].categorical('B', 'C', form, 'contingent'))

    def test_16_actual_anchor(self):
        m = Model(1, ((1, 1, 1), (0, 0, 1)), 1)
        self.assertTrue(m.categorical('A', 'B', 'A'))
        self.assertFalse(m.categorical('A', 'B', 'I'))
        self.assertFalse(m.categorical('A', 'C', 'A'))

    def test_17_empty_subject(self):
        m = Model(1, ((1, 0, 1),))
        for mode in MODALITIES:
            self.assertEqual([m.categorical('A', 'B', f, mode) for f in FORMS], [True, True, False, False])
        self.assertEqual(m.noncontingency_witnesses('A', 'B'), {'necessary_positive': [], 'necessary_negative': []})

    def test_18_single_world(self):
        m = Model(1, ((1, 1, 1),))
        self.assertFalse(m.categorical('A', 'B', 'A', 'contingent'))
        self.assertTrue(m.categorical('A', 'B', 'A', 'necessary'))

    def test_19_models_count(self):
        self.assertEqual(sum(1 for _ in models(1)), 128)
        self.assertEqual(sum(1 for _ in models(1, 1)), 8)

    def test_20_bad_constructors(self):
        cases = [(0, ((0, 0, 0),), 0), (True, ((0, 0, 0),), 0), (1, [], 0),
                 (1, (), 0), (1, ([0, 0, 0],), 0), (1, ((0, 0),), 0),
                 (1, ((2, 0, 0),), 0), (1, ((True, 0, 0),), 0),
                 (1, ((-1, 0, 0),), 0), (1, ((0, 0, 0),), True),
                 (1, ((0, 0, 0),), 1), (1, ((0, 0, 0),), -1)]
        for args in cases:
            with self.subTest(args=args), self.assertRaises(ValueError):
                Model(*args)

    def test_21_bad_methods(self):
        m = self.e['disjoint']
        calls = [lambda: m.extension('D'), lambda: m.extension([]), lambda: m.extension('A', True),
                 lambda: m.extension('A', 2), lambda: m.profile('A', True), lambda: m.profile('A', 2),
                 lambda: m.categorical('A', 'B', 'X'), lambda: m.categorical('A', 'B', 'A', 'X'),
                 lambda: m.noncontingency_witnesses('D', 'B'), lambda: m.jointly_possible('A', 'B', 1)]
        for call in calls:
            with self.assertRaises(ValueError):
                call()
        with self.assertRaises(ValueError):
            Model(1, ((0, 0, 0),)).categorical('D', 'B')

    def test_22_bad_enumerators(self):
        for args in ((0,), (True,), (1, 0), (1, True)):
            with self.assertRaises(ValueError):
                list(models(*args))

    def test_23_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            self.e['disjoint'].actual = 1

    def test_24_runtime_checks_survive_optimization(self):
        with self.assertRaises(RuntimeError):
            require(False, 'expected')


if __name__ == '__main__':
    unittest.main(verbosity=2)
