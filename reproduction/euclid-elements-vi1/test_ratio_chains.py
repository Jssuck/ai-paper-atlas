from fractions import Fraction as F
from itertools import product
import unittest

from ratio_chains import determinant, fan, probe, sqrt2_probe


class VI1Tests(unittest.TestCase):
    def test_exact_signed_determinant(self):
        self.assertEqual(determinant((F(1, 3), 2), (3, 5)), F(-13, 3))

    def test_fan_reconstructs_whole(self):
        for direction in (-1, 1):
            total_base, pieces, area, parallelogram = fan(
                F(3, 2), F(5, 3), 6, direction=direction, apex_x=8, shear=-3
            )
            self.assertEqual(total_base, 9)
            self.assertEqual(pieces, (F(5, 4),) * 6)
            self.assertEqual(sum(pieces), area)
            self.assertEqual(parallelogram, 2 * area)

    def test_comparison_three_branches(self):
        for m, n, expected in ((1, 1, -1), (3, 2, 0), (4, 2, 1)):
            self.assertEqual(probe(2, 3, 4, 4, m, n)[2], (expected,) * 3)

    def test_unequal_height_reverses_first_comparison(self):
        self.assertEqual(probe(2, 3, 4, 2, 1, 1)[2], (-1, 1, 1))

    def test_original_multipliers_independent(self):
        left, right, comparison = probe(3, 8, 3, 3, 4, 2)
        self.assertEqual((left[0], right[0], len(left[1]), len(right[1])), (12, 16, 4, 2))
        self.assertEqual(comparison, (-1, -1, -1))

    def test_exact_irrational_probes(self):
        for m, n, expected in ((1, 1, -1), (2, 1, 1), (99, 70, 1), (239, 169, -1)):
            self.assertEqual(sqrt2_probe(m, n), (expected,) * 3)

    def test_integer_grid_against_independent_oracle(self):
        count = 0
        for a, b, h, m, n in product(range(1, 5), repeat=5):
            left, right, actual = probe(a, b, h, h, m, n)
            delta = a*m - b*n
            expected = 0 if delta == 0 else (1 if delta > 0 else -1)
            self.assertEqual(actual, (expected,) * 3)
            self.assertEqual((2 * left[2], 2 * right[2]), (a*m*h, b*n*h))
            self.assertEqual(left[3] * b*n, right[3] * a*m)
            count += 1
        self.assertEqual(count, 1024)
        print(f"grid: {count} same-height (a,b,h,m,n) tuples")

    def test_domain(self):
        for args in ((0, 2, 1), (1, 0, 1), (1, 2, 0), (1, 2, True)):
            with self.assertRaises(ValueError):
                fan(*args)
        with self.assertRaises(TypeError):
            fan(1.5, 2, 1)
        with self.assertRaises(ValueError):
            fan(1, 2, 1, direction=0)
        with self.assertRaises(ValueError):
            sqrt2_probe(1, F(2))
