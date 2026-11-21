import itertools
import unittest
from collections import Counter
from fractions import Fraction

from ratio_chains import Magnitude, Trace, chain, verify_v20


class ChainTests(unittest.TestCase):
    def test_more(self):
        self.assertEqual(
            verify_v20(chain((6, 4, 3), "line"), chain((12, 8, 6), "area")),
            Trace(Fraction(3, 2), Fraction(3, 4),
                  Fraction(3, 2), Fraction(3, 4), 1),
        )

    def test_equal(self):
        trace = verify_v20(chain((6, 4, 6), "line"), chain((12, 8, 12), "area"))
        self.assertEqual(trace.sign, 0)

    def test_less(self):
        trace = verify_v20(chain((3, 4, 6), "line"), chain((6, 8, 12), "area"))
        self.assertEqual(trace.sign, -1)

    def test_first_edge_needed(self):
        with self.assertRaisesRegex(ValueError, "^first adjacent"):
            verify_v20(chain((6, 4, 3), "line"), chain((12, 20, 15), "area"))

    def test_second_edge_needed(self):
        with self.assertRaisesRegex(ValueError, "^second adjacent"):
            verify_v20(chain((6, 4, 3), "line"), chain((12, 8, 15), "area"))

    def test_kind_guard(self):
        broken = (Magnitude(6, "line"), Magnitude(4, "area"), Magnitude(3, "line"))
        with self.assertRaisesRegex(ValueError, "^a ratio"):
            verify_v20(broken, chain((12, 8, 6), "area"))

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
            left = (Fraction(a, 3), Fraction(b, 5), Fraction(c, 3))
            right = tuple(v * Fraction(n, 7) for v in left)
            t = verify_v20(chain(left, "line"), chain(right, "area"))
            expected = 1 if a > c else -1 if a < c else 0
            self.assertEqual(t.sign, expected)
            signs[t.sign] += 1
        self.assertEqual(signs, {-1: 1792, 0: 512, 1: 1792})

    def test_exhaustive_integer_cross_product_oracle(self):
        good, bad = 0, 0
        for a, b, c, d, e, f in itertools.product(range(1, 6), repeat=6):
            left, right = chain((a, b, c), "line"), chain((d, e, f), "area")
            # An independent guard oracle: integer multiplication, no ratio().
            if a * e != b * d or b * f != c * e:
                with self.assertRaises(ValueError):
                    verify_v20(left, right)
                bad += 1
            else:
                t = verify_v20(left, right)
                order = 1 if d > f else -1 if d < f else 0
                self.assertEqual(t.sign, order)
                good += 1
        # Primitive triples by maximum m=1..5 admit floor(5/m)**2 pairs.
        expected_good = 25 + 24 + 18 + 30 + 60
        self.assertEqual((good, bad), (expected_good, 5**6 - expected_good))


if __name__ == "__main__":
    unittest.main()
