import unittest
from dataclasses import replace
from fractions import Fraction as F
from geometry import *
from cases import positive_cases,rejected_cases

class ExactArithmetic(unittest.TestCase):
    def test_square_reduction(self):self.assertEqual(Q(1,2,F(9,4)),4)
    def test_zero_radicand(self):self.assertEqual(Q(5,99,0),5)
    def test_nonsquare_multiply(self):self.assertEqual(Q(1,1,2)*Q(1,-1,2),-1)
    def test_division(self):self.assertEqual(Q(1,1,2)/Q(1,-1,2),Q(-3,-2,2))
    def test_sign_cancellation(self):self.assertEqual((Q(1,-1,2).sign(),Q(-1,1,2).sign()),(-1,1))
    def test_sign_large_rational(self):self.assertEqual((Q(3,-1,2).sign(),Q(-3,1,2).sign()),(1,-1))
    def test_sign_zero(self):self.assertEqual(Q().sign(),0)
    def test_mixed_field_reject(self):
        with self.assertRaises(ValueError):Q(0,1,2)+Q(0,1,3)
    def test_float_reject(self):
        with self.assertRaises(TypeError):point(0.1,0)
    def test_negative_radicand_reject(self):
        with self.assertRaises(ValueError):Q(0,1,-2)
    def test_zero_division(self):
        with self.assertRaises(ZeroDivisionError):Q(1)/Q(0)

class Construction(unittest.TestCase):
    def setUp(self):
        self.a,self.b,self.c,self.d=point(0,0),point(1,0),point(2,3),point(4,-1)
        self.k=construct(self.a,self.b,self.c,self.d)
    def test_rational_foot(self):self.assertEqual(self.k.h,point(2,0))
    def test_irrational_intersections(self):self.assertEqual(self.k.e,point(Q(2,1,11),0))
    def test_facts(self):self.assertTrue(accepted(self.a,self.b,self.c,self.d,self.k))
    def test_endpoint_swap(self):
        k=construct(self.b,self.a,self.c,self.d)
        self.assertEqual(k.e,self.k.g);self.assertEqual(k.g,self.k.e);self.assertEqual(k.h,self.k.h)
    def test_chord_label_swap(self):self.assertTrue(accepted(self.a,self.b,self.c,self.d,replace(self.k,e=self.k.g,g=self.k.e)))
    def test_d_change_same_foot(self):self.assertEqual(construct(self.a,self.b,self.c,point(-7,-4)).h,self.k.h)
    def test_outside_original_segment(self):self.assertEqual(foot_parameter(self.a,self.b,self.k.h),2)
    def test_zero_line(self):
        with self.assertRaises(ValueError):construct(self.a,self.a,self.c,self.d)
    def test_on_line_c(self):
        with self.assertRaises(ValueError):construct(self.a,self.b,point(7,0),self.d)
    def test_on_line_d(self):
        with self.assertRaises(ValueError):construct(self.a,self.b,self.c,point(7,0))
    def test_same_side_d(self):
        with self.assertRaises(ValueError):construct(self.a,self.b,self.c,point(7,1))
    def test_finite_positive_family(self):
        rows=list(positive_cases());self.assertEqual(len(rows),648)
        for row in rows:self.assertTrue(accepted(*row))
    def test_finite_negative_family(self):
        rows=list(rejected_cases());self.assertEqual(len(rows),16)
        for name,*row in rows:
            with self.subTest(name=name):self.assertFalse(accepted(*row))
    def test_conclusion_is_not_certificate(self):
        bad=replace(self.k,e=point(3,0),g=point(1,0))
        facts=check_certificate(self.a,self.b,self.c,self.d,bad)
        self.assertTrue(facts['perpendicular_modern_check']);self.assertFalse(facts['E_on_prescribed_circle'])
    def test_tangent_model_not_accepted(self):
        bad=Certificate(self.c,Q(9),point(2,0),point(2,0),point(2,0))
        self.assertFalse(accepted(self.a,self.b,self.c,self.d,bad))
    def test_rational_square_root_case(self):
        k=construct(point(0,0),point(1,0),point(0,3),point(0,-2))
        self.assertEqual(k.e,point(4,0));self.assertEqual(k.g,point(-4,0))
    def test_vertical_line(self):
        a,b,c,d=point(1,0),point(1,5),point(4,7),point(-1,2)
        self.assertEqual(construct(a,b,c,d).h,point(1,7))

if __name__=='__main__':unittest.main(verbosity=2)
