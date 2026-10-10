"""Deterministic tests; finite test counts do not establish universal theorems."""
import math
import unittest
from fractions import Fraction

from sylvester import (DomainError, DegenerateIntersection, Triangle, bisect_root,
    bisector_squares, circle_chord, cross_residual, divider_geometry,
    factor_polynomial, factored_bisector_difference, near_segment,
    opposite_sign_example, exact_opposite_sign_example, parameters, remote_segment, sine_residual, tangent_ratios)


class TriangleDomainTests(unittest.TestCase):
    def test_valid_triangle(self):
        t = Triangle(30, 60)
        self.assertAlmostEqual(t.C[0], 0.75)
        self.assertAlmostEqual(t.C[1], math.sqrt(3)/4)

    def test_invalid_angles_and_base(self):
        for args in [(0, 60), (-1, 60), (90, 90), (100, 81),
                     (math.nan, 60), (30, math.inf), (30, 60, 0)]:
            with self.subTest(args=args), self.assertRaises(DomainError): Triangle(*args)

    def test_invalid_n(self):
        for n in [0, math.inf, -math.inf, math.nan]:
            with self.subTest(n=n), self.assertRaises(DomainError): parameters(Triangle(30, 60), n)

    def test_negative_n_keeps_signed_alpha_beta(self):
        alpha, beta, theta, phi = parameters(Triangle(15, 105), -0.5)
        self.assertAlmostEqual(math.degrees(alpha-beta), 90)
        self.assertLess(alpha, 0)
        self.assertLess(beta, 0)


class DividerTests(unittest.TestCase):
    def test_n2_is_internal(self):
        g = divider_geometry(Triangle(50, 70), 2)
        self.assertTrue(g.both_internal_cevians)
        self.assertTrue(g.both_forward_rays)
        self.assertNotAlmostEqual(g.t_A, g.t_B)

    def test_n2_isosceles_equal(self):
        g = divider_geometry(Triangle(50, 50, 3), 2)
        self.assertAlmostEqual(g.t_A, g.t_B)
        self.assertAlmostEqual(sine_residual(g.triangle, 2), 0)

    def test_line_incidence_independently(self):
        for A, B, n in [(50,70,2), (30,60,.5), (15,105,-.5), (90,20,-2), (40,60,1)]:
            with self.subTest(A=A, B=B, n=n):
                g = divider_geometry(Triangle(A, B), n)
                C = g.triangle.C
                self.assertAlmostEqual((g.D[0]-1)*C[1]-g.D[1]*(C[0]-1), 0)
                self.assertAlmostEqual(g.E[0]*C[1]-g.E[1]*C[0], 0)
                self.assertAlmostEqual(math.hypot(*g.D), abs(g.t_A))
                self.assertAlmostEqual(math.hypot(g.E[0]-1,g.E[1]), abs(g.t_B))

    def test_positive_half_equal_extensions(self):
        g = divider_geometry(Triangle(30,60), .5)
        self.assertAlmostEqual(g.t_A, 1)
        self.assertAlmostEqual(g.t_B, 1)
        self.assertTrue(g.both_forward_rays)
        self.assertFalse(g.both_internal_cevians)
        self.assertAlmostEqual(g.bc_fraction, 2)
        self.assertAlmostEqual(g.ac_fraction, 2)
        self.assertAlmostEqual(sine_residual(g.triangle, .5), 0)

    def test_negative_half_equal_extensions(self):
        g = divider_geometry(Triangle(15,105), -.5)
        self.assertAlmostEqual(g.t_A, 1)
        self.assertAlmostEqual(g.t_B, 1)
        self.assertTrue(g.both_forward_rays)
        self.assertFalse(g.both_internal_cevians)
        self.assertAlmostEqual(sine_residual(g.triangle, -.5), 0)

    def test_n1_meets_at_vertex(self):
        g = divider_geometry(Triangle(40,60), 1)
        for p in [g.D, g.E]:
            for got, want in zip(p, g.triangle.C): self.assertAlmostEqual(got, want)
        self.assertFalse(g.both_internal_cevians)
        self.assertNotAlmostEqual(g.t_A, g.t_B)

    def test_negative_one_isosceles_is_parallel_despite_zero_residual(self):
        t = Triangle(50,50)
        self.assertAlmostEqual(cross_residual(t, -1), 0)
        self.assertAlmostEqual(sine_residual(t, -1), 0)
        with self.assertRaises(DegenerateIntersection): divider_geometry(t,-1)

    def test_negative_one_nonisosceles_has_opposite_signs(self):
        g = divider_geometry(Triangle(40,60), -1)
        self.assertLess(g.t_A*g.t_B, 0)
        self.assertFalse(g.both_forward_rays)

    def test_parallel_in_other_case(self):
        with self.assertRaises(DegenerateIntersection): divider_geometry(Triangle(30,60),-.5)

    def test_opposite_sign_branch_is_not_original_signed_equation(self):
        g = opposite_sign_example()
        self.assertNotAlmostEqual(g.triangle.A_deg, g.triangle.B_deg)
        self.assertAlmostEqual(abs(g.t_A), abs(g.t_B), places=12)
        self.assertLess(g.t_A*g.t_B, 0)
        self.assertGreater(abs(sine_residual(g.triangle,g.n)), 1)
        self.assertFalse(g.both_forward_rays)

    def test_exact_opposite_sign_example(self):
        g = exact_opposite_sign_example()
        self.assertAlmostEqual(g.t_A,-1,places=14)
        self.assertAlmostEqual(g.t_B,1,places=14)
        self.assertFalse(g.both_forward_rays)
        self.assertNotAlmostEqual(sine_residual(g.triangle,g.n),0)

    def test_scaling(self):
        a = divider_geometry(Triangle(50,70), 2)
        b = divider_geometry(Triangle(50,70,10), 2)
        self.assertAlmostEqual(b.t_A, 10*a.t_A)
        self.assertAlmostEqual(b.t_B, 10*a.t_B)

    def test_sine_and_cross_equations_consistent(self):
        t = Triangle(40,60)
        for n in [-3,-.5,.5,1,2,3]:
            self.assertAlmostEqual(cross_residual(t,n), sine_residual(t,n)*math.sin(t.A)*math.sin(t.B))


class TangentAuditTests(unittest.TestCase):
    def test_half_sine_factorizations(self):
        for A in range(5, 175, 10):
            for B in range(5, 180-A, 10):
                t=Triangle(A,B)
                plus=-math.sin(2*(t.A+t.B))*math.sin(t.A-t.B)
                minus=math.sin(2*(t.A-t.B))*math.sin(t.A+t.B)
                self.assertAlmostEqual(cross_residual(t,.5),plus,places=12)
                self.assertAlmostEqual(cross_residual(t,-.5),minus,places=12)

    def test_half_cases_have_minus_one(self):
        for A,B,n in [(30,60,.5),(15,105,-.5)]:
            with self.subTest(n=n):
                left,right = tangent_ratios(Triangle(A,B), n)
                self.assertAlmostEqual(left, -1)
                self.assertAlmostEqual(right, -1)
                self.assertNotAlmostEqual(right, 1)

    def test_corrected_second_numerator(self):
        alpha,beta,_,_ = parameters(Triangle(15,105),-.5)
        corrected = math.tan(3*(alpha-beta)/2)/math.tan((alpha-beta)/2)
        visible_unparenthesized = math.tan((3*alpha-beta)/2)/math.tan((alpha-beta)/2)
        self.assertAlmostEqual(corrected,-1)
        self.assertNotAlmostEqual(visible_unparenthesized,-1)

    def test_isosceles_tangent_undefined(self):
        with self.assertRaises(DomainError): tangent_ratios(Triangle(50,50),2)
        self.assertAlmostEqual(sine_residual(Triangle(50,50),2),0)

    def test_tangent_pole(self):
        with self.assertRaises(DomainError): tangent_ratios(Triangle(30,60),1)


class BisectorTests(unittest.TestCase):
    def test_invalid_sides(self):
        for sides in [(1,2,3),(1,2,4),(0,1,1),(-1,1,1),(math.inf,2,2)]:
            with self.subTest(sides=sides), self.assertRaises(DomainError): bisector_squares(*sides)

    def test_unrepresentable_squares_raise_domain_error(self):
        for scale in [1e200,1e-200]:
            with self.subTest(scale=scale):
                with self.assertRaises(DomainError):bisector_squares(3*scale,4*scale,5*scale)
                with self.assertRaises(DomainError):factored_bisector_difference(3*scale,4*scale,5*scale)

    def test_factor_identity_exact_integer_grid(self):
        count = 0
        for aa in range(1,21):
            for bb in range(1,21):
                for cc in range(1,21):
                    if min(aa+bb-cc,aa+cc-bb,bb+cc-aa)<=0: continue
                    a,b,c = map(Fraction,(aa,bb,cc))
                    left=b*c*(1-a*a/(b+c)**2)-a*c*(1-b*b/(a+c)**2)
                    right=(b-a)*c*(a+b+c)*factor_polynomial(a,b,c)/((a+c)**2*(b+c)**2)
                    self.assertEqual(left,right)
                    self.assertGreater(factor_polynomial(a,b,c),0)
                    count+=1
        self.assertEqual(count,4010)

    def test_factor_and_sign(self):
        for sides in [(3,4,5),(4,3,5),(4,4,5),(2.2,3.1,4.0)]:
            a,b,c=sides
            x,y=bisector_squares(a,b,c)
            self.assertAlmostEqual(x-y,factored_bisector_difference(a,b,c))
            self.assertEqual((x>y)-(x<y),(b>a)-(b<a))

    def test_n2_sine_geometry_matches_side_formula(self):
        t=Triangle(50,70,2)
        a=t.base*math.sin(t.A)/math.sin(t.A+t.B)
        b=t.base*math.sin(t.B)/math.sin(t.A+t.B)
        x,y=bisector_squares(a,b,t.base)
        g=divider_geometry(t,2)
        self.assertAlmostEqual(x,g.t_A**2)
        self.assertAlmostEqual(y,g.t_B**2)


class ChordTests(unittest.TestCase):
    def test_positive_root_and_negative_other_root(self):
        for a,b in [(1,1),(2,3),(.1,5),(1e12,1)]:
            x=near_segment(a,b)
            self.assertGreater(x,0)
            self.assertLess(x,b)
            self.assertTrue(math.isclose(x*x+a*x,b*b,rel_tol=1e-12))
            self.assertLess(-a-x,0)

    def test_extreme_but_representable_roots(self):
        for a in [1e200,1e308]:
            self.assertTrue(math.isclose(near_segment(a,1),1/a,rel_tol=1e-12,abs_tol=0))
        with self.assertRaises(DomainError):near_segment(1e308,1e-308)

    def test_invalid_root_inputs(self):
        for a,b in [(0,1),(-1,1),(1,0),(1,-1),(math.nan,1)]:
            with self.subTest(a=a,b=b), self.assertRaises(DomainError): near_segment(a,b)

    def test_circle_incidence_and_chord_identity(self):
        for theta in [-59,-30,0,30,59]:
            g=circle_chord(theta)
            self.assertAlmostEqual(g['Q'][0]**2+g['Q'][1]**2,1)
            self.assertAlmostEqual(g['S'][1],.5)
            self.assertAlmostEqual(g['near']*(g['near']+g['remote']),1)
            self.assertAlmostEqual(near_segment(g['remote'],1),g['near'])

    def test_equal_remote_and_equal_near(self):
        left,right=circle_chord(-30),circle_chord(30)
        self.assertAlmostEqual(left['remote'],right['remote'])
        self.assertAlmostEqual(left['near'],right['near'])

    def test_converse_is_b_squared_not_zero(self):
        a,b=.6,1.0
        x=remote_segment(a,b)
        self.assertAlmostEqual(a*(a+x),b*b)
        self.assertGreater(a*(a+x),0)
        self.assertAlmostEqual(near_segment(x,b),a)

    def test_extreme_representable_converse(self):
        a,b=1e-320,1e-10
        x=remote_segment(a,b)
        self.assertTrue(math.isfinite(x))
        self.assertTrue(math.isclose(a*x,b*b,rel_tol=1e-12))

    def test_converse_domain(self):
        for a,b in [(0,1),(1,1),(2,1),(-1,1)]:
            with self.subTest(a=a,b=b), self.assertRaises(DomainError): remote_segment(a,b)

    def test_fixed_circle_admissibility(self):
        for theta in [-60,60,90,math.inf]:
            with self.subTest(theta=theta), self.assertRaises(DomainError): circle_chord(theta)

    def test_positive_monotonic_factor_exact(self):
        a,x,y=Fraction(3,2),Fraction(1,3),Fraction(4,5)
        self.assertEqual((x*x+a*x)-(y*y+a*y),(x-y)*(x+y+a))
        self.assertGreater(x+y+a,0)


class RootFinderTests(unittest.TestCase):
    def test_rejects_nan_inside_bracket(self):
        def f(x):
            if x==0:return -1
            if x==2:return 1
            return math.nan
        with self.assertRaises(DomainError):bisect_root(f,0,2)

    def test_bracket(self):
        self.assertAlmostEqual(bisect_root(lambda x:x*x-2,0,2),math.sqrt(2))
        self.assertEqual(bisect_root(lambda x:x,0,2),0)
        with self.assertRaises(DomainError):bisect_root(lambda x:x*x+1,0,2)

class PolynomialCertificateTests(unittest.TestCase):
    def test_all_coefficients_vanish(self):
        from polynomial_certificate import certificate
        c = certificate()
        self.assertTrue(c['identity_verified'])
        self.assertEqual(c['residual_nonzero_terms'], 0)
        self.assertGreater(c['left_nonzero_terms'], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
