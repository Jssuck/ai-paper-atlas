from fractions import Fraction
from itertools import product
import unittest

from ratio_scaling import partition_trace, signature


class RatioScalingTests(unittest.TestCase):
    def test_less(self):
        self.assertEqual(partition_trace(2, 3, 4, 1, 1)["total_sign"], -1)

    def test_equal(self):
        self.assertEqual(partition_trace(2, 3, 4, 3, 2)["total_sign"], 0)

    def test_greater(self):
        self.assertEqual(partition_trace(2, 3, 4, 2, 1)["total_sign"], 1)

    def test_partition(self):
        t = partition_trace(2, 3, 4, 1, 1)
        self.assertEqual(t["parts"], ((2, 3),) * 4)
        self.assertEqual(t["total"], (8, 12))
        self.assertEqual(t["part_signs"], (-1,) * 4)
        self.assertEqual(t["total_ratio"], Fraction(2, 3))

    def test_factor_one(self):
        self.assertEqual(partition_trace(5, 7, 1, 7, 5)["total"], (5, 7))

    def test_rational(self):
        c, f = Fraction(2, 3), Fraction(5, 6)
        t = partition_trace(c, f, 3, 5, 4)
        self.assertEqual(t["total"], (2, Fraction(5, 2)))
        self.assertEqual(t["part_ratio"], Fraction(4, 5))
        self.assertEqual(t["total_sign"], 0)

    def test_mismatched_factors(self):
        self.assertEqual(signature(2, 3, 3, 2), 0)
        self.assertEqual(signature(4, 9, 3, 2), -1)

    def test_invalid_magnitude(self):
        for a, error in ((0, ValueError), (-1, ValueError), (True, TypeError), (0.5, TypeError)):
            with self.subTest(a=a), self.assertRaises(error):
                partition_trace(a, 2, 3, 1, 1)

    def test_invalid_multiplier(self):
        for k, error in ((0, ValueError), (-1, ValueError), (True, TypeError), (Fraction(3), TypeError)):
            with self.subTest(k=k), self.assertRaises(error):
                partition_trace(2, 3, k, 1, 1)
        with self.assertRaises(ValueError):
            partition_trace(2, 3, 2, 1, 0)

    def test_grid(self):
        cases = 0
        signs = {-1: 0, 0: 0, 1: 0}
        for c, f, k, m, n in product(range(1, 5), repeat=5):
            t = partition_trace(c, f, k, m, n)
            ratio, threshold = Fraction(c, f), Fraction(n, m)
            expected = (ratio > threshold) - (ratio < threshold)
            self.assertEqual(t["part_signs"], (expected,) * k)
            self.assertEqual(t["total_sign"], expected)
            self.assertEqual(t["total_ratio"], ratio)
            signs[expected] += 1
            cases += 1
        self.assertEqual(cases, 1024)
        self.assertEqual(signs[-1], signs[1])
        self.assertGreater(signs[0], 0)
