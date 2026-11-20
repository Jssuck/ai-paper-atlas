from fractions import Fraction
from itertools import product
import unittest

from ratio_separation import Magnitude, cmp, replay


class V17Tests(unittest.TestCase):
    def test_three_signs_and_exact_compared_pairs(self):
        args = tuple(map(Magnitude, (2, 3, 4, 6)))
        for p, q, sign, wholes, remainders in (
            (1, 1, -1, ((5, 6), (10, 12)), ((2, 3), (4, 6))),
            (3, 2, 0, ((15, 15), (30, 30)), ((6, 6), (12, 12))),
            (2, 1, 1, ((10, 9), (20, 18)), ((4, 3), (8, 6))),
        ):
            with self.subTest(p=p, q=q):
                r = replay(*args, p, q)
                self.assertEqual(r.whole_signs, (sign, sign))
                self.assertEqual(r.remainder_signs, (sign, sign))
                vals = lambda pairs: tuple((a.value, b.value) for a, b in pairs)
                self.assertEqual(vals(r.whole_pairs), wholes)
                self.assertEqual(vals(r.remainder_pairs), remainders)
                self.assertEqual(tuple(x.value for x in r.canceled), (3*p, 6*p))

    def test_mixed_kinds_allowed_across_pairs(self):
        args = (Magnitude(2), Magnitude(3), Magnitude(4, "area"),
                Magnitude(6, "area"))
        r = replay(*args, 3, 2)
        self.assertEqual(r.whole_ratios, (Fraction(5, 3),) * 2)
        self.assertEqual(r.remainder_ratios, (Fraction(2, 3),) * 2)
        with self.assertRaisesRegex(ValueError, "matching kinds"):
            cmp(r.canceled[0], r.canceled[1])

    def test_mismatch_within_pair(self):
        with self.assertRaisesRegex(ValueError, "matching kinds"):
            replay(Magnitude(2), Magnitude(3, "area"),
                   Magnitude(4), Magnitude(6), 1, 1)

    def test_invalid_hypothesis(self):
        with self.assertRaisesRegex(ValueError, "hypothesis"):
            replay(*map(Magnitude, (2, 3, 5, 6)), 3, 2)

    def test_invalid_probes(self):
        args = tuple(map(Magnitude, (2, 3, 4, 6)))
        for k in (0, -1, True, 1.0, Fraction(1)):
            for p, q in ((k, 1), (1, k)):
                with self.subTest(p=p, q=q), self.assertRaises(ValueError):
                    replay(*args, p, q)

    def test_invalid_magnitude(self):
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                Magnitude(bad)
        for bad in (True, 1.0, "1"):
            with self.assertRaises(TypeError):
                Magnitude(bad)
        with self.assertRaises(ValueError):
            Magnitude(1, " ")

    def test_fraction_inputs(self):
        args = tuple(map(Magnitude, (Fraction(2, 7), Fraction(3, 7),
                                     Fraction(5, 9), Fraction(5, 6))))
        self.assertEqual(replay(*args, 3, 2).remainder_ratios, (Fraction(2, 3),)*2)

    def test_unmatched_cancellation_can_change_sign(self):
        r = replay(*map(Magnitude, (2, 3, 4, 6)), 3, 2)
        a, b = r.whole_pairs[1]
        self.assertEqual(cmp(a, b), 0)
        # Cancel 9 on one side and 18 on the other instead of 18 on both.
        self.assertEqual(cmp(Magnitude(a.value - 9), Magnitude(b.value - 18)), 1)

    def test_finite_grid_against_independent_threshold(self):
        counts = {-1: 0, 0: 0, 1: 0}
        for u, v, s, t, p, q in product(range(1, 5), repeat=6):
            a = tuple(map(Magnitude, (u*s, v*s, u*t, v*t)))
            r = replay(*a, p, q)
            sign = (u*p > v*q) - (u*p < v*q)
            self.assertEqual(r.whole_signs, (sign, sign))
            self.assertEqual(r.remainder_signs, (sign, sign))
            self.assertEqual(r.remainder_ratios, (Fraction(u, v),)*2)
            counts[sign] += 1
        self.assertEqual(counts, {-1: 1792, 0: 512, 1: 1792})


if __name__ == "__main__":
    unittest.main()
