import unittest
from dataclasses import replace
from fractions import Fraction as R
from geometry import *
from cases import positive_cases,rejected_cases,example_report

class GeometryTests(unittest.TestCase):
    def setUp(self):
        self.a,self.b,self.c=point(0,0),point(6,0),point(3,0)
        self.h=R(1,6)
    def test_grid(self):
        self.assertEqual(sum(accepted(a,b,c,h,k) for a,b,c,h,k in positive_cases()),864)
    def test_negatives(self):
        for name,a,b,c,h,k in rejected_cases():
            with self.subTest(name=name):self.assertFalse(accepted(a,b,c,h,k))
    def test_interior_exact(self):
        k=construct(self.a,self.b,self.c,self.h)
        self.assertEqual(k.d,point(2,0));self.assertEqual(k.e,point(4,0))
        self.assertEqual(k.f,point(3,SQRT3))
    def test_endpoint_extension(self):
        k=construct(self.a,self.b,self.a,self.h)
        self.assertTrue(accepted(self.a,self.b,self.a,self.h,k))
        self.assertTrue(extension_report(self.a,self.b,k)['D_outside_segment'])
    def test_other_endpoint_extension(self):
        k=construct(self.a,self.b,self.b,self.h)
        self.assertTrue(extension_report(self.a,self.b,k)['E_outside_segment'])
    def test_large_cut_extensions(self):
        k=construct(self.a,self.b,self.c,R(2));r=extension_report(self.a,self.b,k)
        self.assertTrue(r['D_outside_segment'] and r['E_outside_segment'])
    def test_opposite_rays_same_line(self):
        p=construct(self.a,self.b,self.c,self.h,1);m=construct(self.a,self.b,self.c,self.h,-1)
        u,v=sub(p.f,self.c),sub(m.f,self.c)
        self.assertEqual(cross(u,v),ZERO);self.assertLess(dot(u,v).sign(),0)
    def test_cut_scale_same_line(self):
        p=construct(self.a,self.b,self.c,R(1,7));q=construct(self.a,self.b,self.c,R(5,3))
        self.assertEqual(cross(sub(p.f,self.c),sub(q.f,self.c)),ZERO)
        self.assertGreater(dot(sub(p.f,self.c),sub(q.f,self.c)).sign(),0)
    def test_reverse_line(self):
        p=construct(self.a,self.b,self.c,self.h);q=construct(self.b,self.a,self.c,self.h,-1)
        self.assertEqual(p.f,q.f);self.assertEqual(p.d,q.e)
    def test_oblique(self):
        a,b,c=point(-2,1),point(4,9),point(1,5);k=construct(a,b,c,R(1,2))
        self.assertEqual(k.f,point(Q3(1,-4),Q3(5,3)))
        self.assertTrue(accepted(a,b,c,R(1,2),k))
    def test_degenerate_line(self):
        with self.assertRaises(ValueError):construct(self.a,self.a,self.a)
    def test_off_line(self):
        with self.assertRaises(ValueError):construct(self.a,self.b,point(3,1))
    def test_outside_C(self):
        with self.assertRaises(ValueError):construct(self.a,self.b,point(7,0))
    def test_nonpositive_h(self):
        for h in [0,-1,R(-1,2)]:
            with self.assertRaises(ValueError):construct(self.a,self.b,self.c,h)
    def test_invalid_h_types(self):
        for h in [True,0.5,'1/2',Q3(1)]:
            with self.assertRaises(ValueError):construct(self.a,self.b,self.c,h)
    def test_invalid_coordinate_types(self):
        for x in [True,0.5,'1']:
            with self.assertRaises(TypeError):point(x,0)
    def test_irrational_input(self):
        with self.assertRaises(ValueError):construct(point(SQRT3,0),self.b,self.c)
    def test_invalid_branches(self):
        for s in [True,0,2,1.0,'1']:
            with self.assertRaises(ValueError):construct(self.a,self.b,self.c,self.h,s)
    def test_invalid_certificate(self):
        for k in [None,{},[],Certificate(1,(0,0),self.a,self.b)]:
            self.assertFalse(accepted(self.a,self.b,self.c,self.h,k))
    def test_tiny_large_exact(self):
        for scale_value in [R(1,10**200),R(10**200)]:
            a=point(0,0);b=point(scale_value,scale_value);c=a
            self.assertTrue(accepted(a,b,c,R(1,3),construct(a,b,c,R(1,3))))
    def test_large_translation_small_gap(self):
        a=point(10**150,10**150);b=add(a,point(R(1,10**150),0));c=a
        self.assertTrue(accepted(a,b,c,R(1,3),construct(a,b,c,R(1,3))))
    def test_unequal_cuts_equilateral_not_perpendicular(self):
        a,b,c=point(0,0),point(6,0),point(2,0);d,e=point(1,0),point(4,0)
        k=Certificate(1,d,e,equilateral_vertices(d,e)[0]);facts=check_certificate(a,b,c,R(1,6),k)
        self.assertTrue(facts['equilateral_DFE']);self.assertFalse(facts['CD_equals_CE'])
        self.assertFalse(facts['perpendicular_modern_check'])
    def test_equal_distance_not_adjacent(self):
        k=construct(self.a,self.b,self.c,self.h);k=replace(k,e=k.d)
        f=check_certificate(self.a,self.b,self.c,self.h,k)
        self.assertTrue(f['CD_equals_CE']);self.assertFalse(f['opposite_nonzero_rays'])
    def test_perpendicular_not_full_construction(self):
        k=replace(construct(self.a,self.b,self.c,self.h),f=point(3,1))
        f=check_certificate(self.a,self.b,self.c,self.h,k)
        self.assertTrue(f['perpendicular_modern_check']);self.assertFalse(f['equilateral_DFE'])
    def test_q3_field(self):
        z=Q3(R(2,3),R(5,7));self.assertEqual(z/z,ONE)
        self.assertEqual(SQRT3*SQRT3,Q3(3))
        with self.assertRaises(ZeroDivisionError):ONE/ZERO
    def test_q3_sign_near_cancellation(self):
        a,b=2,1
        for _ in range(160):
            self.assertEqual(Q3(a,-b).sign(),1)
            self.assertEqual(Q3(-a,b).sign(),-1)
            a,b=2*a+3*b,a+2*b
    def test_parameter(self):
        self.assertEqual(parameter(self.a,self.b,self.c),Q3(R(1,2)))
        with self.assertRaises(ValueError):parameter(self.a,self.b,point(0,1))
    def test_examples(self):
        self.assertEqual(set(example_report()),{'interior','endpoint','oblique'})

if __name__=='__main__':unittest.main(verbosity=2)
