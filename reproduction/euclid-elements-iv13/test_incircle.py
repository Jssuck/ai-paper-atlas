"""Tests for the IV.13 teaching model."""
import unittest
from fractions import Fraction as F

from incircle import (
    COS36, Q5, add, boundary_sign, center_from_bisectors, check_grid, construct,
    dot, fixtures, inspect_center, norm, q, source_bisector, sub,
)


class IncircleTests(unittest.TestCase):
    def test_exact_grid(self):
        self.assertEqual(check_grid(), (96, 96, 96))

    def test_tangent_radius_square(self):
        points = construct(F(3, 2))
        f = center_from_bisectors(points)
        facts = inspect_center(points, f)
        expected = F(9,4) * Q5(F(3,8), F(1,8))
        self.assertEqual(f, (q(0), q(0)))
        self.assertEqual(facts["distance_squares"], (expected,)*5)
        self.assertTrue(facts["all_feet_midpoints"])
        self.assertEqual(COS36*COS36, Q5(F(3,8), F(1,8)))

    def test_translation_and_mirror(self):
        for branch in (-1,1):
            expect, points, _, _ = fixtures(F(13,5), branch)
            with self.subTest(branch=branch):
                self.assertEqual(boundary_sign(points), branch)
                self.assertEqual(center_from_bisectors(points), expect)

    def test_source_ray_orientation(self):
        p = construct()
        f = center_from_bisectors(p)
        for l,c,r in ((p[1],p[2],p[3]), (p[2],p[3],p[4])):
            with self.subTest(apex=c):
                x,y = sub(l,c),sub(r,c)
                u = source_bisector(l,c,r)
                self.assertEqual(norm(x), norm(y))
                self.assertEqual(dot(x,u), dot(y,u))
                self.assertGreater(dot(sub(f,c),u).sign(), 0)

    def test_wrong_center_perpendicular_is_insufficient(self):
        _, p, _, shifted = fixtures(1, 1)
        facts = inspect_center(p, shifted)
        self.assertTrue(facts["inside_every_halfplane"])
        self.assertTrue(facts["feet_strictly_inside_sides"])
        self.assertTrue(facts["perpendicular_feet"])
        self.assertFalse(facts["equal_positive_distance_squares"])

    def test_same_two_rays_are_insufficient(self):
        oracle, p, irregular, _ = fixtures(1, 1)
        self.assertEqual(center_from_bisectors(p), center_from_bisectors(irregular))
        facts = inspect_center(irregular, oracle)
        self.assertTrue(facts["inside_every_halfplane"])
        self.assertTrue(facts["feet_strictly_inside_sides"])
        self.assertTrue(facts["perpendicular_feet"])
        self.assertEqual(facts["distance_squares"][1:4], (COS36*COS36,)*3)
        self.assertNotEqual(facts["distance_squares"][0], COS36*COS36)
        self.assertFalse(facts["equal_positive_distance_squares"])

    def test_wrong_order_and_degenerate_points_rejected(self):
        p = construct()
        for invalid in ((p[0],p[2],p[4],p[1],p[3]),
                        (p[0],p[0],p[2],p[3],p[4]), p[:4]):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    center_from_bisectors(invalid)

    def test_outside_foot_and_invalid_input(self):
        p = construct()
        outside = add(p[0], (q(2),q(2)))
        facts = inspect_center(p, outside)
        self.assertTrue(facts["perpendicular_feet"])
        self.assertFalse(facts["inside_every_halfplane"])
        self.assertFalse(facts["feet_strictly_inside_sides"])
        for radius, branch in ((0,1),(-2,1),(1.1,1),(1,0),(1,True)):
            with self.subTest(radius=radius, branch=branch):
                with self.assertRaises(ValueError):
                    construct(radius, branch)


if __name__ == "__main__":
    unittest.main()
