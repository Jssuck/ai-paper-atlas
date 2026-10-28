import unittest,copy
from fractions import Fraction as Q
from geometry import construct,verify,area,sub,cross,dot
from cases import valid_cases,INVALID
class Tests(unittest.TestCase):
 def setUp(self):self.A=(0,0);self.B=(3,0);self.c=construct(self.A,self.B)
 def ok(self,c):return verify(self.A,self.B,1,c)
 def mutate(self,k,v):c=copy.deepcopy(self.c);c['points'][k]=v;return c
 def test_grid(self):
  for A,B,s in valid_cases():self.assertTrue(verify(A,B,s,construct(A,B,s)))
 def test_illegal(self):
  for name,A,B,s in INVALID:
   with self.subTest(name=name),self.assertRaises(ValueError):construct(A,B,s)
 def test_verifier_input_validation(self):
  for name,A,B,s in INVALID:
   with self.subTest(name=name),self.assertRaises(ValueError):verify(A,B,s,self.c)
 def test_known(self):self.assertEqual(self.c['points']['E'],(3,3))
 def test_opposite_side(self):self.assertEqual(construct(self.A,self.B,-1)['points']['E'],(3,-3))
 def test_rotated(self):self.assertEqual(construct((0,0),(3,4))['points']['D'],(-4,3))
 def test_area(self):self.assertEqual(area([self.c['points'][k] for k in 'ADEB']),9)
 def test_rectangle_not_square(self):self.assertFalse(self.ok(self.mutate('D',(0,2))))
 def test_rhombus_not_square(self):
  c=self.mutate('D',(Q(9,5),Q(12,5)));c['points']['E']=(Q(24,5),Q(12,5));self.assertFalse(self.ok(c))
 def test_crossed_pairing(self):
  c=copy.deepcopy(self.c);c['points']['D'],c['points']['E']=c['points']['E'],c['points']['D'];self.assertFalse(self.ok(c))
 def test_wrong_intersection(self):self.assertFalse(self.ok(self.mutate('E',(4,3))))
 def test_wrong_base(self):self.assertFalse(self.ok(self.mutate('B',(4,0))))
 def test_C_equal_D(self):self.assertFalse(self.ok(self.mutate('C',(0,3))))
 def test_C_wrong_ray(self):self.assertFalse(self.ok(self.mutate('C',(0,-6))))
 def test_C_not_perpendicular(self):self.assertFalse(self.ok(self.mutate('C',(1,6))))
 def test_C_arbitrary_beyond(self):self.assertTrue(self.ok(self.mutate('C',(0,10))))
 def test_certificate_bool(self):
  c=copy.deepcopy(self.c);c['side']=True;self.assertFalse(self.ok(c))
 def test_certificate_scalar(self):
  c=copy.deepcopy(self.c);c['side_squared']=9.;self.assertFalse(self.ok(c))
 def test_certificate_shape(self):
  for c in [None,[],{},dict(self.c,unexpected=1)]:self.assertFalse(self.ok(c))
 def test_point_float(self):self.assertFalse(self.ok(self.mutate('D',(0.,3))))
 def test_mirror_rejected_for_side(self):self.assertFalse(self.ok(construct(self.A,self.B,-1)))
if __name__=='__main__':unittest.main()
