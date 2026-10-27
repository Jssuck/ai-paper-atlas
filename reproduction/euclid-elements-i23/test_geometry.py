import copy
import unittest
from fractions import Fraction as Q
from geometry import construct,verify,point,rat,dot,cross,sub,strict_json
from cases import positives,negatives,run
BASE=((0,0),(2,0),(1,2),(0,0),(1,0),1)
class Tests(unittest.TestCase):
    def test_all_positive(self):
        for a in positives():self.assertTrue(verify(construct(*a),*a))
    def test_negative_inputs(self):
        for a in negatives():
            with self.assertRaises(ValueError):construct(*a)
    def test_expected_counts(self):self.assertEqual(run()['positive_certificates'],144)
    def test_acute(self):self.assertEqual(construct(*BASE)['checks']['AF_dot_AG'],'2')
    def test_obtuse(self):self.assertLess(Q(construct((0,0),(1,0),(-2,1),(0,0),(1,0))['checks']['AF_dot_AG']),0)
    def test_right(self):self.assertEqual(construct((0,0),(1,0),(0,3),(0,0),(1,1))['checks']['AF_dot_AG'],'0')
    def test_mirror(self):
        a=construct(*BASE);b=construct(*BASE[:-1],-1)
        self.assertEqual(a['checks']['AF2'],b['checks']['AF2']);self.assertEqual(Q(a['checks']['AG_cross_AF']),-Q(b['checks']['AG_cross_AF']))
    def test_signed_source_negative(self):self.assertTrue(construct((0,0),(1,0),(1,1),(0,0),(0,1),-1)['signed_orientation_preserved'])
    def test_target_reversed(self):self.assertTrue(verify(construct(*BASE[:4],(-1,0),1),*BASE[:4],(-1,0),1))
    def test_fraction_input(self):self.assertTrue(verify(construct((0,0),('1/2',0),(1,'2/3'),(0,0),(1,0)),(0,0),('1/2',0),(1,'2/3'),(0,0),(1,0)))
    def test_source_translation(self):
        c=construct((5,6),(7,6),(6,8),*BASE[3:]);self.assertEqual(c['checks'],construct(*BASE)['checks'])
    def test_target_translation(self):
        c=construct(*BASE[:3],(5,6),(6,6));self.assertEqual(c['checks'],construct(*BASE)['checks'])
    def test_target_rescale(self):
        c=construct(*BASE[:4],(7,0));self.assertEqual(c['checks'],construct(*BASE)['checks'])
    def test_nonrational_scale(self):self.assertEqual(construct(*BASE[:4],(1,1))['radicand'],'5/2')
    def test_near_flat(self):self.assertTrue(construct((0,0),(1,0),(1,'1/1000000000000'),(0,0),(1,1))['ordinary_angle_preserved'])
    def test_huge(self):self.assertTrue(construct((0,0),(10**50,0),(1,10**50),(0,0),(1,2))['ordinary_angle_preserved'])
    def test_input_binding(self):self.assertFalse(verify(construct(*BASE),(0,0),(2,0),(1,3),*BASE[3:]))
    def test_side_binding(self):self.assertFalse(verify(construct(*BASE),*BASE[:-1],-1))
    def test_schema_bool(self):
        c=construct(*BASE);c['schema_version']=True;self.assertFalse(verify(c,*BASE))
    def test_side_bool(self):
        c=construct(*BASE);c['side']=True;self.assertFalse(verify(c,*BASE))
    def test_truth_integer(self):
        c=construct(*BASE);c['ordinary_angle_preserved']=1;self.assertFalse(verify(c,*BASE))
    def test_fraction_float(self):
        c=construct(*BASE);c['radicand']=4.0;self.assertFalse(verify(c,*BASE))
    def test_tuple_not_json(self):
        c=construct(*BASE);c['F']['constant']=(0,0);self.assertFalse(verify(c,*BASE))
    def test_nan(self):
        c=construct(*BASE);c['side']=float('nan');self.assertFalse(verify(c,*BASE))
    def test_extra_key(self):
        c=construct(*BASE);c['extra']=None;self.assertFalse(verify(c,*BASE))
    def test_missing_key(self):
        c=construct(*BASE);del c['checks'];self.assertFalse(verify(c,*BASE))
    def test_coordinate_tamper(self):
        c=construct(*BASE);c['G']['sqrt_coefficient'][1]='999';self.assertFalse(verify(c,*BASE))
    def test_length_tamper(self):
        c=construct(*BASE);c['checks']['AG2']='1';self.assertFalse(verify(c,*BASE))
    def test_radicand_tamper(self):
        c=construct(*BASE);c['radicand']='-1';self.assertFalse(verify(c,*BASE))
    def test_order_independent_json(self):
        c=construct(*BASE);self.assertTrue(verify(dict(reversed(list(c.items()))),*BASE))
    def test_deterministic(self):self.assertEqual(construct(*BASE),construct(*BASE))
    def test_zero_angle_invalid(self):self.assertFalse(verify({},(0,0),(1,0),(2,0),(0,0),(1,0)))
if __name__=='__main__':unittest.main(verbosity=2)
