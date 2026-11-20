"""Independent fraction-threshold checks plus branch and validation tests."""
from fractions import Fraction
from itertools import product
import unittest

from ratio_witness import compare, exact_witness, find_witness, is_witness, transport


class WitnessTests(unittest.TestCase):
    def test_lower_equality(self):
        self.assertEqual(transport((3, 2), (6, 4), (2, 2), (1, 1)), (1, 1, 0))

    def test_lower_strict(self):
        self.assertEqual(transport((3, 2), (6, 4), (2, 2), (4, 5)), (1, 1, -1))

    def test_upper_equality_not_witness(self):
        self.assertFalse(is_witness((6, 4), (2, 2), (2, 3)))

    def test_direction(self):
        self.assertFalse(is_witness((2, 2), (6, 4), (1, 1)))
        self.assertIsNone(exact_witness((2, 2), (6, 4)))
        self.assertIsNone(exact_witness((2, 2), (6, 6)))

    def test_bad_equal_premise(self):
        with self.assertRaises(ValueError):
            transport((1, 2), (6, 4), (2, 2), (1, 1))

    def test_bad_witness_premise(self):
        with self.assertRaises(ValueError):
            transport((3, 2), (6, 4), (2, 2), (2, 3))

    def test_finite_window_is_not_verdict(self):
        hi, lo = (102, 100), (101, 100)
        self.assertIsNone(find_witness(hi, lo, 20))
        self.assertEqual(find_witness(hi, lo, 60), (51, 52))
        self.assertEqual(exact_witness(hi, lo), (100, 101))
        self.assertTrue(is_witness(hi, lo, (100, 101)))

    def test_invalid_inputs(self):
        for bad in [0, -1, 1.0, True]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    compare((bad, 2), (1, 2))
                with self.assertRaises(ValueError):
                    compare((1, 2), (bad, 2))
                with self.assertRaises(ValueError):
                    find_witness((2, 1), (1, 1), bad)

    def test_exact_fractions(self):
        self.assertEqual(
            transport((Fraction(3, 5), Fraction(2, 5)), (6, 4), (2, 2), (4, 5)),
            (1, 1, -1),
        )

    def test_grid(self):
        pairs = list(product(range(1, 5), repeat=2))
        probes = list(product(range(1, 5), repeat=2))
        transported = 0
        for first, mid, low in product(pairs, repeat=3):
            a, b, c = (Fraction(*p) for p in (first, mid, low))
            if a != b:
                continue
            for p in probes:
                t = Fraction(p[1], p[0])
                expected = c <= t < b
                self.assertEqual(is_witness(mid, low, p), expected)
                if expected:
                    self.assertEqual(transport(first, mid, low, p), (1, 1, (-1 if c < t else 0)))
                    transported += 1
        self.assertEqual(transported, count_expected(pairs, probes))
        self.assertGreater(transported, 0)


def count_expected(pairs, probes):
    return sum(Fraction(*a) == Fraction(*b)
               and Fraction(*c) <= Fraction(n, m) < Fraction(*b)
               for a, b, c in product(pairs, repeat=3) for m, n in probes)
