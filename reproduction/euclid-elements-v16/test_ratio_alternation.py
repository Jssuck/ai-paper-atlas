import unittest
from collections import Counter
from fractions import Fraction
from itertools import product

from ratio_alternation import Magnitude, cmp, ratio, replay


class AlternationTests(unittest.TestCase):
    def setUp(self):
        self.quad = tuple(map(Magnitude, (2, 3, 4, 6)))

    def test_three_branches(self):
        for m, expected in ((1, -1), (2, 0), (3, 1)):
            with self.subTest(m=m):
                self.assertEqual(replay(*self.quad, m, 1)[3], (expected,) * 2)

    def test_nonproportional_input(self):
        with self.assertRaisesRegex(ValueError, "hypothesis"):
            replay(*map(Magnitude, (2, 3, 4, 5)), 2, 1)

    def test_ill_typed_cross_pairs(self):
        a, b, c, d = Magnitude(2), Magnitude(3), Magnitude(4, "area"), Magnitude(6, "area")
        self.assertEqual(ratio(a, b), ratio(c, d))
        with self.assertRaisesRegex(ValueError, "same kind"):
            replay(a, b, c, d, 2, 1)

    def test_ill_typed_within_pair(self):
        with self.assertRaisesRegex(ValueError, "ratios"):
            replay(Magnitude(2, "area"), *self.quad[1:], 2, 1)

    def test_incompatible_comparison(self):
        with self.assertRaises(ValueError):
            cmp(Magnitude(2), Magnitude(2, "area"))

    def test_bad_magnitudes(self):
        for value in (0, -1, Fraction(-3, 2)):
            with self.subTest(value=value), self.assertRaises(ValueError):
                Magnitude(value)
        for value in (1.5, True, "1"):
            with self.subTest(value=value), self.assertRaises(TypeError):
                Magnitude(value)
        with self.assertRaises(ValueError):
            Magnitude(1, "")

    def test_invalid_probes(self):
        for k in (0, -1, True, 1.5, Fraction(2)):
            for pair in ((1, k), (k, 1)):
                with self.subTest(pair=pair), self.assertRaises(ValueError):
                    replay(*self.quad, *pair)

    def test_fraction_and_regrouping(self):
        args = map(Magnitude, (Fraction(2, 3), Fraction(1, 2), 2, Fraction(3, 2)))
        orig, scaled, alt, signs = replay(*args, 6, 2)
        self.assertEqual(orig, (Fraction(4, 3),) * 2)
        self.assertEqual(scaled, orig)
        self.assertEqual(alt, (Fraction(1, 3),) * 2)
        self.assertEqual(signs, (0, 0))

    def test_finite_grid_against_oracle(self):
        counts = Counter()
        for u, v, s, t, m, n in product(range(1, 5), repeat=6):
            args = map(Magnitude, (u*s, v*s, u*t, v*t))
            orig, scaled, alt, signs = replay(*args, m, n)
            self.assertEqual(orig, (Fraction(u, v),) * 2)
            self.assertEqual(scaled, orig)
            self.assertEqual(alt, (Fraction(s, t),) * 2)
            q, threshold = Fraction(s, t), Fraction(n, m)
            expected = (q > threshold) - (q < threshold)
            self.assertEqual(signs, (expected,) * 2)
            counts[expected] += 1
        self.assertEqual(counts, {-1: 1792, 0: 512, 1: 1792})
        print(f"finite grid: {sum(counts.values())} profiles; signs -1/0/+1: {counts[-1]}/{counts[0]}/{counts[1]}")


if __name__ == "__main__":
    unittest.main()
