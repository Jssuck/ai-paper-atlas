import unittest
from copy import deepcopy
from fractions import Fraction as Q
from geometry import construct,verify,area,inputs
from cases import BASE,valid_cases,INVALID
class Tests(unittest.TestCase):
 def test_reference(self):
  c=construct(BASE); self.assertEqual(c['areas'],(4,7,11));self.assertEqual(c['points']['L'],(Q(13,2),Q(2)))
 def test_grid(self):
  for a in valid_cases(): self.assertTrue(verify(*a,construct(*a)))
 def test_invalid_direct(self):
  for name,*a in INVALID:
   with self.subTest(name=name),self.assertRaises(ValueError):construct(*a)
 def test_invalid_verify(self):
  for name,*a in INVALID:self.assertFalse(verify(*a,construct(BASE)))
 def test_reverse(self): self.assertTrue(verify(BASE[::-1],2,1,2,construct(BASE[::-1])))
 def test_area(self):
  self.assertEqual(area(list(BASE)),11);self.assertIs(type(area(list(BASE))),Q)
 def test_extra_key(self):
  c=construct(BASE);c['extra']=1;self.assertFalse(verify(BASE,2,1,2,c))
 def test_missing_key(self):
  c=construct(BASE);del c['points']['G'];self.assertFalse(verify(BASE,2,1,2,c))
 def test_boolean_certificate(self):
  c=construct(BASE);c['points']['K']=(False,Q(0));self.assertFalse(verify(BASE,2,1,2,c))
 def test_integer_certificate(self):
  c=construct(BASE);c['points']['K']=(0,0);self.assertFalse(verify(BASE,2,1,2,c))
 def test_area_tamper(self):
  c=construct(BASE);c['areas']=(Q(4),Q(7),Q(12));self.assertFalse(verify(BASE,2,1,2,c))
 def test_point_tamper(self):
  for k in 'KFGHLM':
   c=construct(BASE);x,y=c['points'][k];c['points'][k]=(x+1,y);self.assertFalse(verify(BASE,2,1,2,c))
 def test_wrong_angle(self):self.assertFalse(verify(BASE,2,-1,2,construct(BASE)))
 def test_wrong_height(self):self.assertFalse(verify(BASE,3,1,2,construct(BASE)))
 def test_same_ray(self):self.assertEqual(construct(BASE,2,2,4),construct(BASE,2,1,2))
 def test_vertical(self):self.assertTrue(verify(BASE,2,0,1,construct(BASE,2,0,1)))
 def test_obtuse(self):self.assertTrue(verify(BASE,2,-3,1,construct(BASE,2,-3,1)))
 def test_overlap_tamper(self):
  c=construct(BASE);c['points']['M']=(Q(1),Q(0));c['points']['L']=(Q(2),Q(2));self.assertFalse(verify(BASE,2,1,2,c))
 def test_bad_schema(self):
  for c in (None,[],{},42):self.assertFalse(verify(BASE,2,1,2,c))
 def test_fraction_vertices(self):
  v=tuple((Q(x,3),Q(y,3))for x,y in BASE);self.assertEqual(construct(v)['areas'][2],Q(11,9))
if __name__=='__main__':unittest.main(verbosity=2)
