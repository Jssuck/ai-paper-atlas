import unittest
from fractions import Fraction as F
from scaled_ratios import Magnitude as M, Ratio, equal_oracle, mapped_probe, mismatch, ratio, regression_grid


class V4Tests(unittest.TestCase):
    def test_same_kind_within_pair(self):
        with self.assertRaisesRegex(ValueError, "one kind"):
            Ratio(M(2), M(3, "area"))

    def test_two_ratio_kinds_can_differ(self):
        self.assertTrue(equal_oracle(ratio(3, 2), ratio(6, 4, "area")))

    def test_kind_preserved_by_scaling(self):
        self.assertEqual(ratio(3, 2, "area").scale(2, 1), ratio(6, 2, "area"))

    def test_all_three_signs_and_index_map(self):
        r = ratio(3, 2)
        for p, q, expected in ((1, 2, 1), (1, 3, 0), (1, 4, -1)):
            self.assertEqual(mapped_probe(r, 2, 1, p, q), (expected, expected))

    def test_equal_ratio_values_can_change_and_sign_can_flip(self):
        left, right = ratio(3, 2), ratio(6, 4)
        a, b = left.scale(2, 1), right.scale(2, 1)
        self.assertTrue(equal_oracle(a, b))
        self.assertFalse(equal_oracle(left, a))
        self.assertEqual((left.sign(1, 2), a.sign(1, 2)), (-1, 1))

    def test_wrong_factor_only_on_one_side(self):
        left, right = ratio(3, 2).scale(2, 1), ratio(6, 4)
        self.assertFalse(equal_oracle(left, right))
        self.assertEqual(mismatch(left, right, 4), (1, 2, 1, -1))

    def test_bounded_false_positive(self):
        a, b = ratio(101, 100), ratio(102, 101)
        self.assertFalse(equal_oracle(a, b))
        self.assertIsNone(mismatch(a, b, 100))
        self.assertEqual(mismatch(a, b, 101), (100, 101, 0, -1))

    def test_equal_unequal_scale_pairs_with_same_quotient(self):
        self.assertTrue(equal_oracle(ratio(3, 2).scale(2, 3), ratio(6, 4).scale(4, 6)))

    def test_positive_integral_probes_and_integer_scales(self):
        r = ratio(F(3, 2), F(1, 4))
        for bad in (0, -1, True, F(1, 2), 1.0):
            with self.assertRaises(ValueError):
                r.scale(bad, 1)
            with self.assertRaises(ValueError):
                r.sign(1, bad)

    def test_requires_positive_exact_inputs(self):
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                ratio(1, bad)
        with self.assertRaises(TypeError):
            ratio(1.0, 1)

    def test_grid(self):
        self.assertEqual(regression_grid(), (432, 6912))
