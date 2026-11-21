"""Finite exact checks for the VI.2 Cartesian teaching reconstruction."""
import unittest
from fractions import Fraction as Q

from ratio_chains import A, B, C, D, E, CASES, examine, lerp


class VI2Tests(unittest.TestCase):
    def test_parallel(self):
        x = examine(*CASES["parallel"])
        self.assertEqual(x.segment_ratios, (2, 2))
        self.assertEqual(x.double_areas, (1, 2, 2))
        self.assertEqual(x.parallel_det, 0)
        self.assertTrue(x.same_side and x.forward and x.converse)

    def test_nonparallel_and_inverting_one_ratio(self):
        x = examine(*CASES["nonparallel"])
        self.assertEqual(x.segment_ratios, (2, Q(1, 2)))
        self.assertEqual(x.double_areas, (2, 4, 1))
        self.assertEqual(x.parallel_det, 3)
        self.assertEqual(x.segment_ratios[0], 1 / x.segment_ratios[1])
        self.assertNotEqual(*x.segment_ratios)

    def test_outside_unsigned_converse_fails(self):
        with self.assertRaises(ValueError):
            examine(*CASES["outside"])
        x = examine(*CASES["outside"], interior=False)
        self.assertEqual(x.segment_ratios, (Q(1, 2), Q(1, 2)))
        self.assertEqual(x.double_areas, (12, 6, 6))
        self.assertEqual(x.side_values, (-6, 6))
        self.assertEqual(x.parallel_det, 12)
        self.assertFalse(x.same_side or x.converse)

    def test_domain(self):
        for args in ((A, B, B, D, D), (A, B, C, (1, 1), E),
                     (A, B, C, A, E), (A, B, C, B, E)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                examine(*args)
        with self.assertRaises(TypeError):
            examine(A, B, C, (1.0, 0), E)

    def test_fractional_coordinates(self):
        a, b, c = ((Q(1, 7), Q(-2, 9)), (Q(8, 3), 1), (0, Q(4, 5)))
        t = Q(3, 7)
        x = examine(a, b, c, lerp(a, b, t), lerp(a, c, t))
        self.assertEqual(x.area_ratios, (Q(4, 3), Q(4, 3)))
        self.assertEqual(x.parallel_det, 0)

    def test_grid(self):
        frames = [
            ((0, 0), (3, 0), (0, 3)),
            ((0, 0), (0, 3), (3, 0)),
            ((2, 4), (-3, 2), (3, -1)),
            ((-2, 0), (-3, 4), (5, -1)),
            ((-1, -3), (0, -1), (1, 2)),
            ((2, 2), (2, -5), (-3, 2)),
        ]
        sample = [Q(n, 10) for n in range(1, 10)]
        count = positive = negative = 0
        for a, b, c in frames:
            # Independent signed doubled area of ABC via expanded shoelace.
            area = (a[0]*b[1] + b[0]*c[1] + c[0]*a[1]
                    - a[1]*b[0] - b[1]*c[0] - c[1]*a[0])
            for t in sample:
                for s in sample:
                    x = examine(a, b, c, lerp(a, b, t), lerp(a, c, s))
                    self.assertEqual(x.parameters, (t, s))
                    self.assertEqual(x.parallel_det, (s - t) * area)
                    self.assertEqual(x.double_areas, tuple(
                        abs(area) * k for k in (t*s, (1-t)*s, (1-s)*t)))
                    self.assertEqual(x.segment_ratios, x.area_ratios)
                    self.assertEqual(x.segment_ratios[0] == x.segment_ratios[1], t == s)
                    self.assertTrue(x.same_side and x.forward and x.converse)
                    count += 1
                    positive += int(x.parallel_det == 0)
                    negative += int(x.parallel_det != 0)
        self.assertEqual((count, positive, negative), (486, 54, 432))
        print("grid: 486 interior probes (54 parallel, 432 nonparallel)")


if __name__ == "__main__":
    unittest.main()
