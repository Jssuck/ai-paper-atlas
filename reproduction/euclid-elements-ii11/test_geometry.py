import unittest,copy
from fractions import Fraction as F
from geometry import Q5,make_certificate,validate_certificate,area
class GeometryTests(unittest.TestCase):
 def test_default(self):self.assertEqual(validate_certificate(make_certificate(1))['target_left'],Q5(F(3,2),F(-1,2)))
 def test_grid(self):
  for i in range(1,9):
   for j in range(1,9):validate_certificate(make_certificate(F(i,j),origin=(i,-j),u=(3,4),v=(-4,3)))
 def test_reflection(self):validate_certificate(make_certificate(7,u=(0,2),v=(2,0)))
 def test_translation(self):validate_certificate(make_certificate(F(2,3),origin=(F(1,7),-8)))
 def test_scale(self):self.assertEqual(validate_certificate(make_certificate(3,u=(2,0),v=(0,2)))['square_AB'],Q5(36))
 def test_radical_square(self):self.assertEqual(Q5(0,1)**2,Q5(5))
 def test_radical_inverse(self):self.assertEqual(Q5(1,1)/Q5(1,1),Q5(1))
 def test_exact_sign(self):
  self.assertTrue(Q5(-2,1)>0);self.assertTrue(Q5(-3,1)<0);self.assertTrue(Q5(2,-1)<0);self.assertTrue(Q5(3,-1)>0)
 def test_zero_sign(self):self.assertEqual(Q5().sign(),0)
 def test_zero_length(self):
  with self.assertRaises(ValueError):make_certificate(0)
 def test_negative_length(self):
  with self.assertRaises(ValueError):make_certificate(-2)
 def test_bool(self):
  with self.assertRaises(ValueError):make_certificate(True)
 def test_float(self):
  with self.assertRaises(ValueError):make_certificate(1.0)
 def test_skew(self):
  with self.assertRaises(ValueError):make_certificate(1,u=(1,0),v=(1,1))
 def test_unequal(self):
  with self.assertRaises(ValueError):make_certificate(1,u=(1,0),v=(0,2))
 def test_zero_basis(self):
  with self.assertRaises(ValueError):make_certificate(1,u=(0,0),v=(0,0))
 def test_point_tampering(self):
  c=make_certificate(1);c['points']['H']=(Q5(F(1,2)),Q5(0))
  with self.assertRaises(ValueError):validate_certificate(c)
 def test_missing_point(self):
  c=make_certificate(1);del c['points']['F']
  with self.assertRaises(ValueError):validate_certificate(c)
 def test_nonexact_point(self):
  c=make_certificate(1);c['points']['A']=(0,0)
  with self.assertRaises(ValueError):validate_certificate(c)
 def test_negative_root(self):
  c=make_certificate(1);c['points']['H']=(Q5(F(-1,2),F(-1,2)),Q5(0))
  with self.assertRaises(ValueError):validate_certificate(c)
if __name__=='__main__':unittest.main()
