import unittest,copy
from fractions import Fraction as Q
from geometry import *
from cases import *
class ConstructionTests(unittest.TestCase):
 def test_example(self):
  c=make_certificate(example());self.assertEqual(c['points'],{'E':['2','0'],'F':['5','3'],'G':['7','3']});self.assertEqual(c['double_areas'],{'ABC':'12','ABE':'6','AEC':'6','FECG':'12'})
 def test_valid_grid(self):
  for p in valid_cases():
   with self.subTest(p=p): self.assertTrue(verify_certificate(p,make_certificate(p)))
 def test_invalid_direct(self):
  for label,p in invalid_cases():
   with self.subTest(label=label):
    with self.assertRaises(ValueError):make_certificate(p)
 def test_invalid_verifier(self):
  for _,p in invalid_cases():self.assertFalse(verify_certificate(p,{}))
 def test_right_angle(self):self.assertEqual(make_certificate(example(0))['points']['F'],['2','3'])
 def test_obtuse(self):self.assertEqual(make_certificate(example(-2))['points']['F'],['-4','3'])
 def test_small_angle(self):self.assertEqual(make_certificate(example(100))['points']['F'],['302','3'])
 def test_F_equals_A(self):self.assertEqual(make_certificate(example(Q(-1,3)))['points']['F'],['1','3'])
 def test_G_equals_A(self):self.assertEqual(make_certificate(example(-1))['points']['G'],['1','3'])
 def test_scaled_direction(self):
  p=example();q=example();q['u']=(7,7);self.assertEqual(make_certificate(p)['points'],make_certificate(q)['points']);self.assertFalse(verify_certificate(q,make_certificate(p)))
 def test_wrong_ray(self):
  p=example();p['u']=(-1,-1)
  with self.assertRaises(ValueError):make_certificate(p)
 def test_negative_height(self):
  p=example();p['A']=(1,-3);p['u']=(1,-1);self.assertEqual(make_certificate(p)['points']['F'],['5','-3'])
 def test_reverse_base(self):
  p=example();p['B'],p['C']=p['C'],p['B'];self.assertEqual(make_certificate(p)['points']['G'],['3','3'])
 def test_extra_certificate_field(self):
  c=make_certificate(example());c['extra']=0;self.assertFalse(verify_certificate(example(),c))
 def test_altered_point(self):
  c=make_certificate(example());c['points']['F'][0]='99';self.assertFalse(verify_certificate(example(),c))
 def test_altered_area(self):
  c=make_certificate(example());c['double_areas']['ABC']='13';self.assertFalse(verify_certificate(example(),c))
 def test_bool_tamper(self):
  c=make_certificate(example());c['parameter_t']=True;self.assertFalse(verify_certificate(example(),c))
 def test_rebind_same_area(self):self.assertFalse(verify_certificate(example(-1),make_certificate(example(1))))
 def test_missing_certificate(self):self.assertFalse(verify_certificate(example(),{}))
 def test_nonserializable(self):self.assertFalse(verify_certificate(example(),{'a':set()}))
 def test_no_input_mutation(self):
  p=example();old=copy.deepcopy(p);make_certificate(p);self.assertEqual(p,old)
 def test_singular_input_type(self):
  with self.assertRaises(ValueError):make_certificate(None)
 def test_exact_fraction(self):
  p=example(Q(1,7));self.assertEqual(make_certificate(p)['points']['F'],['17/7','3'])
if __name__=='__main__':unittest.main()
