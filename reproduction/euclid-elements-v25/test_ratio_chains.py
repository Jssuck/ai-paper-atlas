"""Run the exact examples and explicitly bounded sensitivity checks."""
from collections import Counter
from fractions import Fraction
from itertools import product
import unittest

from ratio_chains import joyce_signs, parameterized, v25


class V25Tests(unittest.TestCase):
    def test_classical_trace(self):
        t = v25(12, 6, 8, 4)
        self.assertEqual(t.copied_parts, (8, 4))
        self.assertEqual(t.remainders, (4, 2))
        self.assertEqual(t.common_ratio, 2)
        self.assertEqual(t.equal_addends, (12, 12))
        self.assertEqual(t.sums, (16, 14))
        self.assertEqual(t.gap, 2)

    def test_equal_middle_terms_am_gm(self):
        t = v25(9, 6, 6, 4)
        self.assertEqual(t.sums, (13, 12))
        self.assertEqual(t.gap / 2, Fraction(1, 2))

    def test_exact_parameters(self):
        q, g = parameterized(Fraction(3, 2), Fraction(4, 3), Fraction(5, 4))
        self.assertEqual(q, (Fraction(5, 2), Fraction(15, 8), 2, Fraction(3, 2)))
        self.assertEqual(g, Fraction(1, 8))
        self.assertEqual(v25(*q).gap, g)

    def test_invalid_domain(self):
        for value in (0, -1, Fraction(-1, 2)):
            with self.subTest(value=value), self.assertRaises(ValueError):
                v25(value, 6, 8, 4)
        for value in (True, 12.0, "12"):
            with self.subTest(value=value), self.assertRaises(TypeError):
                v25(value, 6, 8, 4)

    def test_degenerate_ties(self):
        for q in ((4, 4, 2, 2), (4, 2, 4, 2), (4, 4, 4, 4)):
            self.assertEqual(q[0] * q[3], q[1] * q[2])
            self.assertEqual(q[0] + q[3], q[1] + q[2])
            with self.subTest(q=q), self.assertRaises(ValueError):
                v25(*q)
        for r, s in ((1, 2), (2, 1), (1, 1)):
            with self.subTest(r=r, s=s), self.assertRaises(ValueError):
                parameterized(1, r, s)

    def test_labels_and_false_converse(self):
        with self.assertRaises(ValueError):
            v25(4, 2, 8, 4)  # proportional, but the labels do not place the extrema
        self.assertGreater(10 + 1, 4 + 5)
        with self.assertRaises(ValueError):
            v25(10, 4, 5, 1)  # the inequality alone does not give proportionality

    def test_exact_integer_grid(self):
        vals = range(1, 13)
        n, accepted = 0, 0
        for a, b, c, d in product(vals, repeat=4):
            n += 1
            # Independent criterion: d<b,c and a is the exact product quotient.
            q, rem = divmod(b * c, d)
            eligible = d < b and d < c and rem == 0 and q == a
            try:
                t = v25(a, b, c, d)
            except ValueError:
                self.assertFalse(eligible)
            else:
                self.assertTrue(eligible)
                self.assertGreater(t.gap, 0)
                self.assertEqual(t.gap * d, (b - d) * (c - d))
                accepted += 1
        self.assertEqual(n, 20736)
        independently_counted = Counter()
        for d in vals:
            for b, c in product(range(d + 1, 13), repeat=2):
                if b*c % d == 0 and b*c // d <= 12:
                    independently_counted[d] += 1
        self.assertEqual(accepted, independently_counted.total())
        print(f"grid: {n} integer quadruples, {accepted} strictly admissible")

    def test_non_archimedean_boundary(self):
        for m, n in product(range(1, 13), repeat=2):
            first, second, conclusion = joyce_signs(m, n)
            expected = 1 if m >= n else -1
            self.assertEqual((first, second), (expected, expected))
            self.assertEqual(conclusion, 1 if m > n else -1)


if __name__ == "__main__":
    unittest.main()
