import itertools
import unittest
from collections import Counter
from fractions import Fraction

from ratio_chains import Magnitude, Trace, chain, verify_v21


class ChainTests(unittest.TestCase):
    def checked(self, left, right):
        return verify_v21(chain(left, "line"), chain(right, "area"))

    def test_greater(self):
        self.assertEqual(
            self.checked((6, 4, 3), (8, 6, 4)),
            Trace(Fraction(3, 2), Fraction(3, 4),
                  Fraction(3, 2), Fraction(3, 4), 1),
        )

    def test_equal(self):
        self.assertEqual(self.checked((6, 4, 6), (8, 12, 8)).sign, 0)

    def test_less(self):
        self.assertEqual(self.checked((3, 4, 6), (4, 6, 8)).sign, -1)

    def test_each_perturbed_pair_needed_for_order(self):
        for right, pair in (((3, 6, 4), "second"), ((8, 6, 10), "first")):
            with self.subTest(right=right):
                self.assertLess(right[0], right[2])
                with self.assertRaisesRegex(ValueError, f"^{pair} perturbed"):
                    self.checked((6, 4, 3), right)

    def test_distinguishes_ordered_from_perturbed_hypotheses(self):
        a, b, c = 6, 4, 3
        for (d, e, f), ordered, perturbed in (
            ((12, 8, 6), True, False),
            ((8, 6, 4), False, True),
        ):
            with self.subTest(right=(d, e, f)):
                self.assertEqual(a * e == b * d and b * f == c * e, ordered)
                self.assertGreater(d, f)  # all edges' products agree under either alignment
                if perturbed:
                    self.assertEqual(self.checked((a, b, c), (d, e, f)).sign, 1)
                else:
                    with self.assertRaises(ValueError):
                        self.checked((a, b, c), (d, e, f))

    def test_kind_guard(self):
        bad = (Magnitude(6, "line"), Magnitude(4, "area"), Magnitude(3, "line"))
        with self.assertRaisesRegex(ValueError, "^a ratio"):
            verify_v21(bad, chain((8, 6, 4), "area"))

    def test_positive_and_exact_guard(self):
        for value in (0, -1, Fraction(-1, 3)):
            with self.subTest(value=value), self.assertRaises(ValueError):
                Magnitude(value, "line")
        for value in (True, 1.0, "1"):
            with self.subTest(value=value), self.assertRaises(TypeError):
                Magnitude(value, "line")

    def test_rational_constructive_grid(self):
        signs = Counter()
        for a, b, c, n in itertools.product(range(1, 9), repeat=4):
            left = Fraction(a, 3), Fraction(b, 5), Fraction(c, 3)
            k = Fraction(n, 7)
            # D:E = B:C and E:F = A:B.
            x, y, z = left
            right = k * x * y, k * x * z, k * y * z
            t = self.checked(left, right)
            expected = 1 if a > c else -1 if a < c else 0
            self.assertEqual(t.sign, expected)
            signs[t.sign] += 1
        self.assertEqual(signs, {-1: 1792, 0: 512, 1: 1792})

    def test_exhaustive_integer_cross_product_oracle(self):
        good, bad = 0, 0
        for a, b, c, d, e, f in itertools.product(range(1, 6), repeat=6):
            left, right = (a, b, c), (d, e, f)
            # Independent integer guard, uses no rational quotients.
            if a * f != b * e or b * e != c * d:
                with self.assertRaises(ValueError):
                    self.checked(left, right)
                bad += 1
            else:
                t = self.checked(left, right)
                order = 1 if d > f else -1 if d < f else 0
                self.assertEqual(t.sign, order)
                good += 1
        self.assertEqual((good, bad), (103, 15_522))


if __name__ == "__main__":
    unittest.main()
