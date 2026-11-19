import unittest
from fractions import Fraction as Q
from math import hypot, pi, tau
from bisect_arc import SelectedArc, cross, dot, grid, square, sub


class ArcBisectorTests(unittest.TestCase):
    def test_grid_geometric_witness(self):
        count = 0
        for arc, expected in grid():
            d, opposite = arc.endpoints_on_bisector()
            mid = arc.chord_midpoint()
            u = sub(arc.b, arc.a)
            du, dv = sub(d, mid), sub(opposite, mid)
            radius = hypot(*sub(arc.a, arc.center))
            for z, offset in ((d, du), (opposite, dv)):
                self.assertAlmostEqual(dot(u, offset), 0, delta=2e-12)
                self.assertAlmostEqual(hypot(*sub(z, arc.center)), radius, delta=2e-12)
                self.assertAlmostEqual(square(sub(z, arc.a)), square(sub(z, arc.b)), delta=2e-12)
            self.assertLess(arc.direction*cross(u, du), 0)
            self.assertGreater(arc.direction*cross(u, dv), 0)
            for p, q in zip(d, expected):
                self.assertAlmostEqual(p, float(q), delta=2e-12)
            count += 1
        self.assertEqual(count, 2808)

    def test_grid_angle_split(self):
        counts = {"minor": 0, "half": 0, "major": 0}
        for arc, _ in grid():
            d, opposite = arc.endpoints_on_bisector()
            a, b = arc.parts(d)
            c, e = arc.parts(opposite)
            full = arc.full_sweep()
            key = ("half" if abs(full-pi) < 2e-12 else
                   "minor" if full < pi else "major")
            counts[key] += 1
            for x in (a, b):
                self.assertTrue(0 < x < min(pi, full))
            self.assertAlmostEqual(a, b, delta=2e-12)
            self.assertAlmostEqual(a+b, full, delta=2e-12)
            self.assertTrue(c > full and e > full)
            self.assertAlmostEqual(c, e, delta=2e-12)
            self.assertAlmostEqual(c+e, full+tau, delta=2e-12)
        self.assertEqual(counts, {"minor": 1326, "half": 156, "major": 1326})

    def test_minor_and_major_same_endpoints(self):
        a, b = (3, -4), (3, 4)
        minor = SelectedArc((0, 0), a, b, 1)
        major = SelectedArc((0, 0), a, b, -1)
        self.assertEqual(minor.endpoints_on_bisector(), ((5, 0), (-5, 0)))
        self.assertEqual(major.endpoints_on_bisector(), ((-5, 0), (5, 0)))
        for arc, squared in ((minor, 20), (major, 80)):
            d, wrong = arc.endpoints_on_bisector()
            self.assertEqual((square(sub(d, a)), square(sub(d, b))), (squared, squared))
            self.assertGreater(sum(arc.parts(wrong)), tau)

    def test_semicircles_require_direction(self):
        a, b = (6, 1), (-4, 1)
        for direction in (1, -1):
            arc = SelectedArc((1, 1), a, b, direction)
            d, _ = arc.endpoints_on_bisector()
            self.assertEqual(d, (1, 1+5*direction))
            self.assertEqual(arc.full_sweep(), pi)
            self.assertEqual(arc.parts(d), (pi/2, pi/2))

    def test_rational_chord_midpoint(self):
        arc = SelectedArc((0, 0), (0, 1), (1, 0), -1)
        self.assertEqual(arc.chord_midpoint(), (Q(1, 2), Q(1, 2)))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            SelectedArc((0, 0), (3, 4), (3, 4), 1)
        with self.assertRaises(ValueError):
            SelectedArc((0, 0), (3, 4), (4, 4), 1)
        with self.assertRaises(ValueError):
            SelectedArc((0, 0), (3, 4), (3, -4), 0)
        with self.assertRaises(TypeError):
            SelectedArc((0, 0), (3.0, 4), (3, -4), -1)


if __name__ == "__main__":
    unittest.main()
