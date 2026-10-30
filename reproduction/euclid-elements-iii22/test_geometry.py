import unittest
from fractions import Fraction as F
from geometry import certificate,cot,circle_points,grid
from independent_oracle import angle,check
Q=((1,0),(0,1),(-1,0),(0,-1))
class Tests(unittest.TestCase):
 def test_square(self): self.assertEqual(certificate(Q)['cots'],(0,0,0,0))
 def test_reverse(self): self.assertEqual(certificate(Q[::-1])['orientation'],-1)
 def test_rotations(self):
  for i in range(4): self.assertEqual(certificate(Q[i:]+Q[:i])['opposite_sums'],(0,0))
 def test_nonrectangular(self):
  q=tuple(circle_points()[:4]); z=certificate(q); self.assertTrue(any(x<0 for x in z['cots']));self.assertEqual(z['opposite_sums'],(0,0))
 def test_original_substitutions(self): self.assertEqual(certificate(tuple(circle_points()[::3]))['same_segment'],(True,True))
 def test_split(self): self.assertTrue(certificate(tuple(circle_points()[:4]))['split_matches_D'])
 def test_triangle(self): self.assertEqual(certificate(tuple(circle_points()[:4]))['triangle_sum'],0)
 def test_translation_scale(self): self.assertEqual(certificate(tuple((3+5*x,-2+5*y) for x,y in Q),(3,-2),25)['cots'],(0,0,0,0))
 def test_crossed(self):
  with self.assertRaises(ValueError): certificate((Q[0],Q[2],Q[1],Q[3]))
 def test_crossed_counterexample(self):
  import math
  q=(Q[0],Q[2],Q[1],Q[3]); self.assertAlmostEqual(angle(q[3],q[0],q[1])+angle(q[1],q[2],q[3]),math.pi/2)
 def test_repeated(self):
  with self.assertRaises(ValueError): certificate((Q[0],Q[1],Q[2],Q[0]))
 def test_noncyclic(self):
  with self.assertRaises(ValueError): certificate(((0,0),(2,0),(2,1),(0,2)))
 def test_interior(self):
  with self.assertRaises(ValueError): certificate((Q[0],Q[1],Q[2],(0,0)))
 def test_radius(self):
  for r in (0,-1):
   with self.assertRaises(ValueError): certificate(Q,radius2=r)
 def test_types(self):
  for r in (True,1.0,'1'):
   with self.assertRaises(TypeError): certificate(Q,radius2=r)
 def test_shape(self):
  with self.assertRaises(ValueError): certificate(Q[:3])
 def test_collinear(self):
  with self.assertRaises(ValueError): cot((0,0),(1,0),(2,0))
 def test_near_degenerate_exact(self):
  t=F(1,10**12); p=((1-t*t)/(1+t*t),2*t/(1+t*t)); self.assertEqual(certificate((Q[0],p,Q[1],Q[2]))['opposite_sums'],(0,0))
 def test_grid(self): self.assertEqual(grid()['configurations'],2970)
 def test_oracle(self): self.assertEqual(check()['configurations'],2970)
if __name__=='__main__': unittest.main(verbosity=2)
