import unittest
from fractions import Fraction as F

from circumscribed_square import circumscribe, measurements, run_grid, tangent_quad, verify


class CircumscribedSquareTests(unittest.TestCase):

    def test_axes_and_contact_order(self):
        o, u = (0, 0), (2, 0)
        self.assertEqual(circumscribe(o, u), ((2, 2), (-2, 2), (-2, -2), (2, -2)))
        self.assertTrue(verify(o, u, circumscribe(o, u)))

    def test_rational_translation_and_irrational_radius(self):
        o, u = (F(1, 2), F(-1, 3)), (2, 1)
        vertices = ((F(3, 2), F(8, 3)), (F(-5, 2), F(2, 3)),
                    (F(-1, 2), F(-10, 3)), (F(7, 2), F(-4, 3)))
        self.assertEqual(circumscribe(o, u), vertices)
        self.assertEqual(measurements(vertices), ((20,)*4, (0,)*4, (40, 40), 20))
        self.assertTrue(verify(o, u, vertices))

    def test_rhombus_not_square(self):
        o, u, v = (0, 0), (5, 0), (3, 4)
        p = tangent_quad(o, u, v)
        self.assertEqual(p, ((5, F(5, 2)), (-5, 10), (-5, F(-5, 2)), (5, -10)))
        sides, dots, diags, area = measurements(p)
        self.assertEqual(sides, (F(625, 4),)*4)
        self.assertEqual(dots, (F(-375, 4), F(375, 4))*2)
        self.assertEqual((diags, area), ((125, 500), 125))
        self.assertFalse(verify(o, u, p))

    def test_crossed_and_wrong_size(self):
        o, u = (0, 0), (1, 0)
        a, b, c, d = circumscribe(o, u)
        self.assertFalse(verify(o, u, (a, c, b, d)))
        self.assertFalse(verify(o, u, circumscribe(o, (2, 0))))

    def test_cyclic_start_tracks_radius(self):
        p = circumscribe((0, 0), (2, 1))
        self.assertEqual(circumscribe((0, 0), (-1, 2)), p[1:] + p[:1])
        self.assertFalse(verify((0, 0), (2, 1), p[1:] + p[:1]))

    def test_degenerate(self):
        with self.assertRaisesRegex(ValueError, "zero"):
            circumscribe((0, 0), (0, 0))
        with self.assertRaisesRegex(ValueError, "nonparallel"):
            tangent_quad((0, 0), (1, 0), (-1, 0))
        with self.assertRaisesRegex(ValueError, "equal-length"):
            tangent_quad((0, 0), (1, 0), (0, 2))

    def test_exact_coordinates_only(self):
        for x in (1.0, True):
            with self.assertRaises(TypeError):
                circumscribe((0, 0), (x, 0))

    def test_grid(self):
        self.assertEqual(run_grid(), (360, 3))
