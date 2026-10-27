import copy
import unittest
from geometry import make_certificate, verify_certificate, rational, strict_equal
from cases import positives, negative_cases

class Checks(unittest.TestCase):
    def setUp(self):
        self.data=next(positives()); self.cert=make_certificate(self.data)
    def test_all_positive_families(self):
        for data in positives(): self.assertTrue(verify_certificate(data,make_certificate(data)))
    def test_all_negative_families(self):
        for data in negative_cases().values():
            with self.assertRaises(ValueError): make_certificate(data)
    def test_right_angle(self):
        d={'E':['0','0'],'F':['2','0'],'A':['0','1'],'D':['2','-1']}
        self.assertEqual(make_certificate(d)['angle_keys'],['0','0'])
    def test_obtuse_sign(self): self.assertEqual(self.cert['angle_keys'],['-3','-3'])
    def test_acute_sign(self):
        d={'E':['0','0'],'F':['2','0'],'A':['1','1'],'D':['1','-1']}
        self.assertEqual(make_certificate(d)['angle_keys'],['1','1'])
    def test_bool_schema(self):
        self.cert['schema']=True; self.assertFalse(verify_certificate(self.data,self.cert))
    def test_float_schema(self):
        self.cert['schema']=1.0; self.assertFalse(verify_certificate(self.data,self.cert))
    def test_string_schema(self):
        self.cert['schema']='1'; self.assertFalse(verify_certificate(self.data,self.cert))
    def test_missing_certificate_field(self):
        del self.cert['conclusion']; self.assertFalse(verify_certificate(self.data,self.cert))
    def test_extra_certificate_field(self):
        self.cert['extra']=0; self.assertFalse(verify_certificate(self.data,self.cert))
    def test_input_binding(self):
        d=list(positives())[1]; self.assertFalse(verify_certificate(d,self.cert))
    def test_rehashed_different_input(self):
        d=list(positives())[1]; other=make_certificate(d)
        self.assertFalse(verify_certificate(self.data,other))
    def test_mutated_side(self):
        self.cert['transversal_side_determinants'][0]='0'; self.assertFalse(verify_certificate(self.data,self.cert))
    def test_mutated_scale(self):
        self.cert['opposite_scale']='-1'; self.assertFalse(verify_certificate(self.data,self.cert))
    def test_mutated_angle(self):
        self.cert['angle_keys'][0]='3'; self.assertFalse(verify_certificate(self.data,self.cert))
    def test_mutated_conclusion(self):
        self.cert['conclusion']='parallel'; self.assertFalse(verify_certificate(self.data,self.cert))
    def test_non_json_tuple(self):
        self.cert['angle_keys']=tuple(self.cert['angle_keys']); self.assertFalse(verify_certificate(self.data,self.cert))
    def test_bad_input_fields(self):
        for k in ('E','F','A','D'):
            d=copy.deepcopy(self.data); del d[k]
            with self.assertRaises(ValueError): make_certificate(d)
    def test_extra_input_field(self):
        self.data['extra']=0
        with self.assertRaises(ValueError): make_certificate(self.data)
    def test_coordinate_types(self):
        for x in (True,False,1,1.0,None,[],{}):
            d=copy.deepcopy(self.data); d['E'][0]=x
            with self.assertRaises(ValueError): make_certificate(d)
    def test_noncanonical_rationals(self):
        for s in ('2/2','01','+1','1.0','0/1','-0','1/0','nan',' 1'):
            with self.assertRaises(ValueError): rational(s)
    def test_canonical_fraction(self): self.assertEqual(str(rational('-2/3')),'-2/3')
    def test_point_shape(self):
        for p in ([1],['0','0','0'],('0','0'),'00',None):
            d=copy.deepcopy(self.data);d['E']=p
            with self.assertRaises(ValueError): make_certificate(d)
    def test_nonobject_input(self):
        for d in ([],None,True,'x'):
            with self.assertRaises(ValueError): make_certificate(d)
    def test_nonobject_certificate(self):
        for c in ([],None,True,'x'): self.assertFalse(verify_certificate(self.data,c))
    def test_no_alias(self):
        self.data['E'][0]='1'; self.assertEqual(self.cert['input']['E'][0],'0')
    def test_strict_type_recursive(self):
        self.assertFalse(strict_equal({'x':[True]},{'x':[1]}))
    def test_bool_coordinate_in_certificate(self):
        self.cert['input']['E'][0]=False; self.assertFalse(verify_certificate(self.data,self.cert))
    def test_invalid_expected_input(self):
        for d in negative_cases().values(): self.assertFalse(verify_certificate(d,self.cert))

if __name__=='__main__': unittest.main(verbosity=2)
