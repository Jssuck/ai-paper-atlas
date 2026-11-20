import unittest
from fractions import Fraction

from polygon15 import (PHI15, ZERO, certify, chord_sq, grid, half_arc, mul,
                       reduce_poly, root, step_exponent, walk)


class PolygonTests(unittest.TestCase):
    def test_cyclotomic_field(self):
        self.assertEqual(reduce_poly(PHI15), ZERO)
        self.assertEqual(root(0), root(15))
        self.assertEqual(len({root(i) for i in range(15)}), 15)
        for k in range(15):
            self.assertEqual(mul(root(k), root(-k)), root(0))

    def test_source_arcs(self):
        self.assertEqual(half_arc(), Fraction(1, 15))
        self.assertEqual(half_arc(pentagon_direction=-1, triangle_direction=-1),
                         Fraction(-1, 15))

    def test_euclid_walk(self):
        self.assertTrue(certify(walk(3, step_exponent(half_arc()))).regular)

    def test_exact_scale(self):
        # Triangle side length squared 3 and pentagon side nonzero in unit circle.
        self.assertEqual(chord_sq(0, 5), (3,) + (0,) * 7)
        self.assertNotEqual(chord_sq(0, 3), ZERO)
        self.assertEqual(chord_sq(3, 4), chord_sq(4, 5))

    def test_opposite_side(self):
        turn = half_arc(pentagon_direction=-1)
        self.assertEqual(turn, Fraction(4, 15))
        c = certify(walk(3, step_exponent(turn)))
        self.assertTrue(c.closed and c.distinct and c.equal_sides and c.equal_angles)
        self.assertFalse(c.boundary_order or c.regular)

    def test_major_arc_outside_model(self):
        turn = half_arc(major=True)
        self.assertEqual(turn, Fraction(13, 30))
        with self.assertRaisesRegex(ValueError, "outside"):
            step_exponent(turn)
        self.assertEqual((30 * turn) % 1, 0)
        self.assertNotEqual((15 * turn) % 1, 0)
        other = half_arc(pentagon_direction=-1, major=True)
        self.assertEqual(other, Fraction(7, 30))
        with self.assertRaisesRegex(ValueError, "outside"):
            step_exponent(other)

    def test_early_closure(self):
        c = certify(walk(0, 5))
        self.assertTrue(c.closed)
        self.assertFalse(c.distinct or c.regular)

    def test_wrong_order_and_missing_return(self):
        p = walk(0, 1)
        self.assertFalse(certify(p[:1] + p[2:3] + p[1:2] + p[3:]).regular)
        c = certify(p[:-1] + (p[-2],))
        self.assertTrue(c.distinct)
        self.assertFalse(c.closed or c.regular)

    def test_all_grid_controls(self):
        self.assertEqual(grid(), (30, 30, 30))


if __name__ == "__main__":
    unittest.main()
