import unittest
from fractions import Fraction as F
from geometry import *
class Checks(unittest.TestCase):
 def test_unit_semicircle(self): self.assertEqual(cot(point(0,1)),0)
 def test_negative_cot_obtuse(self): self.assertEqual(cot(point(-1,F(1,4))),-1)
 def test_positive_cot_acute(self): self.assertEqual(cot(point(1,1)),1)
 def test_point_on_circle(self): self.assertEqual(residual(F(3,7),point(F(3,7),F(1,5))),0)
 def test_order(self): self.assertLess(ordered_witness(-2,3)['C'][1],ordered_witness(-2,3)['D'][1])
 def test_equal_rejected(self): self.assertRaises(ValueError,ordered_witness,1,1)
 def test_reversed_rejected(self): self.assertRaises(ValueError,ordered_witness,2,1)
 def test_zero_ray_rejected(self): self.assertRaises(ValueError,point,1,0)
 def test_tangent_rejected(self): self.assertRaises(ValueError,point,-1,1)
 def test_base_vertex_rejected(self): self.assertRaises(ValueError,cot,A)
 def test_bad_side(self): self.assertRaises(ValueError,segment_cot,1,0)
 def test_bad_side_inside(self): self.assertRaises(ValueError,inside,1,(0,1),0)
 def test_reflection_is_similar_and_congruent_not_unequal(self): self.assertEqual(segment_cot(1,1),segment_cot(-1,-1))
 def test_distinct_same_side_not_similar(self): self.assertNotEqual(segment_cot(1,1),segment_cot(2,1))
 def test_same_circle_opposite_not_similar(self): self.assertNotEqual(segment_cot(1,1),segment_cot(1,-1))
 def test_semicircles_similar_congruent(self): self.assertEqual(segment_cot(0,1),segment_cot(0,-1))
 def test_strict_nested(self):
  z=ordered_witness(-1,1);self.assertTrue(inside(1,z['C']));self.assertFalse(inside(-1,z['D']))
 def test_lower_reflection(self):
  p=point(2,F(1,8));q=point(-2,F(-1,8));self.assertEqual(q,(p[0],-p[1]))
 def test_near_equal_exact(self):
  z=ordered_witness(1,1+F(1,10**30));self.assertEqual(z['cot_D']-z['cot_C'],F(1,10**30))
 def test_finite_grid(self): self.assertGreater(grid()['strict_nested_pairs'],100)
if __name__=='__main__': unittest.main(verbosity=2)
