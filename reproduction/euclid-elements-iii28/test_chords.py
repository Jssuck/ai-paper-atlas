import math
import unittest
from fractions import Fraction
from chords import Chord, pair_family, point, polyline_arc_estimate, unequal_radius_pair


class ChordTests(unittest.TestCase):
    def test_grid_exact_chord_and_center_geometry(self):
        count = 0
        for a, b in pair_family():
            self.assertEqual(a.r2, b.r2)
            self.assertEqual(a.c2, b.c2)
            self.assertEqual(a.midpoint_d2(), b.midpoint_d2())
            for c in (a, b):
                self.assertEqual(c.midpoint_d2() + Fraction(c.c2, 4), c.r2)
                self.assertEqual(c.cos_signature(), 1 - Fraction(c.c2, 2*c.r2))
            count += 1
        self.assertEqual(count, 1560)

    def test_grid_angles_from_raw_endpoints(self):
        count = 0
        for a, b in pair_family():
            am, aM = a.endpoint_arcs()
            bm, bM = b.endpoint_arcs()
            self.assertTrue(0 < am < math.pi < aM < math.tau)
            self.assertTrue(0 < bm < math.pi < bM < math.tau)
            self.assertAlmostEqual(am, bm, delta=3e-14)
            self.assertAlmostEqual(aM, bM, delta=3e-14)
            self.assertAlmostEqual(math.cos(am), float(a.cos_signature()), delta=3e-14)
            self.assertAlmostEqual(math.cos(bm), float(b.cos_signature()), delta=3e-14)
            count += 1
        self.assertEqual(count, 1560)

    def test_polylines_are_numerical_not_exact_lengths(self):
        a, b = next(pair_family())
        for x, y in zip(a.endpoint_sweeps(), b.endpoint_sweeps()):
            # Read both endpoint-derived sweeps rather than passing a shared angle.
            samples = [polyline_arc_estimate(a, x, n) for n in (8, 32, 128)]
            self.assertTrue(samples[0] < samples[1] < samples[2] < abs(x))
            self.assertAlmostEqual(samples[-1], polyline_arc_estimate(b, y, 128), delta=3e-14)

    def test_wrong_matching(self):
        a, b = next(pair_family())
        self.assertLess(a.endpoint_arcs()[0], math.pi)
        self.assertGreater(b.endpoint_arcs()[1], math.pi)
        self.assertNotAlmostEqual(a.endpoint_arcs()[0], b.endpoint_arcs()[1])

    def test_unequal_radii_break_both_arc_lengths(self):
        a, b = unequal_radius_pair()
        self.assertEqual((a.r2, b.r2, a.c2, b.c2), (169, 225, 576, 576))
        self.assertNotEqual(a.cos_signature(), b.cos_signature())
        for x, y in zip(a.endpoint_arcs(), b.endpoint_arcs()):
            self.assertNotAlmostEqual(13*x, 15*y, delta=1e-3)

    def test_diameter_tie(self):
        a = Chord(point(0, 0), point(5, 0), point(-5, 0))
        b = Chord(point(3, 1), point(6, 5), point(0, -3))
        self.assertEqual(a.c2, b.c2)
        for c in (a, b):
            self.assertTrue(c.diameter)
            self.assertEqual(c.endpoint_arcs(), (math.pi, math.pi))
            self.assertEqual(c.cos_signature(), -1)
            self.assertEqual(c.midpoint_d2(), 0)

    def test_invalid_endpoints(self):
        o = point(0, 0)
        with self.assertRaises(ValueError):
            Chord(o, point(5, 0), point(5, 0))
        with self.assertRaises(ValueError):
            Chord(o, point(5, 0), point(4, 0))
        with self.assertRaises(TypeError):
            Chord(o, (5.0, 0), (0, 5))


if __name__ == "__main__":
    unittest.main()
