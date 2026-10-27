import copy
import unittest
from fractions import Fraction as Q
from geometry import *
from cases import positive_cases,NEGATIVE

class GeometryTests(unittest.TestCase):
    def test_345(self):self.assertEqual(construct(3,4,5)['K']['x'],'9/5')
    def test_height(self):self.assertEqual(construct(3,4,5)['height_squared'],'144/25')
    def test_equilateral(self):self.assertEqual(construct(1,1,1)['height_squared'],'3/4')
    def test_mirrors(self):
        p,m=construct(2,3,4,1),construct(2,3,4,-1)
        self.assertEqual(p['height_squared'],m['height_squared'])
        self.assertEqual(p['K']['y']['coefficient'],'1');self.assertEqual(m['K']['y']['coefficient'],'-1')
    def test_external_tangent(self):self.assertEqual(classify(1,1,2),'external_tangent_degenerate')
    def test_internal_tangent(self):self.assertEqual(classify(3,1,2),'internal_tangent_degenerate')
    def test_separate(self):self.assertEqual(classify(1,1,3),'separate')
    def test_contained(self):self.assertEqual(classify(3,1,1),'contained')
    def test_intersect(self):self.assertEqual(classify(2,3,4),'two_intersections')
    def test_negative_inputs(self):
        for values in NEGATIVE:
            with self.subTest(values=values):
                with self.assertRaises((ValueError,ZeroDivisionError,TypeError)):construct(*values)
    def test_orientation(self):
        for sign in (True,False,0,2,1.0,'1'):
            with self.assertRaises(ValueError):construct(1,1,1,sign)
    def test_all_cases(self):
        for values in positive_cases():
            for sign in (-1,1):self.assertTrue(verify(construct(*values,sign),*values,sign))
    def test_near_degenerate(self):self.assertGreater(Q(construct(1,1,Q(1999999,1000000))['height_squared']),0)
    def test_outside_projection(self):self.assertLess(Q(construct(2,4,3)['K']['x']),0)
    def test_fraction_strings(self):self.assertEqual(construct('1/3','1/3','1/3')['height_squared'],'1/12')
    def test_scale(self):self.assertEqual(Q(construct(6,8,10)['height_squared']),4*Q(construct(3,4,5)['height_squared']))
    def test_factorization(self):
        for v in positive_cases():
            c=construct(*v);self.assertEqual(c['height_squared'],c['factorized_height_squared'])
    def test_input_binding(self):self.assertFalse(verify(construct(3,4,5),4,3,5))
    def test_sign_binding(self):self.assertFalse(verify(construct(3,4,5),3,4,5,-1))
    def test_missing_key(self):
        c=construct(3,4,5);del c['noncollinear'];self.assertFalse(verify(c,3,4,5))
    def test_extra_key(self):
        c=construct(3,4,5);c['extra']=0;self.assertFalse(verify(c,3,4,5))
    def test_bool_int(self):
        c=construct(3,4,5);c['schema_version']=True;self.assertFalse(verify(c,3,4,5))
    def test_int_bool(self):
        c=construct(3,4,5);c['strict_triangle']=1;self.assertFalse(verify(c,3,4,5))
    def test_float(self):
        c=construct(3,4,5);c['orientation']=1.0;self.assertFalse(verify(c,3,4,5))
    def test_nan(self):
        c=construct(3,4,5);c['orientation']=float('nan');self.assertFalse(verify(c,3,4,5))
    def test_tuple(self):
        c=construct(3,4,5);c['F']=('0','0');self.assertFalse(verify(c,3,4,5))
    def test_tamper_distance(self):
        c=construct(3,4,5);c['squared_distances']['FK']='10';self.assertFalse(verify(c,3,4,5))
    def test_tamper_coordinate(self):
        c=construct(3,4,5);c['K']['x']='2';self.assertFalse(verify(c,3,4,5))
    def test_tamper_radicand(self):
        c=construct(3,4,5);c['K']['y']['radicand']='1';self.assertFalse(verify(c,3,4,5))
    def test_quad_square(self):self.assertEqual((Quad(0,1,2)*Quad(0,1,2)).rational_value(),2)
    def test_quad_product(self):self.assertEqual(Quad(1,1,2)*Quad(1,-1,2),Quad(-1,0,2))
    def test_quad_fields(self):
        with self.assertRaises(ValueError):Quad(0,1,2)+Quad(0,1,3)
    def test_quad_nonrational(self):
        with self.assertRaises(ValueError):Quad(0,1,2).rational_value()
    def test_quad_invalid(self):
        with self.assertRaises(ValueError):Quad(0,1,0)
    def test_json_roundtrip(self):self.assertTrue(verify(json.loads(json.dumps(construct(3,4,5))),3,4,5))
    def test_reordered_keys(self):
        c=construct(3,4,5);self.assertTrue(verify(dict(reversed(list(c.items()))),3,4,5))

if __name__=='__main__':unittest.main(verbosity=2)
