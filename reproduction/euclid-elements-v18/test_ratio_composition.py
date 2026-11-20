from fractions import Fraction as F
from itertools import product
from unittest import TestCase

from ratio_composition import Magnitude, candidate_trace, direct_probe, replay


def mags(a, b, c, d):
    return Magnitude(a), Magnitude(b), Magnitude(c, "area"), Magnitude(d, "area")


class CompositionTests(TestCase):
    def test_exact_fourth_candidate_with_different_kinds(self):
        trace = replay(*mags(F(2, 3), F(5, 7), F(4, 3), F(10, 7)))
        self.assertEqual(trace.candidate, Magnitude(F(10, 7), "area"))
        self.assertEqual(trace.remainder, Magnitude(F(4, 3), "area"))
        self.assertEqual((trace.denominator_sign, trace.remainder_sign), (0, 0))

    def test_both_strict_branches_are_failed_premises(self):
        a = mags(2, 3, 3, 7)
        b = mags(2, 3, 5, 5)
        for case, signs in ((a, (-1, 1)), (b, (1, -1))):
            t = candidate_trace(*case)
            self.assertEqual(t.candidate.value, 6)
            self.assertEqual(t.remainder.value, 4)
            self.assertEqual((t.denominator_sign, t.remainder_sign), signs)
            self.assertFalse(t.separated_hypothesis)
            with self.assertRaises(ValueError):
                replay(*case)
            with self.assertRaises(ValueError):
                direct_probe(*case, 1, 1)

    def test_probe_at_and_below_boundary(self):
        for m, k in ((3, 1), (3, 3)):
            t = direct_probe(*mags(2, 3, 4, 6), m, k)
            self.assertEqual(t.joint_signs, (1, 1))
            self.assertIsNone(t.separated_signs)

    def test_shifted_probe_covers_all_signs(self):
        for k, sign in ((4, 1), (5, 0), (6, -1)):
            t = direct_probe(*mags(2, 3, 4, 6), 3, k)
            self.assertEqual(t.joint_signs, (sign, sign))
            self.assertEqual(t.separated_signs, (sign, sign))

    def test_kind_must_match_within_pair(self):
        bad = (Magnitude(2), Magnitude(3, "area"), Magnitude(4), Magnitude(6))
        with self.assertRaises(ValueError):
            candidate_trace(*bad)
        with self.assertRaises(ValueError):
            direct_probe(*bad, 1, 1)

    def test_nonpositive_magnitudes_rejected(self):
        for value in (0, -1):
            with self.assertRaises(ValueError):
                Magnitude(value)

    def test_floats_and_booleans_rejected(self):
        for value in (True, 2.0):
            with self.assertRaises(TypeError):
                Magnitude(value)

    def test_illegal_probe_rejected(self):
        for m, k in ((0, 2), (2, -1), (True, 2), (2, 1.0)):
            with self.assertRaises(ValueError):
                direct_probe(*mags(2, 3, 4, 6), m, k)

    def test_grid_against_independent_integer_formula(self):
        seen = {-1: 0, 0: 0, 1: 0}
        shifts = {False: 0, True: 0}
        for u, v, s, t, m, k in product(range(1, 5), repeat=6):
            args = mags(u*s, v*s, u*t, v*t)
            r = direct_probe(*args, m, k)
            x = m*(u+v) - k*v
            signed = (x > 0) - (x < 0)
            self.assertEqual(r.joint_signs, (signed, signed))
            seen[signed] += 1
            shifts[r.separated_signs is not None] += 1
        self.assertEqual(sum(seen.values()), 4096)
        self.assertEqual(shifts, {False: 2560, True: 1536})
