import unittest,copy
from fractions import Fraction as F
from geometry import construct,verify,area,det,sub,mul
from cases import VALID,INVALID
class GeometryTests(unittest.TestCase):
 def test_grid(self):
  for args in VALID:self.assertTrue(verify(construct(*args)))
 def test_invalid(self):
  for args in INVALID:
   with self.assertRaises((ValueError,TypeError)):construct(*args)
 def test_example(self):
  P=construct(3,2,6,1,1)['points'];self.assertEqual(P['K'],(0,-2));self.assertEqual(P['L'],(-5,-2));self.assertEqual(P['M'],(-2,-2))
 def test_right(self):self.assertEqual(construct(3,2,6,0,1)['points']['M'],(0,-2))
 def test_obtuse(self):self.assertGreater(construct(3,2,6,-1,1)['points']['M'][0],0)
 def test_acute(self):self.assertLess(construct(3,2,6,1,1)['points']['M'][0],0)
 def test_fraction(self):self.assertTrue(verify(construct(F(3,2),F(2,3),F(5,7),-2,3)))
 def test_scale_direction(self):self.assertEqual(construct(3,2,6,1,2)['points'],construct(3,2,6,3,6)['points'])
 def test_output_independent_b(self):
  x=construct(3,2,6,1,2);y=construct(3,5,6,1,2)
  for k in 'ABML':self.assertEqual(x['points'][k],y['points'][k])
 def test_prescribed_base(self):
  for args in VALID:self.assertEqual(construct(*args)['points']['A'],(-args[0],0))
 def test_ray_order(self):
  for args in VALID:
   c=construct(*args);a,b,*_=c['parameters'];self.assertGreater((a+b)/a,1)
 def test_area(self):
  for args in VALID:
   P=construct(*args)['points'];self.assertEqual(area([P[k] for k in 'ABML']),args[2])
 def test_outer_diagonal(self):
  for args in VALID:
   P=construct(*args)['points'];self.assertEqual(det(sub(P['B'],P['H']),sub(P['K'],P['H'])),0)
 def test_tampered_K(self):
  c=construct(3,2,6,1,1);c['points']['K']=(0,2);self.assertFalse(verify(c))
 def test_wrong_side(self):
  c=construct(3,2,6,1,1);c['points']['A']=(3,0);self.assertFalse(verify(c))
 def test_reverse_ray(self):
  c=construct(3,2,6,1,1);c['points']['M']=mul(-1,c['points']['M']);self.assertFalse(verify(c))
 def test_swapped_labels(self):
  c=construct(3,2,6,1,1);P=c['points'];P['F'],P['G']=P['G'],P['F'];self.assertFalse(verify(c))
 def test_missing(self):self.assertFalse(verify({}))
 def test_extra_point(self):
  c=construct(3,2,6,1,1);c['points']['X']=(0,0);self.assertFalse(verify(c))
 def test_area_not_congruence(self):
  c=construct(3,2,6,0,1);P=c['points'];self.assertNotEqual(sub(P['E'],P['B']),sub(P['B'],P['A']))
 def test_no_assert_dependency(self):self.assertFalse(verify({'parameters':(0,1,1,1,1),'points':{},'v':(1,1)}))
if __name__=='__main__':unittest.main()
