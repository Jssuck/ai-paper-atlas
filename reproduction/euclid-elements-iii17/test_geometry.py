import unittest
from geometry import *
class Tests(unittest.TestCase):
 def test_grid(self):self.assertEqual(grid(),dict(configurations=324,certificates=648,power_checks=3240))
 def test_coordinates(self):
  c=construct(3,5);self.assertEqual(c['D'],(3,0));self.assertEqual(c['F'],(3,4));self.assertEqual(c['B'],(Q(9,5),Q(12,5)))
 def test_reflection(self):self.assertEqual(construct(3,5,side=-1)['B'],(Q(9,5),Q(-12,5)))
 def test_boundary(self):self.assertTrue(verify(construct(3,3)))
 def test_boundary_power(self):self.assertEqual(line_power(construct(3,3),2),4)
 def test_translation(self):self.assertTrue(verify(construct(3,5,(4,-2))))
 def test_rotation(self):self.assertTrue(verify(construct(3,5,axis=(Q(3,5),Q(4,5)))))
 def test_scale(self):self.assertTrue(verify(construct(Q(3,7),Q(5,7))))
 def test_inner(self):self.assertRaises(ValueError,construct,3,2)
 def test_center(self):self.assertRaises(ValueError,construct,3,0)
 def test_zero_radius(self):self.assertRaises(ValueError,construct,0,0)
 def test_negative_radius(self):self.assertRaises(ValueError,construct,-3,5)
 def test_negative_distance(self):self.assertRaises(ValueError,construct,3,-5)
 def test_irrational(self):self.assertRaises(ValueError,construct,1,2)
 def test_float(self):self.assertRaises(ValueError,construct,3.0,5)
 def test_bool(self):self.assertRaises(ValueError,construct,True,5)
 def test_axis(self):self.assertRaises(ValueError,construct,3,5,axis=(1,1))
 def test_zero_axis(self):self.assertRaises(ValueError,construct,3,5,axis=(0,0))
 def test_side(self):self.assertRaises(ValueError,construct,3,5,side=0)
 def test_bool_side(self):self.assertRaises(ValueError,construct,3,5,side=True)
 def test_tamper(self):
  for key in ['A','B','D','F','direction','E']:
   c=construct(3,5);c[key]=add(c[key],(1,0));self.assertFalse(verify(c))
 def test_extra(self):
  c=construct(3,5);c['extra']=1;self.assertFalse(verify(c))
 def test_missing(self):
  c=construct(3,5);del c['D'];self.assertFalse(verify(c))
 def test_type(self):self.assertFalse(verify(None))
 def test_bad_scalar(self):
  c=construct(3,5);c['r']=3.0;self.assertFalse(verify(c))
 def test_zero_direction(self):
  c=construct(3,3);c['direction']=(0,0);self.assertFalse(verify(c))
 def test_sqrt(self):self.assertEqual(sqrtq(Q(4,9)),Q(2,3))
 def test_negative_sqrt(self):self.assertRaises(ValueError,sqrtq,-1)
if __name__=='__main__':unittest.main(verbosity=2)
