"""Independently compare replayed outputs with known generating ratios."""
from fractions import Fraction as F
from itertools import product
import unittest

from ratio_remainders import Magnitude as Q, main_trace, porism_trace


class RemainderTests(unittest.TestCase):
    def test_main_exact(self):
        a, b, u, v = map(Q, (10, 15, 4, 6))
        self.assertEqual(main_trace(a, b, u, v),
                         (("V.16", F(5, 2), F(5, 2)),
                          ("V.17", F(3, 2), F(3, 2)),
                          ("V.16", F(2, 3), F(2, 3)),
                          ("V.11", F(2, 3), F(2, 3))))

    def test_porism_mixed(self):
        a, u = map(Q, (10, 4))
        b, v = (Q(n, "area") for n in (15, 6))
        self.assertEqual(porism_trace(a, u, b, v),
                         (("V.17", F(3, 2), F(3, 2)),
                          ("inverse", F(2, 3), F(2, 3)),
                          ("V.18", F(5, 3), F(5, 3))))

    def test_grid_independent_expected(self):
        count = 0
        for r, u, p, q in product(range(1, 9), repeat=4):
            a, b, c, d = map(Q, ((r+u)*p, (r+u)*q, u*p, u*q))
            self.assertEqual(main_trace(a, b, c, d)[-1][1:], (F(p, q),)*2)
            b, d = (Q(x.value, "area") for x in (b, d))
            self.assertEqual(porism_trace(a, c, b, d)[-1][1:],
                             (F(r+u, r),)*2)
            count += 1
        self.assertEqual(count, 4096)

    def test_fraction_noninteger_case(self):
        a, b, u, v = map(Q, (F(5, 6), F(5, 9), F(1, 3), F(2, 9)))
        self.assertEqual(main_trace(a, b, u, v)[-1][1], F(3, 2))

    def test_main_rejects_mixed(self):
        with self.assertRaisesRegex(ValueError, "kinds differ"):
            main_trace(Q(10), Q(15, "area"), Q(4), Q(6, "area"))

    def test_unmatched_premises(self):
        a, b, u, v = map(Q, (10, 15, 4, 5))
        with self.assertRaisesRegex(ValueError, "whole ratio"):
            main_trace(a, b, u, v)
        with self.assertRaisesRegex(ValueError, "joint ratios"):
            porism_trace(a, u, b, v)

    def test_zero_and_negative_remainders(self):
        for n in (10, 11):
            with self.subTest(removed=n):
                with self.assertRaisesRegex(ValueError, "strictly smaller"):
                    main_trace(Q(10), Q(15), Q(n), Q(6))

    def test_invalid_kind_inside_porism_pair(self):
        with self.assertRaisesRegex(ValueError, "kinds differ"):
            porism_trace(Q(10), Q(4, "area"), Q(15), Q(6))

    def test_invalid_numbers(self):
        for n in (2.5, True):
            with self.assertRaises(TypeError):
                Q(n)
        for n in (0, -1):
            with self.assertRaises(ValueError):
                Q(n)
