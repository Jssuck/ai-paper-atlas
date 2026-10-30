import unittest
from geometry import *
class GeometryTests(unittest.TestCase):
 def test_world_float(self):
  with self.assertRaises(TypeError): Segment(1,0).world((0.1,0))
 def test_world_bool(self):
  with self.assertRaises(TypeError): Segment(1,0).world((True,0))
 def test_base_zero(self):
  with self.assertRaises(ValueError): Segment(0,1)
 def test_base_negative(self):
  with self.assertRaises(ValueError): Segment(-1,1)
 def test_float(self):
  with self.assertRaises(TypeError): Segment(1,0.1)
 def test_bool(self):
  with self.assertRaises(TypeError): Segment(True,0)
 def test_nonunit(self):
  with self.assertRaises(ValueError): Segment(1,0,e=(2,0))
 def test_nonorthogonal(self):
  with self.assertRaises(ValueError): Segment(1,0,n=(1,0))
 def test_zero_slope(self):
  with self.assertRaises(ValueError): Segment(1,0).arc_point(0)
 def test_wrong_ray(self):
  with self.assertRaises(ValueError): Segment(1,-2).arc_point(1)
 def test_endpoint(self):
  with self.assertRaises(ValueError): Segment(1,0).measured_cot((1,0))
 def test_interior(self):
  with self.assertRaises(ValueError): Segment(1,0).measured_cot((0,F(1,2)))
 def test_wrong_arc(self):
  with self.assertRaises(ValueError): Segment(1,0).measured_cot((0,-1))
 def test_kind(self): self.assertEqual([Segment(1,k).kind for k in [-1,0,1]],['minor','semicircle','major'])
 def test_scale_similar(self): self.assertTrue(Segment(1,1).similar(Segment(2,2)))
 def test_scale_not_rigid(self):
  with self.assertRaises(ValueError): Segment(1,1).align_point_to(Segment(2,2),(0,0))
 def test_different_angles(self): self.assertFalse(Segment(1,1).similar(Segment(1,-1)))
 def test_near_not_equal(self): self.assertFalse(Segment(1,1).similar(Segment(1,1+F(1,10**30))))
 def test_translation(self):
  s=Segment(1,1); t=Segment(1,1,mid=(4,2)); self.assertTrue(s.aligned_circle_matches(t)); self.assertFalse(s.coincides(t))
 def test_mirror(self):
  s=Segment(1,1); t=Segment(1,1,n=(0,-1)); self.assertTrue(s.similar(t)); self.assertTrue(s.aligned_circle_matches(t)); self.assertFalse(s.coincides(t))
 def test_same_circle_other_side(self):
  s=Segment(1,1); t=Segment(1,-1,n=(0,-1)); self.assertEqual(s.center,t.center); self.assertFalse(s.similar(t))
 def test_semicircle_other_side(self):
  s=Segment(1,0); t=Segment(1,0,n=(0,-1)); self.assertTrue(s.similar(t)); self.assertFalse(s.coincides(t))
 def test_endpoint_swap(self): self.assertTrue(Segment(1,1).coincides(Segment(1,1,e=(-1,0))))
 def test_align_without_similarity(self): self.assertFalse(Segment(1,1).aligned_circle_matches(Segment(1,2)))
 def test_frame_inverse(self):
  s=Segment(2,-1,(3,5),(F(3,5),F(4,5)),(F(4,5),F(-3,5))); self.assertEqual(s.local(s.world((F(2,3),F(4,7)))),(F(2,3),F(4,7)))
 def test_boundary(self):
  s=Segment(1,0); self.assertTrue(s.contains((1,0))); self.assertTrue(s.contains((0,1))); self.assertFalse(s.contains((0,-1)))
 def test_exact_example(self):
  s=Segment(2,F(3,2)); p=s.arc_point(1); self.assertEqual(p,(F(3,2),F(7,2))); self.assertEqual(s.measured_cot(p),F(3,4))
 def test_grid(self): self.assertEqual(grid(),dict(configurations=39,placements=156,arc_checks=936,membership_checks=6552,unequal_base_pairs=39))
if __name__=='__main__': unittest.main(verbosity=2)
