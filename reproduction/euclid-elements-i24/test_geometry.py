import copy
import json
import unittest
from fractions import Fraction as Q
from geometry import certify,verify,unit,norm2,strict_equal,load_json
from cases import case,positives,negatives

class GeometryTests(unittest.TestCase):
    def test_article_examples(self):
        for a,region,ef,eg in [(2,'outside',[16,5],[8,1]),(6,'collinear',[128,5],[40,1]),(8,'inside',[244,5],[68,1])]:
            c=certify(case(a=a,b=2,s=Q(1,2),t=1))
            self.assertEqual((c['configuration'],c['EF_squared'],c['EG_squared']),(region,ef,eg))
    def test_grid(self):
        for d in positives():
            with self.subTest(d=d):self.assertTrue(verify(d,certify(d)))
    def test_invalid(self):
        for d in negatives():
            with self.subTest(d=d):
                with self.assertRaises(ValueError):certify(d)
    def test_unit(self):
        for t in (Q(1,100),Q(1,3),Q(1),Q(100)):self.assertEqual(norm2(unit(t)),1)
    def test_monotone(self):self.assertGreater(unit(Q(1,3))[0],unit(Q(1))[0])
    def test_exact_example(self):
        c=certify(case());self.assertEqual(c['gap'],[8,5])
    def test_outside(self):self.assertEqual(certify(case(a=1))['configuration'],'outside')
    def test_collinear(self):self.assertEqual(certify(case(a=2))['configuration'],'collinear')
    def test_inside(self):self.assertEqual(certify(case(a=3))['configuration'],'inside')
    def test_reflection(self):
        for a in (1,2,3):
            x,y=certify(case(a=a)),certify(case(a=a,reflection=-1))
            self.assertEqual(x['configuration'],y['configuration']);self.assertEqual(x['gap'],y['gap'])
            self.assertEqual(x['EFG_orientation'],-y['EFG_orientation'])
    def test_scale(self):
        self.assertEqual(certify(case(a=7,b=7))['gap'],[392,5])
    def test_near_zero(self):self.assertTrue(verify(case(s=Q(1,10**12)),certify(case(s=Q(1,10**12)))))
    def test_near_pi(self):self.assertTrue(verify(case(t=10**12),certify(case(t=10**12))))
    def test_close_angles(self):self.assertTrue(verify(case(s=1,t=Q(10**12+1,10**12)),certify(case(s=1,t=Q(10**12+1,10**12)))))
    def test_wrong_input(self):self.assertFalse(verify(case(a=2),certify(case())))
    def test_changed_gap(self):
        c=certify(case());c['gap']=[1,1];self.assertFalse(verify(case(),c))
    def test_boolean_tamper(self):
        c=certify(case());c['EFG_orientation']=True;self.assertFalse(verify(case(),c))
    def test_nested_bool(self):
        c=certify(case());c['input']['a'][0]=True;self.assertFalse(verify(case(),c))
    def test_float_tamper(self):
        c=certify(case());c['EFG_orientation']=1.0;self.assertFalse(verify(case(),c))
    def test_extra_field(self):
        c=certify(case());c['extra']=0;self.assertFalse(verify(case(),c))
    def test_missing_field(self):
        c=certify(case());del c['gap'];self.assertFalse(verify(case(),c))
    def test_point_tamper(self):
        c=certify(case());c['points']['F'][0]=[0,1];self.assertFalse(verify(case(),c))
    def test_configuration_tamper(self):
        c=certify(case());c['configuration']='inside';self.assertFalse(verify(case(),c))
    def test_json_roundtrip(self):
        c=certify(case());self.assertTrue(verify(case(),load_json(json.dumps(c))))
    def test_duplicate_keys(self):
        with self.assertRaises(ValueError):load_json('{"a":1,"a":2}')
    def test_nan(self):
        with self.assertRaises(ValueError):load_json('{"a":NaN}')
    def test_inf(self):
        with self.assertRaises(ValueError):load_json('{"a":Infinity}')
    def test_not_dict(self):self.assertFalse(verify(case(),[]))
    def test_input_copy(self):
        d=case();c=certify(d);d['a'][0]=2;self.assertEqual(c['input']['a'],[1,1])
    def test_type_equality(self):self.assertFalse(strict_equal([1],[True]))
    def test_area_not_monotone(self):
        # Larger included angle: t=2 -> t=3; heights decrease 4/5 -> 3/5.
        self.assertGreater(unit(Q(2))[1],unit(Q(3))[1]);self.assertTrue(verify(case(s=2,t=3),certify(case(s=2,t=3))))
    def test_equal_angle_boundary(self):
        with self.assertRaises(ValueError):certify(case(s=1,t=1))
    def test_reversed_angle(self):
        with self.assertRaises(ValueError):certify(case(s=2,t=1))
if __name__=='__main__':unittest.main(verbosity=2)
