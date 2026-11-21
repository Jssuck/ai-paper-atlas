from fractions import Fraction as Q
from itertools import product
from unittest import TestCase

from ratio_chains import compare, polygon_area, rational_middle


def diagonal_area(vertices):
    a, b, c, d = vertices
    def triangle(p, q, r):
        return abs((q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])) / 2
    return triangle(a, b, c) + triangle(a, c, d)


class VI17Tests(TestCase):
    def test_equal(self):
        result = compare(9, 12, 16)
        self.assertEqual(result.ratios, (Q(3, 4), Q(3, 4)))
        self.assertEqual(result.areas, (144, 144))
        self.assertTrue(result.proportional)
        self.assertTrue(result.equal_area)

    def test_unequal(self):
        result = compare(9, 13, 16)
        self.assertEqual(result.areas, (144, 169))
        self.assertFalse(result.proportional)
        self.assertFalse(result.equal_area)

    def test_extremes_swap_not_middle_swap(self):
        self.assertEqual(compare(16, 12, 9).ratios, (Q(4, 3), Q(4, 3)))
        self.assertTrue(compare(16, 12, 9).equal_area)
        self.assertFalse(compare(12, 9, 16).proportional)

    def test_arithmetic_mean_is_not_geometric_mean(self):
        b = Q(9 + 16, 2)
        self.assertEqual(compare(9, b, 16).areas, (144, Q(625, 4)))
        self.assertFalse(compare(9, b, 16).equal_area)

    def test_rational_roots(self):
        for a, c, b in ((9, 16, Q(12)), (Q(2, 3), Q(3, 8), Q(1, 2)),
                        (Q(2, 9), Q(8, 25), Q(4, 15))):
            self.assertEqual(rational_middle(a, c), b)
            self.assertTrue(compare(a, b, c).equal_area)
        for a, c in ((1, 2), (1, Q(1, 2)), (1, Q(4, 3))):
            self.assertIsNone(rational_middle(a, c))

    def test_exact_grid(self):
        values = (Q(1, 3), Q(1, 2), Q(2, 3), Q(3, 4), Q(1), Q(3, 2), Q(2), Q(3))
        truth = set()
        for a, b, c in product(values, repeat=3):
            result = compare(a, b, c)
            self.assertEqual(result.areas, tuple(map(diagonal_area,
                                                      (result.extremes, result.middle_square))))
            self.assertEqual(result.areas, (a*c, b*b))
            self.assertEqual(result.ratios, (a/b, b/c))
            self.assertEqual(result.proportional, result.equal_area)
            truth.add(result.equal_area)
        self.assertEqual(truth, {False, True})

    def test_translation_and_orientation(self):
        for polygon in (compare(3, 2, 4).extremes, compare(3, 2, 4).middle_square):
            transformed = tuple((x + Q(2, 3), y - Q(1, 7)) for x, y in reversed(polygon))
            self.assertEqual(polygon_area(polygon), polygon_area(transformed))

    def test_nonpositive_rejected_each_position(self):
        for index, invalid in product(range(3), (0, -1, Q(-1, 3))):
            args = [1, 1, 1]
            args[index] = invalid
            with self.assertRaises(ValueError):
                compare(*args)
        for pair in ((0, 1), (1, 0), (-1, 1), (1, -1)):
            with self.assertRaises(ValueError):
                rational_middle(*pair)

    def test_nonexact_rejected(self):
        for value in (0.5, True, "1"):
            with self.assertRaises(TypeError):
                compare(1, value, 1)
            with self.assertRaises(TypeError):
                rational_middle(value, 1)
