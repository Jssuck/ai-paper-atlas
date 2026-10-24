import unittest
from fractions import Fraction
from model import coverage_report, available_routes, extensional_candidates, alternation, enumerate_models


class ModelTests(unittest.TestCase):
    def test_exhaustive_sound_parts(self):
        self.assertTrue(coverage_report(7, 7, (1, 2, 4), 3)['extensional_certificate'])
    def test_missing_part(self):
        r = coverage_report(7, 3, (1, 2), 3)
        self.assertEqual(r['missing_mask'], 4)
        self.assertFalse(r['extensional_certificate'])
    def test_overlap_allowed(self):
        self.assertTrue(coverage_report(7, 7, (3, 6), 3)['extensional_certificate'])
    def test_false_part(self):
        self.assertEqual(coverage_report(7, 3, (7,), 3)['part_counterexamples_mask'], 4)
    def test_empty_target(self):
        self.assertTrue(coverage_report(0, 0, (), 0)['target_true'])
    def test_no_parts_nonempty(self):
        self.assertFalse(coverage_report(1, 1, (), 1)['covered'])
    def test_truth_not_certificate(self):
        r = coverage_report(7, 7, (1,), 3)
        self.assertTrue(r['target_true'])
        self.assertFalse(r['extensional_certificate'])
    def test_outside_irrelevant_counterexample(self):
        r = coverage_report(1, 1, (3,), 2)
        self.assertTrue(r['target_true'])
        self.assertFalse(r['all_parts_sound'])
    def test_outside_mask(self):
        self.assertEqual(coverage_report(1, 3, (3,), 2)['outside_target_mask'], 2)
    def test_bad_masks(self):
        for mask in (-1, 8, True):
            with self.assertRaises(ValueError):
                coverage_report(mask, 0, (), 3)
    def test_bad_size(self):
        for size in (-1, True, 1.5):
            with self.assertRaises(ValueError):
                coverage_report(0, 0, (), size)
    def test_invalid_part(self):
        with self.assertRaises(ValueError):
            coverage_report(1, 1, (4,), 2)
    def test_bronze_removed(self):
        self.assertEqual(available_routes(({'triangle'},), {'triangle', 'isosceles'}), (0,))
    def test_isosceles_removed(self):
        self.assertEqual(available_routes(({'triangle'},), {'triangle'}), (0,))
    def test_triangle_removed(self):
        self.assertEqual(available_routes(({'triangle'},), {'figure', 'limit'}), ())
    def test_alternative_routes(self):
        self.assertEqual(available_routes(({'triangle'}, {'axiom'}), {'axiom'}), (1,))
    def test_empty_route_is_declared_assumption(self):
        self.assertEqual(available_routes((set(),), set()), (0,))
    def test_coextensional_labels_not_distinguished(self):
        c = {'triangle': 7, 'isosceles_in_restricted_sample': 7, 'empty': 0}
        self.assertEqual(extensional_candidates(c, 7, 3), tuple(c))
    def test_ratio_valid(self):
        self.assertEqual(alternation(2, 4, 3, 6), {'premise': True, 'conclusion': True})
    def test_ratio_false(self):
        self.assertFalse(alternation(1, 2, 3, 4)['premise'])
    def test_ratio_rational(self):
        self.assertTrue(alternation(Fraction(1, 2), 1, Fraction(3, 2), 3)['conclusion'])
    def test_ratio_rejects_undefined_or_out_of_scope(self):
        for bad in (0, -1, 1.5, True):
            with self.assertRaises(ValueError):
                alternation(bad, 1, 1, 1)
    def test_enumeration(self):
        r = enumerate_models()
        self.assertEqual((r['coverage_cases'], r['support_cases'], r['ratio_cases']), (4096, 64, 1296))
        for key in ('coverage_oracle_mismatches', 'coverage_implication_failures', 'support_oracle_mismatches', 'ratio_implication_failures'):
            self.assertEqual(r[key], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
