import unittest
from fractions import Fraction as F
from geometry import *
class ExactModel(unittest.TestCase):
 def test_grid(self):self.assertEqual(grid()['cases'],2160)
 def test_examples(self):
  for p in EXAMPLES.values():check(*p)
 def test_arc_types(self):
  self.assertEqual(check(*EXAMPLES['reflex_extension'])['arc'],'major')
  self.assertEqual(check(*EXAMPLES['addition'])['arc'],'minor')
  self.assertEqual(check(*EXAMPLES['base_diameter'])['arc'],'semicircle')
 def test_positions(self):
  for key,pos in [('addition','inside'),('subtraction','outside'),('side_boundary','boundary')]:self.assertEqual(check(*EXAMPLES[key])['center_location'],pos)
 def test_two_boundaries_differ(self):
  self.assertTrue(check(*EXAMPLES['side_boundary'])['side_through_center'])
  self.assertFalse(check(*EXAMPLES['side_boundary'])['base_diameter'])
  self.assertTrue(check(*EXAMPLES['base_diameter'])['base_diameter'])
  self.assertFalse(check(*EXAMPLES['base_diameter'])['side_through_center'])
 def test_wrong_minor_counterexample(self):
  r=check(*EXAMPLES['reflex_extension']);self.assertLess(r['central'][1],0)
  self.assertNotEqual((r['central'][0],abs(r['central'][1])),r['doubled'])
 def test_swap(self):
  for A,B,C in EXAMPLES.values():self.assertEqual(check(A,B,C)['central'],check(A,C,B)['central'])
 def test_central_unit(self):
  for A,B,C in EXAMPLES.values():
   x,y=check(A,B,C)['central'];self.assertEqual(x*x+y*y,1)
 def test_parametrization(self):
  for x,y in sample_points():self.assertEqual(x*x+y*y,1)
 def test_duplicates(self):
  for A,B,C in [((1,0),(1,0),(0,1)),((1,0),(0,1),(0,1))]:
   with self.assertRaises(ValueError):evaluate(A,B,C)
 def test_off_circle(self):
  with self.assertRaises(ValueError):evaluate((1,0),(0,2),(-1,0))
 def test_zero_radius(self):
  with self.assertRaises(ValueError):evaluate((0,0),(0,0),(0,0))
 def test_float_rejected(self):
  with self.assertRaises(ValueError):evaluate((1.,0),(0,1),(-1,0))
 def test_bool_rejected(self):
  with self.assertRaises(ValueError):point((True,0))
 def test_bad_dimension(self):
  with self.assertRaises(ValueError):point((1,2,3))
 def test_transform_rejected(self):
  with self.assertRaises(ValueError):transform((1,0),9)
if __name__=='__main__':unittest.main(verbosity=2)
