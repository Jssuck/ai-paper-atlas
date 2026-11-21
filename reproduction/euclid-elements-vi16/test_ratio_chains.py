from fractions import Fraction as Q
from itertools import product
import unittest

from ratio_chains import compare, polygon_area


def area_from_triangles(rect):
    """Independent oracle: split at diagonal from the first to third vertex."""
    a, b, c, d = rect

    def area(p, q, r):
        x, y = q[0] - p[0], q[1] - p[1]
        u, v = r[0] - p[0], r[1] - p[1]
        return abs(x * v - y * u) / 2

    return area(a, b, c) + area(a, c, d)


class VI16Tests(unittest.TestCase):
    def test_true_nonidentical_rectangles(self):
        report = compare(6, 4, 9, 6)
        self.assertEqual(report.ratios, (Q(3, 2), Q(3, 2)))
        self.assertEqual(report.areas, (36, 36))
        self.assertNotEqual(report.extremes, report.means)
        self.assertTrue(report.proportional and report.equal_area)

    def test_false(self):
        report = compare(6, 4, 8, 6)
        self.assertEqual(report.ratios, (Q(3, 2), Q(4, 3)))
        self.assertEqual(report.areas, (36, 32))
        self.assertFalse(report.proportional or report.equal_area)

    def test_wrong_pairing_false_negative(self):
        a, b, c, d = 6, 4, 9, 6
        self.assertTrue(compare(a, b, c, d).proportional)
        self.assertEqual((a * c, b * d), (54, 24))

    def test_wrong_pairing_false_positive(self):
        a, b, c, d = 2, 3, 3, 2
        self.assertEqual(a * c, b * d)
        self.assertFalse(compare(a, b, c, d).equal_area)

    def test_roles(self):
        original = compare(6, 4, 9, 6)
        for swapped in (compare(9, 6, 6, 4), compare(4, 6, 6, 9)):
            self.assertTrue(swapped.proportional and swapped.equal_area)
        # Flipping only one ratio does not generally preserve equality.
        self.assertFalse(compare(4, 6, 9, 6).proportional)

    def test_zero_and_negative_each_position(self):
        for index, v in product(range(4), (0, -1)):
            data = [2, 3, 4, 6]
            data[index] = v
            with self.assertRaises(ValueError):
                compare(*data)

    def test_forbid_inexact_or_non_numeric_length(self):
        for v in (1.0, "1", True):
            with self.assertRaises(TypeError):
                compare(v, 2, 3, 4)

    def test_vertex_orientation_and_translation(self):
        v = compare(Q(3, 4), 4, 9, Q(2, 7)).extremes
        translated = tuple((x + 100, y - Q(5, 3)) for x, y in v)
        self.assertEqual(polygon_area(translated[::-1]), Q(3, 14))

    def test_exact_grid(self):
        grid = (Q(1, 5), Q(2, 3), Q(1), Q(7, 5), Q(2), Q(5))
        both = either = 0
        for a, b, c, d in product(grid, repeat=4):
            report = compare(a, b, c, d)
            areas = tuple(area_from_triangles(r) for r in (report.extremes, report.means))
            self.assertEqual(report.areas, (a * d, b * c))
            self.assertEqual(report.areas, areas)
            self.assertEqual(report.proportional, report.equal_area)
            self.assertEqual(report.equal_area, areas[0] == areas[1])
            both += report.equal_area
            either += 1
        self.assertEqual(either, 1296)
        self.assertGreater(both, 0)
        self.assertLess(both, either)


if __name__ == "__main__":
    unittest.main()
