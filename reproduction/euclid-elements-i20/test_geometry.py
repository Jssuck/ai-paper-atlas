import unittest
from copy import deepcopy
from itertools import permutations
from geometry import *
from cases import positive_cases,invalid_cases

class TestGeometry(unittest.TestCase):
    def setUp(self):
        self.tri=(point(0,0),point(3,0),point(0,4));self.cert=construct(*self.tri)
    def test_all_positive(self):
        for case in positive_cases():self.assertTrue(accepted(*case,construct(*case)))
    def test_all_negative(self):
        for case in invalid_cases():
            with self.assertRaises(ValueError):construct(*case)
    def test_sample_D(self):self.assertEqual(self.cert['D'],pjson(point(-4,0)))
    def test_sample_ratio(self):self.assertEqual(self.cert['t'],qjson(Q(F(4,3))))
    def test_permutations(self):
        for p in permutations(self.tri):self.assertTrue(accepted(*p,construct(*p)))
    def test_nonrational(self):self.assertNotEqual(construct(point(0,0),point(1,0),point(1,1))['t']['b'],'0')
    def test_rational_inputs(self):self.assertTrue(accepted(*(t:= (point(F(1,3),0),point(2,F(1,7)),point(-1,2))),construct(*t)))
    def test_reflection(self):self.assertTrue(accepted(*(t:=tuple(point(p[0].a,-p[1].a) for p in self.tri)),construct(*t)))
    def test_rotation(self):self.assertTrue(accepted(*(t:=tuple(point(-p[1].a,p[0].a) for p in self.tri)),construct(*t)))
    def test_translation(self):self.assertTrue(accepted(*(t:=tuple(add(p,point(10,-7)) for p in self.tri)),construct(*t)))
    def test_positive_scale(self):self.assertTrue(accepted(*(t:=tuple(scale(F(1,11),p) for p in self.tri)),construct(*t)))
    def test_negative_scale(self):self.assertTrue(accepted(*(t:=tuple(scale(-3,p) for p in self.tri)),construct(*t)))
    def test_large(self):self.assertTrue(accepted(*(t:=(point(0,0),point(10**30,1),point(1,10**30))),construct(*t)))
    def test_near_collinear(self):self.assertTrue(accepted(*(t:=(point(0,0),point(1,0),point(2,F(1,10**30)))),construct(*t)))
    def test_input_binding(self):self.assertFalse(accepted(point(0,0),point(3,0),point(0,5),self.cert))
    def test_bad_coordinate(self):
        with self.assertRaises(TypeError):point(True,0)
    def test_float_coordinate(self):
        with self.assertRaises(TypeError):point(1.0,0)
    def test_irrational_input(self):
        with self.assertRaises(TypeError):construct(point(Q(0,1,2),0),point(3,0),point(0,4))
    def test_wrong_shape(self):
        with self.assertRaises(TypeError):construct((Q(0),),*self.tri[1:])
    def test_tampered_D(self):
        c=deepcopy(self.cert);c['D'][0]['a']='-5';self.assertFalse(accepted(*self.tri,c))
    def test_bool_integer(self):
        c=deepcopy(self.cert);c['checks']['t_positive']=1;self.assertFalse(accepted(*self.tri,c))
    def test_bool_float(self):
        c=deepcopy(self.cert);c['checks']['t_positive']=1.0;self.assertFalse(accepted(*self.tri,c))
    def test_tuple(self):
        c=deepcopy(self.cert);c['D']=tuple(c['D']);self.assertFalse(accepted(*self.tri,c))
    def test_extra_key(self):
        c=deepcopy(self.cert);c['extra']=1;self.assertFalse(accepted(*self.tri,c))
    def test_missing_key(self):
        c=deepcopy(self.cert);del c['t'];self.assertFalse(accepted(*self.tri,c))
    def test_nan(self):
        c=deepcopy(self.cert);c['t']=float('nan');self.assertFalse(accepted(*self.tri,c))
    def test_none(self):self.assertFalse(accepted(*self.tri,None))
    def test_collinear_equality(self):self.assertFalse(sum_greater(1,4,9))
    def test_zero_equality(self):self.assertFalse(sum_greater(0,9,9))
    def test_other_degenerate_sums(self):self.assertTrue(sum_greater(1,9,4))
    def test_sum_types(self):
        for x in (True,1.0,"1"):
            with self.assertRaises(TypeError):sum_greater(x,1,1)
    def test_sum_domain(self):
        with self.assertRaises(ValueError):sum_greater(-1,1,1)
    def test_sum_exact_boundary(self):
        self.assertTrue(sum_greater(1,1,F(399,100)));self.assertFalse(sum_greater(1,1,F(401,100)))
    def test_quadratic_sign(self):
        self.assertEqual(Q(-3,2,2).sign(),-1);self.assertEqual(Q(-2,2,2).sign(),1)
    def test_angle_zero_ray(self):
        with self.assertRaises(ValueError):angle_cmp(point(0,0),point(1,0),point(1,0),point(0,1))
    def test_check_tampering(self):
        for key in self.cert['checks']:
            c=deepcopy(self.cert);c['checks'][key]=False;self.assertFalse(accepted(*self.tri,c))

if __name__=='__main__':unittest.main(verbosity=2)
