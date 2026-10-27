"""Exact regression tests. No Python assert statement is used as a gate."""
import unittest
from dataclasses import replace
from decimal import Decimal, localcontext
from fractions import Fraction as R
from geometry import (Q3, ZERO, ONE, SQRT3, point, add, sub, scale, dot, cross,
                      norm2, dist2, equilateral_vertices, inside, equal_angles,
                      i9_vertex, intersect_open_ray_segment, construct,
                      check_certificate, accepted)
from cases import rejected_cases


class ExactFieldTests(unittest.TestCase):
    def test_field_identities(self):
        self.assertEqual(SQRT3 * SQRT3, Q3(3))
        for a in range(-4, 5):
            for b in range(-4, 5):
                x = Q3(R(a, 7), R(b, 11))
                self.assertEqual(x + -x, ZERO)
                self.assertEqual(x * (SQRT3 + ONE), x * SQRT3 + x)
                if x != ZERO:
                    self.assertEqual(x / x, ONE)
                    self.assertEqual(x * (ONE / x), ONE)
        with self.assertRaises(ZeroDivisionError):
            ONE / ZERO

    def test_exact_sign_against_independent_decimal(self):
        with localcontext() as ctx:
            ctx.prec = 100
            root = Decimal(3).sqrt()
            for a in range(-16, 17):
                for b in range(-16, 17):
                    approximate = Decimal(a) / Decimal(7) + Decimal(b) / Decimal(11) * root
                    self.assertEqual(Q3(R(a, 7), R(b, 11)).sign(),
                                     (approximate > 0) - (approximate < 0))

    def test_sign_near_cancellation_pell(self):
        a, b = 2, 1
        for _ in range(160):
            self.assertEqual(a*a - 3*b*b, 1)
            self.assertEqual(Q3(a, -b).sign(), 1)
            self.assertEqual(Q3(-a, b).sign(), -1)
            a, b = 2*a + 3*b, a + 2*b

    def test_reject_implicit_float_bool(self):
        for value in (0.1, True, '1/3'):
            with self.assertRaises(TypeError):
                Q3(value)


class ConstructionTests(unittest.TestCase):
    def setUp(self):
        self.a, self.b = point(0, 0), point(2, 0)

    def test_I1_two_equilateral_candidates(self):
        for c in equilateral_vertices(self.a, self.b):
            self.assertEqual(dist2(self.a, c), Q3(4))
            self.assertEqual(dist2(self.b, c), Q3(4))
        self.assertNotEqual(*equilateral_vertices(self.a, self.b))

    def test_both_I10_branches(self):
        certs = [construct(self.a, self.b, branch) for branch in (1, -1)]
        for cert in certs:
            self.assertTrue(accepted(self.a, self.b, cert))
            self.assertEqual(cert.d, point(1, 0))
            self.assertEqual(cert.s, Q3(R(1, 2)))
            self.assertEqual(cert.t, Q3(R(1, 2)))
        self.assertEqual(certs[0].c, certs[1].f)
        self.assertEqual(certs[0].f, certs[1].c)
        self.assertEqual(certs[0].d, certs[1].d)

    def test_vertical(self):
        a, b = point(-2, 7), point(-2, 13)
        self.assertEqual(construct(a, b).d, point(-2, 10))

    def test_oblique_rational(self):
        a, b = point(R(1, 3), R(-2, 5)), point(R(7, 3), R(8, 5))
        cert = construct(a, b)
        self.assertTrue(accepted(a, b, cert))
        # Midpoint is an independent output oracle here, not the construction.
        self.assertEqual(cert.d, point(R(4, 3), R(3, 5)))

    def test_article_worked_examples(self):
        cert = construct(point(0, 0), point(6, 0))
        self.assertEqual(cert.c, point(3, 3*SQRT3))
        self.assertEqual(cert.f, point(3, -3*SQRT3))
        self.assertEqual(cert.d, point(3, 0))
        self.assertEqual(dist2(point(0, 0), cert.c), Q3(36))
        self.assertEqual(dist2(cert.c, cert.d), Q3(27))
        self.assertEqual(dist2(point(0, 0), cert.d), Q3(9))
        a, b = point(-2, 1), point(4, 9)
        cert = construct(a, b)
        self.assertTrue(accepted(a, b, cert))
        self.assertEqual(cert.d, point(1, 5))
        self.assertEqual(dist2(a, cert.d), Q3(25))
        self.assertEqual(dist2(b, cert.d), Q3(25))

    def test_endpoint_reversal(self):
        a, b = point(R(1, 3), 4), point(7, R(-9, 5))
        x, y = construct(a, b, 1), construct(b, a, -1)
        self.assertEqual(x.c, y.c)
        self.assertEqual(x.d, y.d)
        self.assertTrue(accepted(b, a, y))

    def test_tiny_and_large(self):
        for n in (R(1, 10**200), R(10**200)):
            a, b = point(0, 0), point(2*n, 4*n)
            for branch in (1, -1):
                cert = construct(a, b, branch)
                self.assertTrue(accepted(a, b, cert))
                self.assertEqual(cert.d, point(n, 2*n))

    def test_large_translation_tiny_displacement(self):
        h, e = 10**150, R(1, 10**150)
        a, b = point(h, -h), point(h + 2*e, -h + 4*e)
        cert = construct(a, b)
        self.assertTrue(accepted(a, b, cert))
        self.assertEqual(cert.d, point(h + e, -h + 2*e))

    def test_reject_coincident_and_irrational_endpoints(self):
        for a, b in ((self.a, self.a), (point(SQRT3, 0), self.b)):
            with self.assertRaises(ValueError):
                construct(a, b)

    def test_reject_invalid_branch(self):
        for branch in (0, 2, True, '1'):
            with self.assertRaises(ValueError):
                construct(self.a, self.b, branch)

    def test_I9_invalid_equal_cuts(self):
        with self.assertRaises(ValueError):
            i9_vertex(point(0, 1), self.a, self.b)
        with self.assertRaises(ValueError):
            i9_vertex(point(1, 0), self.a, self.b)


class IntersectionAndCertificateTests(unittest.TestCase):
    def setUp(self):
        self.a, self.b = point(0, 0), point(2, 0)
        self.cert = construct(self.a, self.b)

    def test_solver_not_a_midpoint_assignment(self):
        # Deliberately non-bisecting ray intersects a different segment at t=1/3.
        d, s, t = intersect_open_ray_segment(point(1, 2), point(0, -1), point(0, 0), point(3, 0))
        self.assertEqual(d, point(1, 0))
        self.assertEqual(s, Q3(2))
        self.assertEqual(t, Q3(R(1, 3)))

    def test_solver_rejects_invalid_intersections(self):
        for origin, direction in (
            (point(1, 1), point(0, 0)),  # zero direction
            (point(1, 1), point(1, 0)),  # parallel
            (point(1, 0), point(1, 0)),  # coincident line
            (point(1, 1), point(0, 1)),  # line intersection behind ray
            (point(0, 1), point(0, -1)), # endpoint, not strictly interior
            (point(3, 1), point(0, -1)), # beyond segment
            (point(1, 0), point(0, -1)), # intersection at ray origin
        ):
            with self.subTest(origin=origin, direction=direction):
                with self.assertRaises(ValueError):
                    intersect_open_ray_segment(origin, direction, self.a, self.b)
        with self.assertRaises(ValueError):
            intersect_open_ray_segment(point(1, 1), point(0, -1), self.a, self.a)

    def test_equal_distance_not_midpoint(self):
        cert = replace(self.cert, d=self.cert.c)
        checks = check_certificate(self.a, self.b, cert)
        self.assertTrue(checks['conclusion_AD_equals_DB'])
        self.assertFalse(checks['intersection_collinear_AB'])
        self.assertFalse(accepted(self.a, self.b, cert))

    def test_reverse_equal_angle_ray_is_not_internal(self):
        cert = replace(self.cert, f=sub(scale(2, self.cert.c), self.cert.f), s=-self.cert.s)
        checks = check_certificate(self.a, self.b, cert)
        self.assertTrue(checks['I9_equal_angles'])
        self.assertTrue(checks['intersection_on_claimed_ray'])
        self.assertFalse(checks['I9_strictly_inside'])
        self.assertFalse(checks['intersection_positive_ray_parameter'])
        self.assertFalse(accepted(self.a, self.b, cert))

    def test_wrong_interior_ray(self):
        cert = replace(self.cert, f=point(R(1, 2), 0))
        checks = check_certificate(self.a, self.b, cert)
        self.assertTrue(checks['I9_strictly_inside'])
        self.assertFalse(checks['I9_equal_angles'])
        self.assertFalse(accepted(self.a, self.b, cert))

    def test_all_rejected_cases(self):
        for label, a, b, cert in rejected_cases():
            with self.subTest(label=label):
                self.assertFalse(accepted(a, b, cert))

    def test_checker_binds_trusted_input(self):
        self.assertFalse(accepted(self.a, point(4, 0), self.cert))

    def test_tamper_each_claimed_field(self):
        mutations = {'branch': -1, 'c': point(1, 2), 'f': self.a,
                     'd': point(R(3, 4), 0), 's': Q3(R(1, 3)), 't': Q3(R(1, 3))}
        for key, value in mutations.items():
            with self.subTest(field=key):
                self.assertFalse(accepted(self.a, self.b, replace(self.cert, **{key: value})))

    def test_malformed_certificate(self):
        for bad in (None, {}, replace(self.cert, branch=True), replace(self.cert, t=0.5)):
            self.assertFalse(accepted(self.a, self.b, bad))

    def test_angle_predicate_sign_and_zero(self):
        self.assertFalse(equal_angles(point(1, 0), point(-1, 0), point(1, 1)))
        self.assertFalse(equal_angles(point(1, 0), point(0, 1), point(0, 0)))
        self.assertFalse(inside(point(1, 0), point(-1, 0), point(0, 1)))


if __name__ == '__main__':
    unittest.main(verbosity=2)
