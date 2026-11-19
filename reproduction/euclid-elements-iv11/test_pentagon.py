from fractions import Fraction as F
from itertools import permutations
import unittest

from pentagon import (COS36, U, V, angle_key, check_grid, construct, dot,
                      polygon_checks, q, rotate, source_checks, star, sub)


class PentagonTests(unittest.TestCase):
    def test_exact_grid(self):
        self.assertEqual(check_grid(), (96, 96))

    def test_rotation_polynomial_and_closure(self):
        self.assertGreater(U.sign(), 0)
        self.assertGreater(V.sign(), 0)
        self.assertEqual(4 * U * U + 2 * U, q(1))
        self.assertEqual(2 * COS36 * COS36 - 1, U)
        points = construct()
        self.assertEqual(rotate(points[-1], 1), points[0])
        self.assertEqual(len(set(points)), 5)

    def test_source_triangle_and_bisectors(self):
        expected = {"apex_36", "both_bases_72", "interior_bisectors_CE_DB",
                    "five_equal_inscribed_angles"}
        for branch in (-1, 1):
            checks = source_checks(construct(F(3, 7), branch))
            self.assertEqual(set(checks), expected)
            self.assertTrue(all(checks.values()))

    def test_star_fools_ordinary_angle_and_chord_checks(self):
        points = star(construct())
        checks = polygon_checks(points)
        self.assertTrue(checks["same_circle"])
        self.assertTrue(checks["equal_chords"])
        self.assertTrue(checks["equal_ordinary_angles"])
        self.assertFalse(checks["ordinary_angles_108"])
        self.assertFalse(checks["regular_convex_boundary"])
        self.assertEqual(checks["winding"], 2)
        self.assertEqual(checks["strict_crossings"], 5)
        self.assertEqual(angle_key(*points[:3]), (1, COS36 * COS36))

    def test_all_orders_of_one_vertex_set(self):
        counts = [0, 0, 0]  # boundary orders, uniform star orders, other
        for order in permutations(construct()):
            result = polygon_checks(order)
            if result["regular_convex_boundary"]:
                counts[0] += 1
            elif result["equal_chords"] and result["equal_ordinary_angles"]:
                self.assertEqual(abs(result["winding"]), 2)
                self.assertEqual(result["strict_crossings"], 5)
                counts[1] += 1
            else:
                counts[2] += 1
        self.assertEqual(counts, [10, 10, 100])

    def test_reflection_and_scale(self):
        base = construct()
        r = F(17, 4)
        reflected = construct(r, -1)
        for (x, y), (xx, yy) in zip(base, reflected):
            self.assertEqual((x * r, -y * r), (xx, yy))
        edge = sub(reflected[0], reflected[1])
        self.assertEqual(dot(edge, edge), 2 * r * r * (1 - U))
        self.assertEqual(polygon_checks(reflected)["winding"], -1)

    def test_rejected_inputs(self):
        for radius in (0, -1, F(-1, 3), True, 1.0):
            with self.subTest(radius=radius), self.assertRaises(ValueError):
                construct(radius)
        for branch in (0, 2, True, -1.0):
            with self.subTest(branch=branch), self.assertRaises(ValueError):
                construct(branch=branch)

    def test_rejected_point_lists(self):
        p = construct()
        for malformed in (p[:4], p[:4] + (p[0],),
                          p[:4] + ((q(2), q(0)),),
                          p[:4] + ((q(-1), q(0)),)):
            with self.subTest(malformed=malformed), self.assertRaises(ValueError):
                polygon_checks(malformed)


if __name__ == "__main__":
    unittest.main()
