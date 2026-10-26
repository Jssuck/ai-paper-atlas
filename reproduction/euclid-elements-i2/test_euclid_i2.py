import unittest
from fractions import Fraction as F
from euclid_i2 import *

class ArithmeticTests(unittest.TestCase):
    def test_product(self):self.assertEqual(Q3(1,1)*Q3(1,-1),Q3(-2))
    def test_sign(self):
        for a,b,e in [(2,-1,1),(1,-1,-1),(-2,1,-1),(-1,1,1),(0,0,0)]:
            self.assertEqual(Q3(a,b).sign(),e)
    def test_exact_fraction(self):self.assertEqual(Q3(F(1,3)).scale(3),Q3(1))
    def test_reject_inexact(self):
        for v in (1.0,True,'1'):
            with self.assertRaises(TypeError):construct(v,1)
    def test_reject_r(self):
        for v in (0,-1):
            with self.assertRaises(ValueError):construct(1,v)
    def test_reject_s(self):
        for v in (0,-1):
            with self.assertRaises(ValueError):construct(v,1)
    def test_reject_side(self):
        for v in (True,0,2,1.0):
            with self.assertRaises(ValueError):construct(1,1,v)
    def test_reject_offset(self):
        with self.assertRaises(TypeError):construct(1,1,offset=(0.1,0))

class GeometryTests(unittest.TestCase):
    def test_hand_example(self):
        p=construct(2,1)
        self.assertEqual(p['A'],point((2,0)))
        self.assertEqual(p['G'],(Q3(F(3,2)),Q3(0,F(3,2))))
        self.assertEqual(p['L'],point((3,0)))
        self.assertTrue(certificate(p)['accepted'])
    def test_reflection(self):
        for side in (-1,1):self.assertTrue(certificate(construct(1,2,side))['accepted'])
    def test_translation(self):
        self.assertTrue(certificate(construct(F(1,7),F(17,3),offset=(F(-9,5),F(8,3))))['accepted'])
    def test_radius_smaller(self):self.assertTrue(certificate(construct(100,1))['accepted'])
    def test_radius_larger(self):self.assertTrue(certificate(construct(1,100))['accepted'])
    def test_radius_equal(self):self.assertTrue(certificate(construct(1,1))['accepted'])
    def test_wrong_near_G(self):
        p=construct(2,1);p['G']=scale(p['B'],F(1,2)); c=certificate(p)
        self.assertTrue(c['circle_B_through_C']);self.assertFalse(c['D_B_G_order']);self.assertFalse(c['accepted'])
    def test_wrong_L_ray(self):
        p=construct(2,1);p['L']=point((-3,0));c=certificate(p)
        self.assertTrue(c['circle_D_through_G']);self.assertFalse(c['D_A_L_order']);self.assertFalse(c['accepted'])
    def test_wrong_G_circle(self):
        p=construct(2,1);p['G']=scale(p['B'],2);c=certificate(p)
        self.assertTrue(c['D_B_G_order']);self.assertFalse(c['circle_B_through_C']);self.assertFalse(c['accepted'])
    def test_wrong_frame(self):
        p=construct(2,1);p['D']=point((-1,0));self.assertFalse(certificate(p)['equilateral_frame'])
    def test_zero_input(self):
        p=construct(2,1);p['C']=p['B'];self.assertFalse(certificate(p)['nonzero_input'])
    def test_malformed_certificate(self):
        p=construct(2,1);p['L']=(3,0)
        with self.assertRaises(TypeError):certificate(p)
    def test_direct_case(self):
        a=point((1,2));c=point((4,6));self.assertEqual(coincident_anchor(a,a,c),c)
    def test_direct_case_wrong_anchor(self):
        with self.assertRaises(ValueError):coincident_anchor(point((0,0)),point((1,0)),point((2,0)))
    def test_direct_case_zero(self):
        a=point((0,0))
        with self.assertRaises(ValueError):coincident_anchor(a,a,a)
    def test_beyond(self):
        d,a=point((0,0)),point((2,0))
        self.assertTrue(beyond(d,a,point((3,0))))
        for p in ((1,0),(2,0),(-1,0),(3,1)):
            self.assertFalse(beyond(d,a,point(p)))
    def test_enumeration(self):
        e=run()['enumeration'];self.assertEqual(e,{'cases':150,'violations':0})

if __name__=='__main__':unittest.main()
