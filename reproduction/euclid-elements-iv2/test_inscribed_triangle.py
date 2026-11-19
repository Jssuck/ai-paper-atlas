from fractions import Fraction as Q
import unittest
from inscribed_triangle import OBTUSE, angle_keys, inscribe, second_hit, sweep, verifies


EXPECTED = {"acute": 128, "right": 320, "obtuse": 544, "degenerate": 258}

class InscribedTriangleTests(unittest.TestCase):
    def test_obtuse_e(self):
        expected = ((0, 0), (Q(-100, 29), Q(40, 29)), (-4, 8))
        self.assertEqual(inscribe(OBTUSE, 5), expected)
        self.assertLess(angle_keys(expected)[1], 0)
        self.assertTrue(verifies(OBTUSE, expected, 5))

    def test_obtuse_f(self):
        d, e, f = OBTUSE
        template = d, f, e
        result = inscribe(template, 5)
        self.assertLess(angle_keys(result)[2], 0)
        self.assertTrue(verifies(template, result, 5))

    def test_right(self):
        template = (0, 1), (0, 0), (4, 0)
        result = inscribe(template, Q(3, 2))
        self.assertEqual(result[2], (0, 3))
        self.assertTrue(verifies(template, result, Q(3, 2)))

    def test_wrong_label(self):
        a, b, c = inscribe(OBTUSE, 5)
        self.assertFalse(verifies(OBTUSE, (a, c, b), 5))

    def test_scaled_same_angles_but_off_circle(self):
        a, b, c = inscribe(OBTUSE, 5)
        scaled = a, (2*b[0], 2*b[1]), (2*c[0], 2*c[1])
        self.assertEqual(angle_keys(scaled), angle_keys(OBTUSE))
        self.assertFalse(verifies(OBTUSE, scaled, 5))

    def test_degenerate_and_domain(self):
        with self.assertRaises(ValueError):
            inscribe(((0, 0), (1, 1), (2, 2)), 5)
        with self.assertRaises(ValueError):
            inscribe(OBTUSE, 0)
        with self.assertRaises(TypeError):
            inscribe(OBTUSE, 1.5)

    def test_tangent_or_outward_ray(self):
        for q in ((1, 0), (1, -1)):
            with self.assertRaises(ValueError):
                second_hit(Q(5), q)

    def test_grid(self):
        self.assertEqual(sweep(), EXPECTED)


if __name__ == "__main__":
    unittest.main()
