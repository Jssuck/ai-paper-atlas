"""Eight tests; the finite grid checks implementation, not a general proof."""

from fractions import Fraction
from itertools import product
import unittest

from demo import Pair, build_results, remark, unrestricted_remark


class RemarkTests(unittest.TestCase):
    def test_exact_rationals_and_reject_float(self):
        self.assertEqual(Pair("1/3", "2/7") + Pair("2/3", "5/7"), Pair(1, 1))
        with self.assertRaises(TypeError):
            Pair(0.1)

    def test_pair_arithmetic(self):
        self.assertEqual(Pair(0, 1) * Pair(0, 1), Pair(-1))
        self.assertEqual(Pair(2, 3) - Pair(1, 5), Pair(1, -2))
        self.assertEqual(Pair(2, 3) * Pair(4, -5), Pair(23, 2))

    def test_signed_differences(self):
        cases = build_results()
        self.assertEqual([x["difference"] for x in cases["signed_real_differences"]],
                         ["2", "-2", "0"])
        self.assertEqual([remark(2, b, 3, c) for b, c in [(5, 3), (3, 5), (3, 3)]],
                         [Pair(5, 2), Pair(5, -2), Pair(5)])

    def test_real_iff_equal_grid_625_cases(self):
        grid = [Fraction(-2), Fraction(-1, 2), Fraction(0), Fraction(1, 2), Fraction(2)]
        for a, b, f, c in product(grid, repeat=4):
            with self.subTest(a=a, b=b, f=f, c=c):
                value = remark(a, b, f, c)
                self.assertEqual(value, Pair(a + f, b - c))
                self.assertEqual(value.is_real, b == c)

    def test_nonunique_decomposition(self):
        self.assertEqual(remark(2, 5, 3, 3), Pair(5, 2))
        self.assertEqual(remark(1, 9, 4, 7), Pair(5, 2))

    def test_nonreal_intermediates_cancel(self):
        left, right = Pair(2, 3), Pair(3, -3)
        self.assertFalse(left.is_real)
        self.assertFalse(right.is_real)
        self.assertEqual(left + right, Pair(5))
        self.assertEqual(Pair(1, 1) * Pair(1, -1), Pair(2))

    def test_positive_length_constraint(self):
        for root in [Fraction(1), Fraction(-4)]:
            self.assertEqual(root * root + 3 * root - 4, 0)
        result = build_results()["positive_length_constraint"]
        self.assertEqual(result["real_roots"], ["1", "-4"])
        self.assertEqual(result["admissible_roots"], ["1"])
        self.assertEqual(result["excluded_real_roots"], ["-4"])

    def test_complex_coefficients_break_both_directions(self):
        # b=c is not sufficient when a has a nonzero imaginary part.
        self.assertEqual(unrestricted_remark(Pair(0, 1), 1, Pair(), 1), Pair(0, 1))
        # b=c is not necessary when a supplies the cancelling imaginary part.
        self.assertEqual(unrestricted_remark(Pair(0, -1), 2, Pair(), 1), Pair())


if __name__ == "__main__":
    unittest.main(verbosity=2)
