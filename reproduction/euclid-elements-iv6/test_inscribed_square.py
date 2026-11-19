"""Regression checks for IV.6 teaching model (also active in -O/-OO)."""
from fractions import Fraction as F
from unittest import TestCase

from inscribed_square import inscribe, grid_sweep, measurements, rectangle_control, verify


class InscribedSquareTests(TestCase):
    def test_axis_aligned_diameters(self):
        o, a = (0, 0), (0, 1)
        p = inscribe(o, a)
        self.assertEqual(p, ((0, 1), (-1, 0), (0, -1), (1, 0)))
        self.assertEqual(verify(o, a, p)["signed_area"], 2)

    def test_rational_center_nonsquare_radius_squared(self):
        o, a = (F(1, 2), F(-1, 3)), (F(5, 2), F(2, 3))
        p = inscribe(o, a)
        self.assertEqual(p, (a, (F(-1, 2), F(5, 3)), (F(-3, 2), F(-4, 3)),
                             (F(3, 2), F(-7, 3))))
        m = verify(o, a, p)
        self.assertEqual(m["radii_squared"], (5,) * 4)
        self.assertEqual(m["sides_squared"], (10,) * 4)
        self.assertEqual(m["diagonals_squared"], (20, 20))
        self.assertEqual(m["signed_area"], 10)

    def test_nonsquare_rectangle_preserves_right_angles(self):
        p = rectangle_control()
        m = measurements((0, 0), p)
        self.assertEqual(m["radii_squared"], (25,) * 4)
        self.assertEqual(m["adjacent_dot"], (0,) * 4)
        self.assertEqual(m["sides_squared"], (20, 80, 20, 80))
        self.assertEqual(m["diagonals_squared"], (100, 100))
        self.assertEqual(m["diagonal_dot"], 60)
        with self.assertRaises(ValueError):
            verify((0, 0), p[0], p)

    def test_crossed_order_of_correct_vertices_is_not_a_square(self):
        a, b, c, d = inscribe((0, 0), (1, 0))
        p = a, c, b, d
        self.assertEqual(measurements((0, 0), p)["signed_area"], 0)
        with self.assertRaises(ValueError):
            verify((0, 0), a, p)

    def test_zero_radius_rejected(self):
        with self.assertRaises(ValueError):
            inscribe((F(1, 3), 2), (F(1, 3), 2))

    def test_inexact_and_boolean_rejected(self):
        for a in ((0.0, 1), (True, 1)):
            with self.subTest(a=a), self.assertRaises(TypeError):
                inscribe((0, 0), a)

    def test_cyclic_choice_of_start_rotates_sequence(self):
        o, a = (3, 4), (1, 5)
        p = inscribe(o, a)
        for i, first in enumerate(p):
            with self.subTest(i=i):
                self.assertEqual(inscribe(o, first), p[i:] + p[:i])

    def test_grid(self):
        self.assertEqual(grid_sweep(), (360, 3))
