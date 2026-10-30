import unittest,copy
from fractions import Fraction as F
from geometry import *
class Tests(unittest.TestCase):
 def test_tangent(self):self.assertEqual(certify((0,0),(3,0),3,(0,2))['kind'],'tangent')
 def test_oblique(self):self.assertEqual(certify((0,0),(3,0),3,(1,1))['power'],F(-9,2))
 def test_radial(self):self.assertEqual(certify((0,0),(3,0),3,(1,0))['h'],(0,0))
 def test_reverse(self):
  a=certify((0,0),(3,0),3,(1,2));b=certify((0,0),(3,0),3,(-1,-2));self.assertEqual(a['h'],b['h'])
 def test_scaling(self):
  a=certify((0,0),(3,0),3,(1,2));b=certify((0,0),(3,0),3,(2,4));self.assertEqual(a['h'],b['h'])
 def test_translation(self):self.assertEqual(certify((2,1),(5,1),3,(1,1))['power'],F(-9,2))
 def test_rotation(self):self.assertEqual(certify((0,0),(0,3),3,(-1,1))['power'],F(-9,2))
 def test_circle(self):
  with self.assertRaises(ValueError):certify((0,0),(2,0),3,(1,1))
 def test_zero_radius(self):
  with self.assertRaises(ValueError):certify((0,0),(0,0),0,(1,1))
 def test_negative_radius(self):
  with self.assertRaises(ValueError):certify((0,0),(3,0),-3,(1,1))
 def test_zero_direction(self):
  with self.assertRaises(ValueError):certify((0,0),(3,0),3,(0,0))
 def test_bool(self):
  with self.assertRaises(ValueError):certify((False,0),(3,0),3,(1,1))
 def test_float(self):
  with self.assertRaises(ValueError):certify((0,0),(3,0),3.0,(1,1))
 def test_shape(self):
  with self.assertRaises(ValueError):certify((0,),(3,0),3,(1,1))
 def test_string(self):
  with self.assertRaises(ValueError):certify((0,0),(3,0),'3',(1,1))
 def test_missing(self):
  c=certify((0,0),(3,0),3,(1,1));del c['h'];self.assertFalse(verify(c))
 def test_extra(self):
  c=certify((0,0),(3,0),3,(1,1));c['extra']=1;self.assertFalse(verify(c))
 def test_kind(self):
  c=certify((0,0),(3,0),3,(1,1));c['kind']='tangent';self.assertFalse(verify(c))
 def test_fields(self):
  for k in ['q','s','t','power']:
   c=certify((0,0),(3,0),3,(1,1));c[k]+=1;self.assertFalse(verify(c))
 def test_point_tamper(self):
  c=certify((0,0),(3,0),3,(1,1));c['h']=(0,0);self.assertFalse(verify(c))
 def test_bool_certificate(self):
  c=certify((0,0),(3,0),3,(0,1));c['q']=False;self.assertFalse(verify(c))
 def test_non_dict(self):self.assertFalse(verify([]))
 def test_tangent_powers(self):
  c=certify((0,0),(3,0),3,(0,1))
  for t in [F(-1,3),0,F(2,7)]:self.assertEqual(line_power(c,t),t*t)
 def test_second_crossing(self):
  c=certify((0,0),(3,0),3,(1,1));self.assertEqual(line_power(c,-2*c['q']/c['s']),0)
 def test_grid(self):self.assertEqual(grid(),dict(configurations=360,tangent=72,interior_witness=288,power_checks=1800))
if __name__=='__main__':unittest.main(verbosity=2)
