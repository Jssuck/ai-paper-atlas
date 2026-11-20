from fractions import Fraction
from itertools import product
import unittest

from ratio_order import (
    Magnitude, bounded_difference, local_probe, mags, order_transport,
    proportion, strict_trace,
)


class OrderTests(unittest.TestCase):
    def test_greater(self):
        self.assertEqual(order_transport(*mags(9, 6, 6, 4)),
                         ((1, 1), ((1, 1), (1, 0, 1), (4, 6, 6))))

    def test_less(self):
        self.assertEqual(order_transport(*mags(6, 4, 9, 6)),
                         ((-1, -1), ((1, 1), (1, 0, 1), (4, 6, 6))))

    def test_equal(self):
        self.assertEqual(order_transport(*mags(6, 4, 6, 4)), ((0, 0), None))

    def test_fraction(self):
        a, b, c, d = mags(Fraction(7, 2), Fraction(5, 2),
                          Fraction(7, 4), Fraction(5, 4))
        self.assertEqual(strict_trace(a, b, c, d),
                         ((10, 7), (1, 0, 1),
                          (Fraction(35, 4), Fraction(35, 2), Fraction(35, 2))))

    def test_not_proportion(self):
        with self.assertRaisesRegex(ValueError, "exact proportion"):
            order_transport(*mags(51, 50, 52, 50))

    def test_bounded_not_decision(self):
        near = mags(51, 50, 52, 50)
        self.assertIsNone(bounded_difference(*near, 20))
        self.assertEqual(bounded_difference(*near, 26), ((25, 26), (-1, 0)))

    def test_types(self):
        x = (*mags(9, 6), Magnitude(6, "area"), Magnitude(4, "area"))
        self.assertTrue(proportion(*x))
        with self.assertRaisesRegex(ValueError, "common kind"):
            order_transport(*x)

    def test_no_bad_numbers(self):
        for x in (True, 1.0, 0, -1, "2"):
            with self.subTest(x=x), self.assertRaises(ValueError):
                Magnitude(x)

    def test_wrong_probe_and_orientation(self):
        for m, n in ((False, 1), (1, 0), (1, -1), (Fraction(1), 1)):
            with self.subTest(m=m, n=n), self.assertRaises(ValueError):
                local_probe(*mags(3, 2), m, n)
        with self.assertRaises(ValueError):
            strict_trace(*mags(6, 4, 9, 6))

    def test_exhaustive_grid(self):
        eligible = 0
        for a, b, c, d in product(range(1, 9), repeat=4):
            # Independent quotient oracle and raw comparison of both columns.
            if Fraction(a, b) != Fraction(c, d):
                continue
            eligible += 1
            expected = ((a > c) - (a < c), (b > d) - (b < d))
            observed, trace = order_transport(*mags(a, b, c, d))
            self.assertEqual(observed, expected)
            if expected[0]:
                (m, n), signs, values = trace
                self.assertGreater(min(m, n), 0)
                self.assertEqual(signs, (1, 0, 1))
                self.assertLess(values[0], values[1])
                self.assertLessEqual(values[1], values[2])
            else:
                self.assertIsNone(trace)
        self.assertEqual(eligible, 160)
