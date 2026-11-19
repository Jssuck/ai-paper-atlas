import unittest
from fractions import Fraction as F

from golden_triangle import GOLDEN_SPLIT, Q5, check_grid, construct


class TriangleTests(unittest.TestCase):
    def test_split_field_identity_and_other_root(self):
        t = GOLDEN_SPLIT
        self.assertEqual(t * t + t - 1, Q5())
        other = -1 - t
        self.assertEqual(other * other + other - 1, Q5())
        self.assertLess(other.sign(), 0)
        with self.assertRaises(ValueError):
            construct(t=other)

    def test_exact_sign_and_division(self):
        self.assertGreater(Q5(-2, 1).sign(), 0)
        self.assertLess(Q5(-3, 1).sign(), 0)
        self.assertGreater(Q5(3, -1).sign(), 0)
        self.assertLess(Q5(2, -1).sign(), 0)
        self.assertEqual(Q5(2, 1) / Q5(2, 1), Q5(1))
        with self.assertRaises(ZeroDivisionError):
            Q5(2) / Q5()

    def test_exact_grid(self):
        self.assertEqual(check_grid(), (96, 8))

    def test_reflection(self):
        upper, lower = construct(F(5, 3), branch=1), construct(F(5, 3), branch=-1)
        self.assertEqual(upper.checks(), lower.checks())
        for a, b in ((upper.D, lower.D), (upper.O, lower.O)):
            self.assertEqual(a[0], b[0])
            self.assertEqual(a[1], -b[1])

    def test_scale(self):
        a, b = construct(), construct(F(7, 5))
        self.assertEqual(b.dist2(b.B, b.D), F(49, 25) * a.dist2(a.B, a.D))

    def test_equal_chord_does_not_imply_tangency(self):
        c = construct(t=F(1, 2)).checks()
        self.assertTrue(c["given_circle_and_chord"])
        self.assertTrue(c["point_power"])
        self.assertFalse(c["tangent_at_D"])
        self.assertFalse(c["both_base_angles_double"])

    def test_invalid_inputs(self):
        for kwargs in ({"scale": 0}, {"scale": -1}, {"t": 0}, {"t": 1},
                       {"t": F(5, 4)}, {"t": -1}, {"branch": 0}, {"branch": True}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                construct(**kwargs)

    def test_float_rejected(self):
        with self.assertRaises(TypeError):
            construct(t=.5)
        with self.assertRaises(ValueError):
            construct(scale=1.5)


if __name__ == "__main__":
    unittest.main()
