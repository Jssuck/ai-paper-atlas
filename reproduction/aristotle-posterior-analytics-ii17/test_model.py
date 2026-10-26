"""Checks use unittest methods, remaining active under -O and -OO."""
import unittest
from fractions import Fraction
from itertools import product
from model import powerset, coverage, two_routes, extension_equivalence, alternation, enumerate_models

class ModelTests(unittest.TestCase):
    def test_powerset_size(self):
        self.assertEqual(len(powerset(3)), 8)
    def test_empty_domain(self):
        self.assertEqual(powerset(0), [frozenset()])
    def test_bad_domain(self):
        for value in (-1, 6, True, 1.5):
            with self.assertRaises(ValueError): powerset(value)
    def test_complete_strict_cover(self):
        r = coverage({0, 1}, ({0}, {1}))
        self.assertTrue(r['each_strict']); self.assertTrue(r['collectively_equal'])
    def test_incomplete_cover(self):
        self.assertEqual(coverage({0, 1, 2}, ({0}, {1}))['missing'], [2])
    def test_single_equal_species(self):
        self.assertFalse(coverage({0}, ({0},))['each_strict'])
    def test_overlap_allowed(self):
        self.assertTrue(coverage({0, 1, 2}, ({0, 1}, {1, 2}))['collectively_equal'])
    def test_invalid_species(self):
        with self.assertRaises(ValueError): coverage({0}, ({1},))
    def test_empty_catalog_not_exhaustive(self):
        self.assertFalse(coverage({0}, ())['collectively_equal'])
    def test_empty_universal_caution(self):
        r = coverage(set(), (set(),)); self.assertTrue(r['collectively_equal'])
        self.assertEqual(r['empty_species'], 1); self.assertFalse(r['each_strict'])
    def test_routes_entail(self):
        r = two_routes({0, 1}, {0}, {1}, {0}, {1})
        self.assertTrue(r['premises']); self.assertTrue(r['conclusion'])
    def test_reverse_not_entailed(self):
        r = two_routes({0, 1}, {0}, {1}, {0}, {1})
        self.assertFalse(r['effect_implies_b']); self.assertFalse(r['effect_implies_c'])
    def test_missing_route_premise(self):
        r = two_routes({0}, {0}, set(), {1}, set())
        self.assertFalse(r['premises']); self.assertFalse(r['conclusion'])
    def test_equal_middle_not_forbidden(self):
        r = two_routes({0}, {0}, {0}, {0}, {0})
        self.assertTrue(r['premises']); self.assertFalse(r['different_middle_extensions'])
    def test_equal_extension_not_explanation(self):
        r = extension_equivalence({0}, {0})
        self.assertTrue(r['same_extension']); self.assertEqual(r['causal_direction'], 'undetermined')
        self.assertEqual(r['same_definition'], 'undetermined')
    def test_unequal_extension_not_explanation(self):
        self.assertEqual(extension_equivalence({0}, {0, 1})['causal_direction'], 'undetermined')
    def test_alternation_example(self):
        self.assertEqual(alternation(2, 4, 3, 6), {'premise': True, 'conclusion': True})
    def test_exact_fraction(self):
        self.assertTrue(alternation(Fraction(1, 3), Fraction(2, 3), 1, 2)['conclusion'])
    def test_alternation_invalid_domain(self):
        for v in (0, -1):
            with self.assertRaises(ValueError): alternation(1, v, 2, 3)
    def test_alternation_finite_exhaustion(self):
        for values in product(range(1, 6), repeat=4):
            r = alternation(*values)
            if r['premise']: self.assertTrue(r['conclusion'], values)
    def test_route_exhaustion(self):
        r = enumerate_models(3)
        self.assertEqual(r['route_assignments'], 32768)
        self.assertEqual(r['route_conclusion_violations'], 0)
        self.assertGreater(r['reverse_b_failures_under_premises'], 0)
    def test_coverage_exhaustion_independent_count(self):
        r = enumerate_models(2)
        # Each point is absent from B, or in D1 only, D2 only, or both.
        self.assertEqual(r['complete_coverage_models'], 4**2)
        # Both strict requires a point only in D1 and a point only in D2.
        self.assertEqual(r['complete_each_strict_models'], 2)

if __name__ == '__main__': unittest.main()
