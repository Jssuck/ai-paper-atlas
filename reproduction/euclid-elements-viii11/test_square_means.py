import unittest
from fractions import Fraction
from math import gcd
from square_means import from_sides, integer_mean, is_mean


class SquareMeansTests(unittest.TestCase):
    def test_source_construction(self):
        self.assertEqual(from_sides(4, 6),
                         ((16, 24, 36), Fraction(2, 3), Fraction(4, 9)))
        self.assertEqual(from_sides(6, 4),
                         ((36, 24, 16), Fraction(3, 2), Fraction(9, 4)))

    def test_side_grid(self):
        for c in range(2, 16):
            for d in range(2, 16):
                with self.subTest(c=c, d=d):
                    (a, e, b), side, full = from_sides(c, d)
                    self.assertTrue(is_mean(a, e, b))
                    self.assertEqual(Fraction(a, e), Fraction(e, b))
                    self.assertEqual(Fraction(e, b), side)
                    self.assertEqual(full, side**2)
                    self.assertEqual(integer_mean(a, b), e)
        print("196 ordered side pairs (2..15), including equal sides.")

    def test_independent_merged_multiple_oracle(self):
        # Oracles: an enumeration of all possible middles, and reduced
        # endpoints checked against a precomputed finite table of squares.
        squares = {i*i for i in range(1, 37)}
        solutions = 0
        for a in range(1, 37):
            for b in range(1, 37):
                brute = [e for e in range(min(a,b), max(a,b)+1)
                         if a*b == e*e]
                g = gcd(a, b)
                self.assertLessEqual(len(brute), 1)
                self.assertEqual(bool(brute), a//g in squares and b//g in squares)
                self.assertEqual(integer_mean(a, b), brute[0] if brute else None)
                solutions += len(brute)
        print(f"1296 ordered endpoint pairs (1..36); {solutions} with a mean.")

    def test_counterexamples_and_boundaries(self):
        self.assertEqual(integer_mean(8, 18), 12)
        self.assertIsNone(integer_mean(4, 10))
        self.assertFalse(is_mean(16, 26, 36))
        self.assertEqual(integer_mean(49, 49), 49)
        self.assertEqual(integer_mean(1, 49), 7)
        # Exact case beyond ordinary binary64 precision.
        c, d = 10**70 + 1, 10**70 + 3
        self.assertEqual(integer_mean(c*c, d*d), c*d)
        self.assertIsNone(integer_mean(1, c*c + 1))

    def test_invalid(self):
        for value in (0, -1, True, 1.0, "1", None):
            for fn, args in ((from_sides, (value, 2)),
                             (integer_mean, (2, value)),
                             (is_mean, (2, value, 2))):
                with self.subTest(value=value, fn=fn):
                    with self.assertRaises(ValueError):
                        fn(*args)


if __name__ == "__main__":
    unittest.main()
