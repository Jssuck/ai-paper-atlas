import unittest
from fractions import Fraction as F

from tangent_pentagon import (U, Q5, check_grid, construct, dot, envelope,
                              envelope_checks, irregular_contacts, q, sub,
                              tangent_intersection, wrong_order)


class TangentPentagonTests(unittest.TestCase):
    def test_exact_grid(self):
        self.assertEqual(check_grid(), (96,96,96))

    def test_intersection_solves_both_lines(self):
        pts = construct(F(5,7))
        vertices = envelope(pts)
        for i,v in enumerate(vertices):
            a,b = pts[i],pts[(i+1)%5]
            self.assertEqual(dot(a,v), dot(a,a))
            self.assertEqual(dot(b,v), dot(b,b))

    def test_touchpoints_are_midpoints_in_regular_case(self):
        pts = construct(3)
        vs = envelope(pts)
        for i,p in enumerate(pts):
            a,b = vs[i-1],vs[i]
            self.assertEqual(tuple((x+y)/2 for x,y in zip(a,b)), p)
            self.assertEqual(dot(p,sub(b,a)), q(0))

    def test_unit_radical_lengths(self):
        vs = envelope(construct())
        side = sub(vs[0],vs[1])
        self.assertEqual(dot(side,side), Q5(20,-8))
        self.assertEqual(dot(vs[0],vs[0]), Q5(6,-2))
        self.assertEqual(4*U*U+2*U-1,q(0))

    def test_reflection_and_scaling(self):
        vs = envelope(construct())
        r = F(11,5)
        new = envelope(construct(r,-1))
        self.assertEqual(new,tuple((x*r,-y*r) for x,y in vs))

    def test_wrong_order_fools_local_checks(self):
        x = envelope_checks(wrong_order(construct()))
        for k in ("tangent_lines","contacts_on_side_segments",
                  "equal_sides","equal_ordinary_angles"):
            self.assertTrue(x[k])
        self.assertEqual(x["strict_crossings"],5)
        self.assertFalse(x["inside_all_tangent_halfplanes"])
        self.assertFalse(x["convex_envelope"])
        self.assertFalse(x["angles_108"])

    def test_irregular_controls_are_still_tangent(self):
        x = envelope_checks(irregular_contacts(F(7,2),-1))
        for k in ("tangent_lines","contacts_on_side_segments",
                  "inside_all_tangent_halfplanes","convex_envelope"):
            self.assertTrue(x[k])
        self.assertFalse(x["equal_sides"])
        self.assertFalse(x["equal_ordinary_angles"])

    def test_invalid_or_parallel_inputs(self):
        for radius, direction in ((0,1),(-2,1),(True,1),(1.0,1),(1,0),(1,True)):
            with self.subTest(radius=radius, direction=direction), self.assertRaises(ValueError):
                construct(radius,direction)
        a,b,c,d,e = construct()
        for contacts in ((a,b,c,d),(a,b,c,d,a),(a,b,c,d,(q(0),q(0))),
                         (a,(-a[0],-a[1]),c,d,e)):
            with self.subTest(contacts=contacts), self.assertRaises(ValueError):
                envelope(contacts)
        with self.assertRaises(ValueError):
            tangent_intersection(a,a)


if __name__ == "__main__":
    unittest.main()
