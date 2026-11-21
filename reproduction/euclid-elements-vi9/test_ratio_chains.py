"""Exact independent checks for the original one-third and teaching extensions."""
import unittest
from fractions import Fraction as Q

from ratio_chains import certificate, construct


def sweep():
    count = positive = negative = 0
    for ax, ay in [(0, 0), (Q(1, 3), Q(-2, 7))]:
        for dx, dy in [(12, 0), (4, 5), (-3, 7)]:
            for wx, wy in [(1, 3), (-1, -3), (1, 2), (-1, -2), (3, 1), (-3, -1)]:
                a, b = (ax, ay), (ax + dx, ay + dy)
                side = dx*wy - dy*wx
                for n in range(2, 9):
                    for m in range(1, n):
                        got = construct(a, b, (wx, wy), n, m)
                        expected = (ax + Q(m, n)*dx, ay + Q(m, n)*dy)
                        step_differences = [(q[0]-p[0], q[1]-p[1])
                                            for p, q in zip(got.marks, got.marks[1:])]
                        cert = certificate(a, b, got.marks[-1], got.marks[m],
                                           got.cut_point)
                        r = Q(n-m, m)
                        if (got.cut_point != expected or got.segment_parameter != Q(m, n)
                                or step_differences != [(wx, wy)] * n or cert != (0, r, r)):
                            raise ArithmeticError("exact construction check failed")
                        count += 1
                        positive += side > 0
                        negative += side < 0
    return count, positive, negative


class TestVI9(unittest.TestCase):
    def test_original_third(self):
        got = construct((0, 0), (12, 0), (1, 3))
        self.assertEqual(got.marks, ((0, 0), (1, 3), (2, 6), (3, 9)))
        self.assertEqual((got.cut_point, got.segment_parameter), ((4, 0), Q(1, 3)))
        self.assertEqual(certificate((0, 0), (12, 0), (3, 9), (1, 3), (4, 0)),
                         (0, 2, 2))

    def test_off_parallel(self):
        self.assertEqual(certificate((0, 0), (12, 0), (3, 9), (1, 3), (5, 0)),
                         (-9, 2, Q(7, 5)))

    def test_equal_steps_not_arbitrary(self):
        self.assertEqual(certificate((0, 0), (12, 0), (4, 12), (1, 3), (3, 0)),
                         (0, 3, 3))

    def test_vertical_base(self):
        self.assertEqual(construct((2, 3), (2, -12), (-4, 0), 5, 2).cut_point, (2, -3))

    def test_degenerate_base_or_ray(self):
        for b, w in [((0, 0), (1, 2)), ((2, 4), (0, 0)), ((2, 4), (-1, -2))]:
            with self.subTest(b=b, w=w), self.assertRaises(ValueError):
                construct((0, 0), b, w)

    def test_not_proper_fraction(self):
        for n, m in [(1, 1), (3, 3), (3, 4), (3, 0), (3, -1), (3, True), (3.0, 1)]:
            with self.subTest(n=n, m=m), self.assertRaises(ValueError):
                construct((0, 0), (4, 0), (1, 3), n, m)

    def test_certificate_rejects_noninterior(self):
        for f in [(0, 0), (12, 0), (13, 0), (4, 1)]:
            with self.subTest(f=f), self.assertRaises(ValueError):
                certificate((0, 0), (12, 0), (3, 9), (1, 3), f)

    def test_sweep(self):
        result = sweep()
        print("configurations, positive side, negative side =", result, flush=True)
        self.assertEqual(result, (1008, 504, 504))
