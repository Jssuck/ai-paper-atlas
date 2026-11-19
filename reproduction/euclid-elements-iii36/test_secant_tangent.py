from unittest import TestCase

from secant_tangent import (
    DIAMETER, OFFSET, O, Q, add, mul, point, sweep, verify,
)


class SecantTangentTests(TestCase):
    def test_diameter(self):
        cert = verify(*DIAMETER)
        self.assertEqual((cert["branch"], cert["product"]), ("diameter", 144))
        self.assertEqual(cert["center_offset_squared"], 0)

    def test_offset(self):
        cert = verify(*OFFSET)
        self.assertEqual((cert["branch"], cert["product"]), ("offset", 9))
        self.assertEqual(cert["half_chord_squared"], 16)
        self.assertEqual(cert["center_offset_squared"], 9)

    def test_similarity(self):
        o, r, d, c, a, b = OFFSET
        k, shift = Q(2, 3), point(Q(5, 9), -7)

        def transformed(p):
            return add(mul(k, (-p[1], p[0])), shift)

        cert = verify(transformed(o), k*r, *(transformed(p) for p in (d, c, a, b)))
        self.assertEqual(cert["product"], k*k*9)

    def test_malformed_secant(self):
        o, r, d, c, a, b = OFFSET
        for near, far in ((a, c), (c, c), (b, a)):
            with self.subTest(near=near, far=far):
                with self.assertRaisesRegex(ValueError, "secant order"):
                    verify(o, r, d, near, far, b)

    def test_b_on_circle_but_not_tangent(self):
        o, r, d, c, a, _ = DIAMETER
        with self.assertRaisesRegex(ValueError, "tangent at B"):
            verify(o, r, d, c, a, point(0, 5))

    def test_premise_checks(self):
        o, r, d, c, a, b = OFFSET
        for radius, d0 in [(0, d), (-5, d), (r, O), (r, c)]:
            with self.subTest(radius=radius, d=d0):
                with self.assertRaisesRegex(ValueError, "positive radius and exterior"):
                    verify(o, radius, d0, c, a, b)
        with self.assertRaisesRegex(ValueError, "must be on the circle"):
            verify(o, r, d, c, point(-3, 3), b)

    def test_other_tangent_same_square(self):
        o, r, d, c, a, b = DIAMETER
        self.assertEqual(verify(o, r, d, c, a, (b[0], -b[1])), verify(*DIAMETER))

    def test_sweep(self):
        self.assertEqual(sweep(), {"diameter": 120, "offset": 440})
