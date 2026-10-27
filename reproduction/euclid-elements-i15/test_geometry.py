import unittest
from copy import deepcopy
from fractions import Fraction as F
from geometry import *
from cases import positives,negative_inputs,run

class Tests(unittest.TestCase):
    def setUp(self): self.data=next(positives());self.c=certificate(self.data)
    def test_roundtrip(self): self.assertTrue(verify(self.data,self.c))
    def test_all_cases(self): self.assertEqual(run()['positive_certificates'],135)
    def test_all_invalid(self):
        for d in negative_inputs(): self.assertFalse(verify(d,{}))
    def test_rational(self): self.assertEqual(rational('2/3'),F(2,3))
    def test_bool_input(self): self.assertRaises(ValueError,rational,True)
    def test_float_input(self): self.assertRaises(ValueError,rational,0.5)
    def test_zero_ray(self): self.assertRaises(ValueError,angle,(0,0),(1,0))
    def test_right_angle(self): self.assertEqual(angle((1,0),(0,3)),(0,1))
    def test_obtuse(self): self.assertEqual(angle((1,0),(-1,1)),(F(-1,2),F(1,2)))
    def test_simultaneous_reversal(self): self.assertEqual(angle((2,1),(1,3)),angle((-4,-2),(-3,-9)))
    def test_one_reversal_not_equal(self): self.assertNotEqual(angle((2,1),(1,3)),angle((-2,-1),(1,3)))
    def test_angle_symmetry(self): self.assertEqual(angle((2,1),(1,3)),angle((1,3),(2,1)))
    def test_positive_scaling(self): self.assertEqual(angle((2,1),(1,3)),angle((6,3),(2,6)))
    def test_opposite_scale(self): self.assertEqual(opposite_scale((2,3),(-4,-6)),2)
    def test_same_ray(self): self.assertRaises(ValueError,opposite_scale,(2,3),(4,6))
    def test_noncollinear(self): self.assertRaises(ValueError,opposite_scale,(2,3),(1,1))
    def test_missing_claim(self): self.assertFalse(verify(self.data,{}))
    def test_extra_claim(self): self.c['extra']=0;self.assertFalse(verify(self.data,self.c))
    def test_int_bool_version(self): self.c['schema_version']=True;self.assertFalse(verify(self.data,self.c))
    def test_bool_int_result(self): self.c['vertical_pairs_equal'][0]=1;self.assertFalse(verify(self.data,self.c))
    def test_nan_claim(self): self.c['schema_version']=float('nan');self.assertFalse(verify(self.data,self.c))
    def test_tuple_claim(self): self.c['opposite_scales']=tuple(self.c['opposite_scales']);self.assertFalse(verify(self.data,self.c))
    def test_mutate_angle(self): self.c['angles_CEA_AED_DEB_BEC'][0][0]='1';self.assertFalse(verify(self.data,self.c))
    def test_input_binding(self): self.data['E']=['3','3'];self.assertFalse(verify(self.data,self.c))
    def test_scale_binding(self): self.data['B']=['-2','0'];self.assertFalse(verify(self.data,self.c))
    def test_numeric_string_binding(self): self.c['schema_version']='1';self.assertFalse(verify(self.data,self.c))
    def test_ledger(self): self.assertEqual(angle_ledger('2/3','4/3','2/3')['four_angles_sum'],'4')
    def test_ledger_missing_premise(self): self.assertRaises(ValueError,angle_ledger,'2/3','4/3','1/2')
    def test_ledger_degenerate(self): self.assertRaises(ValueError,angle_ledger,0,2,0)
    def test_ledger_bool(self): self.assertRaises(ValueError,angle_ledger,True,1,1)
    def test_nonstring_key(self): self.assertRaises(ValueError,canonical,{1:2})
    def test_zero_point(self): self.assertRaises(ValueError,point,[0])

if __name__=='__main__': unittest.main(verbosity=2)
