"""Focused geometry and input-boundary checks."""
import unittest
from fractions import Fraction as F
import circumcircle as g


def p(x,y):
    return g.q(x), g.q(y)


class CircumcircleTests(unittest.TestCase):
    def test_exact_grid(self):
        self.assertEqual(g.check_grid(), (96, 96, 96))

    def test_worked_moved_a(self):
        _, regular, moved, _ = g.fixtures(1, 1)
        center = g.center_from_bisectors(regular)
        self.assertEqual(g.center_from_bisectors(moved), center)
        self.assertEqual(g.circumcenter_three(*moved[1:4]), center)
        self.assertEqual(g.vertex_squares(moved, center), (g.q(F(121,100)),)+(g.q(1),)*4)

    def test_cyclic_nonregular(self):
        pts = g.cyclic_nonregular()
        self.assertEqual(g.boundary_sign(pts), 1)
        center = g.circumcenter_three(*pts[1:4])
        self.assertEqual(center, p(0,0))
        self.assertEqual(g.vertex_squares(pts, center), (g.q(1),)*5)
        self.assertGreater(len({g.norm(g.sub(b,a)) for a,b in g.edges(pts)}), 1)
        with self.assertRaises(ValueError):
            g.center_from_bisectors(pts)

    def test_reject_collinear_triple(self):
        with self.assertRaisesRegex(ValueError, "noncollinear"):
            g.circumcenter_three(p(0,0), p(1,0), p(3,0))

    def test_reject_repeated_points(self):
        a,b,c,d,e = g.construct()
        with self.assertRaises(ValueError):
            g.center_from_bisectors((a,b,c,c,e))

    def test_reject_crossed_order(self):
        a,b,c,d,e = g.construct()
        with self.assertRaises(ValueError):
            g.center_from_bisectors((a,c,b,d,e))

    def test_circumcenter_not_in_acute_wedge(self):
        # A very flat isosceles triangle; all input y coefficients are >=0.
        a,b,c = p(-2,0), p(2,0), p(0,1)
        center = g.circumcenter_three(a,b,c)
        self.assertLess(center[1].sign(), 0)
        self.assertEqual(len(set(g.vertex_squares((a,b,c),center))), 1)

    def test_radii_differ(self):
        a,b,*_ = g.construct()
        center = p(0,0)
        midpoint = g.scale(g.add(a,b),F(1,2))
        outer = g.vertex_squares((a,),center)[0]
        inner = g.vertex_squares((midpoint,),center)[0]
        self.assertEqual(outer, g.q(1))
        self.assertEqual(inner, g.Q5(F(3,8), F(1,8)))
        self.assertGreater((outer-inner).sign(),0)
