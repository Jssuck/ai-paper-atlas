"""Assertions use unittest methods and remain effective under -O and -OO."""
import copy
import unittest
from geometry import *
from quadratic import asq
from cases import positives,negatives

class GeometryTests(unittest.TestCase):
    def setUp(self):
        self.args=(point(0,0),point(1,1),point(4,0))
        self.k=construct(*self.args)
    def test_01_positive(self):self.assertTrue(accepted(*self.args,self.k))
    def test_02_all_cases(self):
        for args in positives():self.assertTrue(accepted(*args,construct(*args)))
    def test_03_negative(self):
        for args in negatives():
            with self.assertRaises((ValueError,TypeError)):construct(*args)
    def test_04_irrational(self):self.assertNotEqual(self.k['t']['b'],'0')
    def test_05_rational(self):self.assertEqual(construct(point(0,0),point(3,4),point(10,0))['t']['a'],'1/2')
    def test_06_input_binding(self):self.assertFalse(accepted(point(1,0),*self.args[1:],self.k))
    def test_07_t_tamper(self):
        k=copy.deepcopy(self.k);k['t']['b']='2';self.assertFalse(accepted(*self.args,k))
    def test_08_d_tamper(self):
        k=copy.deepcopy(self.k);k['D'][0]['a']='99';self.assertFalse(accepted(*self.args,k))
    def test_09_check_tamper(self):
        k=copy.deepcopy(self.k);k['checks']['AD_equals_AB']=False;self.assertFalse(accepted(*self.args,k))
    def test_10_bool_to_int(self):
        k=copy.deepcopy(self.k);k['checks']['AD_equals_AB']=1;self.assertFalse(accepted(*self.args,k))
    def test_11_tuple(self):
        k=copy.deepcopy(self.k);k['D']=tuple(k['D']);self.assertFalse(accepted(*self.args,k))
    def test_12_nan(self):
        k=copy.deepcopy(self.k);k['extra']=float('nan');self.assertFalse(accepted(*self.args,k))
    def test_13_extra(self):
        k=copy.deepcopy(self.k);k['extra']=0;self.assertFalse(accepted(*self.args,k))
    def test_14_missing(self):
        k=copy.deepcopy(self.k);del k['D'];self.assertFalse(accepted(*self.args,k))
    def test_15_bool_input(self):
        with self.assertRaises(TypeError):point(True,0)
    def test_16_float_input(self):
        with self.assertRaises(TypeError):point(1.0,0)
    def test_17_quadratic_input(self):
        with self.assertRaises(TypeError):construct((Q(0,1,2),Q(0)),*self.args[1:])
    def test_18_q_square(self):self.assertEqual(Q(0,1,2)*Q(0,1,2),2)
    def test_19_q_div(self):self.assertEqual(Q(1,1,2)/Q(1,1,2),1)
    def test_20_q_sign_positive(self):self.assertEqual(Q(-1,1,2).sign(),1)
    def test_21_q_sign_negative(self):self.assertEqual(Q(1,-1,2).sign(),-1)
    def test_22_q_sign_large(self):self.assertEqual(Q(2,-1,2).sign(),1)
    def test_23_q_rational_reduce(self):self.assertEqual(Q(0,1,F(9,4)),F(3,2))
    def test_24_mixed_radicals(self):
        with self.assertRaises(ValueError):Q(0,1,2)+Q(0,1,3)
    def test_25_zero_div(self):
        with self.assertRaises(ZeroDivisionError):Q(1)/Q(0)
    def test_26_zero_angle(self):self.assertEqual(angle_cmp(point(1,0),point(1,0),point(1,0),point(0,1)),-1)
    def test_27_straight_angle(self):self.assertEqual(angle_cmp(point(1,0),point(-1,0),point(1,0),point(0,1)),1)
    def test_28_acute(self):self.assertEqual(angle_cmp(point(1,0),point(2,1),point(1,0),point(1,1)),-1)
    def test_29_obtuse(self):self.assertEqual(angle_cmp(point(1,0),point(-2,1),point(1,0),point(-1,1)),1)
    def test_30_equal_angle(self):self.assertEqual(angle_cmp(point(1,0),point(1,1),point(2,0),point(3,3)),0)
    def test_31_zero_ray(self):
        with self.assertRaises(ValueError):angle_cmp(point(0,0),point(1,1),point(1,0),point(0,1))
    def test_32_negative_radicand(self):
        with self.assertRaises(ValueError):Q(0,1,-1)

if __name__=='__main__':unittest.main(verbosity=2)
