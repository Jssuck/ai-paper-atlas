import unittest
from fractions import Fraction as Q

from triangle_areas import (area, grid, norm2, side_squares, signed_double_area,
                            sub, third_point, worked)


class AreaRatioTests(unittest.TestCase):
    def test_worked_construction(self):
        abc, deff, g = worked()
        a, b, c = abc
        self.assertEqual(g, (9, 0))
        self.assertEqual((area(*abc), area(*deff), area(a, b, g)), (6, Q(27, 2), Q(27, 2)))
        self.assertEqual(area(*abc)/area(*deff), Q(4, 9))

    def test_independent_side_and_area_paths(self):
        cases = 0
        sizes = [0, 0, 0]
        reflected_count = 0
        for abc, deff, k, reflected in grid():
            a, b, c = abc
            d, e, f = deff
            g = third_point(b, c, k)
            self.assertGreater(area(*abc), 0)
            self.assertGreater(area(*deff), 0)
            sides1, sides2 = side_squares(*abc), side_squares(*deff)
            self.assertEqual(sides2, tuple(k*k*x for x in sides1))
            self.assertEqual(area(*deff)/area(*abc), Q(sides2[1], sides1[1]))
            self.assertEqual(area(a, b, g), area(*deff))
            self.assertEqual(signed_double_area(*deff),
                             (-1 if reflected else 1)*k*k*signed_double_area(*abc))
            # Squared versions of BC:EF=EF:BG and AB:DE=EF:BG.
            bg2 = norm2(sub(g, b))
            self.assertEqual(sides1[1]*bg2, sides2[1]**2)
            self.assertEqual(sides1[0]*bg2, sides2[0]*sides2[1])
            sizes[0 if k < 1 else 1 if k == 1 else 2] += 1
            reflected_count += reflected
            cases += 1
        self.assertEqual((cases, sizes, reflected_count), (320, [128, 64, 128], 160))

    def test_short_equal_long_third_point(self):
        b, c = (0, 0), (4, 0)
        self.assertEqual([third_point(b, c, k) for k in (Q(1, 2), 1, Q(3, 2))],
                         [(1, 0), c, (9, 0)])

    def test_nonsimilar_counterexample(self):
        abc, deff, _ = worked()
        d_wrong = (2, 3)
        _, e, f = deff
        actual = area(d_wrong, e, f)/area(*abc)
        self.assertEqual(actual, Q(3, 2))
        self.assertEqual(Q(norm2(sub(f, e)), norm2(sub(abc[2], abc[1]))), Q(9, 4))
        self.assertNotEqual(actual, Q(9, 4))

    def test_squared_base_area_ratio_does_not_imply_similarity(self):
        abc, deff, _ = worked()
        _, e, f = deff
        wrong = ((0, Q(9, 2)), e, f)
        left, right = side_squares(*abc), side_squares(*wrong)
        squared_base_ratio = Q(right[1], left[1])
        self.assertEqual(area(*wrong)/area(*abc), squared_base_ratio)
        self.assertEqual(squared_base_ratio, Q(9, 4))
        self.assertEqual(Q(right[0], left[0]), Q(81, 40))
        self.assertNotEqual(Q(right[0], left[0]), squared_base_ratio)

    def test_reject_degenerate_construction_inputs(self):
        with self.assertRaises(ValueError):
            third_point((0, 0), (0, 0), 1)
        with self.assertRaises(ValueError):
            third_point((0, 0), (1, 0), 0)


if __name__ == "__main__":
    unittest.main()
