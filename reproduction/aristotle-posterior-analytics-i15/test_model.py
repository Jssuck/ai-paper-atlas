"""unittest checks remain active under Python -O and -OO."""
import unittest
from itertools import product
from model import all_of, none_of, some_not, premises, subsets, witnesses, audit

F = frozenset


class DirectNegationTests(unittest.TestCase):
    def test_all_three_universal_negative_forms(self):
        report = audit()
        self.assertEqual(report['triples_per_form'], 4096)
        for form, row in report['forms'].items():
            with self.subTest(form=form):
                self.assertGreater(row['all_terms_nonempty'], 0)
                self.assertEqual(row['violations'], 0)

    def test_missing_genus_not_disjoint_even_if_conclusion_false(self):
        a, b, c = F({0, 1}), F({1, 2}), F({0, 1, 3})
        self.assertLess(a, c)
        self.assertFalse(all_of(c, b))  # Not all B are C.
        self.assertFalse(none_of(c, b))  # Does NOT imply no B are C.
        self.assertFalse(none_of(a, b))
        self.assertFalse(premises('Camestres', a, b, c))

    def test_true_conclusion_does_not_supply_missing_premise(self):
        a, b, c = F({0}), F({1, 2}), F({0, 1})
        self.assertTrue(none_of(a, b))
        self.assertTrue(all_of(c, a))
        self.assertFalse(all_of(c, b))
        self.assertFalse(none_of(c, b))

    def test_third_figure_only_particular_counterexample(self):
        a, b, m = F({0}), F({0, 1}), F({1})
        self.assertTrue(none_of(a, m))
        self.assertTrue(all_of(b, m))
        self.assertTrue(m)
        self.assertTrue(some_not(a, b))
        self.assertFalse(none_of(a, b))

    def test_third_figure_particular_finite_check(self):
        for a, b, m in product(subsets(3), repeat=3):
            if m and none_of(a, m) and all_of(b, m):
                self.assertTrue(some_not(a, b))

    def test_vocabulary_dependence_and_complement(self):
        a, b, u = F({0}), F({1}), F(range(4))
        self.assertTrue(none_of(a, b))
        self.assertEqual(witnesses(a, b, {'A': a, 'B': b}), [])
        self.assertEqual(witnesses(a, b, {'not_A': u-a}),
                         [('not_A', 'Celarent'), ('not_A', 'Cesare')])

    def test_complement_construction_for_all_disjoint_nonempty_pairs(self):
        u = F(range(4))
        for a, b in product(subsets(4), repeat=2):
            if a and b and none_of(a, b):
                self.assertTrue(premises('Celarent', a, b, u-a))
        # The construction can be circular/extentionally identical to B.
        self.assertEqual(u-F({0, 1, 2}), F({3}))

    def test_two_negative_premises_do_not_entail_disjointness(self):
        a, b, m = F({0}), F({0}), F({1})
        self.assertTrue(none_of(m, a) and none_of(m, b))
        self.assertFalse(none_of(a, b))

    def test_empty_subject_is_vacuous_not_scientific_evidence(self):
        self.assertTrue(all_of(F(), F()))
        self.assertTrue(none_of(F({0}), F()))
        self.assertFalse(some_not(F({0}), F()))

    def test_unknown_form_rejected(self):
        with self.assertRaises(ValueError):
            premises('invented', F(), F(), F())


if __name__ == '__main__':
    unittest.main(verbosity=2)
