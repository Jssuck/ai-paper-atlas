from fractions import Fraction as F
from unittest import TestCase

from ratio_chains import construct


class TestMeanProportional(TestCase):
    def test_integer_square(self):
        c = construct(9, 16)
        self.assertEqual((c.center_x, c.radius), (F(7, 2), F(25, 2)))
        self.assertEqual(c.altitude_squared, 144)
        self.assertEqual(c.rational_altitude, 12)
        self.assertEqual(F(9, 12), F(12, 16))

    def test_irrational_height(self):
        c = construct(1, 2)
        self.assertEqual(c.altitude_squared, 2)
        self.assertIsNone(c.rational_altitude)

    def test_fraction_square(self):
        self.assertEqual(construct(F(1, 8), F(1, 2)).rational_altitude, F(1, 4))

    def test_nonsquare_denominator(self):
        self.assertIsNone(construct(1, F(1, 2)).rational_altitude)

    def test_equal_lengths_midpoint(self):
        c = construct(F(3, 7), F(3, 7))
        self.assertEqual(c.center_x, 0)
        self.assertEqual(c.rational_altitude, F(3, 7))

    def test_wrong_intersection_and_wrong_mean(self):
        c = construct(9, 16)
        self.assertTrue(c.center_x != 0)
        self.assertNotEqual(c.radius**2, c.altitude_squared)
        self.assertEqual(c.center_x**2 + c.radius**2, F(337, 2))
        self.assertNotEqual(11**2 + c.center_x**2, c.radius**2)

    def test_zero_and_negative_lengths(self):
        for a, b in [(0, 1), (1, 0), (-1, 2), (2, F(-3, 7))]:
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                construct(a, b)

    def test_forbid_uncontrolled_coercion(self):
        for value in (True, 1.0, "1"):
            with self.subTest(value=value), self.assertRaises(TypeError):
                construct(value, 2)

    def test_exact_grid_and_reflection(self):
        values = [F(n, 7) for n in range(1, 33)]
        for a in values:
            for b in values:
                with self.subTest(a=a, b=b):
                    c = construct(a, b)
                    self.assertLess(abs(c.center_x), c.radius)
                    self.assertEqual(c.altitude_squared, a * b)
                    self.assertEqual(c.right_angle_dot, 0)
                    reflected = construct(b, a)
                    self.assertEqual(reflected.center_x, -c.center_x)
                    self.assertEqual(reflected.altitude_squared, c.altitude_squared)
