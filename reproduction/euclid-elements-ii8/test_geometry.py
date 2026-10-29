import unittest,copy
from fractions import Fraction as Q
from geometry import construct,verify,area
class GeometryTests(unittest.TestCase):
 def test_default(self):self.assertEqual(verify(construct())['whole'],49)
 def test_four_squares(self):
  r=verify(construct());self.assertEqual([r[k] for k in ('CK','KD','GR','RN')],[4]*4)
 def test_four_rectangles(self):
  r=verify(construct());self.assertEqual([r[k] for k in ('AG','MQ','QL','RF')],[6]*4)
 def test_gnomon(self):self.assertEqual(verify(construct())['gnomon'],40)
 def test_missing_square(self):self.assertEqual(verify(construct())['OH'],9)
 def test_equal_cut(self):self.assertEqual(verify(construct(2,2),2,2)['whole'],36)
 def test_rational(self):self.assertEqual(verify(construct(Q(1,3),Q(1,2)),Q(1,3),Q(1,2))['whole'],Q(16,9))
 def test_rotation(self):self.assertEqual(verify(construct(u=(0,1),v=(-1,0)),u=(0,1),v=(-1,0))['whole'],49)
 def test_reflection(self):self.assertEqual(verify(construct(v=(0,-1)),v=(0,-1))['whole'],49)
 def test_scale(self):self.assertEqual(verify(construct(u=(3,4),v=(-4,3)),u=(3,4),v=(-4,3))['whole'],1225)
 def test_translation(self):self.assertEqual(verify(construct(origin=(-9,11)),origin=(-9,11))['whole'],49)
 def test_grid(self):
  for a in range(1,9):
   for b in range(1,9):self.assertEqual(verify(construct(a,b),a,b)['whole'],(a+2*b)**2)
 def test_nonpositive(self):
  for x in (0,-1):
   with self.assertRaises(ValueError):construct(x,2)
   with self.assertRaises(ValueError):construct(2,x)
 def test_wrong_types(self):
  for x in (True,False,1.0,'2',None):
   with self.assertRaises(ValueError):construct(x,2)
 def test_bad_basis(self):
  for u,v in (((0,0),(0,0)),((1,0),(1,1)),((1,0),(0,2))):
   with self.assertRaises(ValueError):construct(u=u,v=v)
 def test_bad_points(self):
  for k in construct()['points']:
   c=construct();x,y=c['points'][k];c['points'][k]=(x+1,y)
   with self.assertRaises(ValueError):verify(c)
 def test_missing_extra(self):
  c=construct();del c['points']['Q']
  with self.assertRaises(ValueError):verify(c)
  c=construct();c['points']['Z']=(0,0)
  with self.assertRaises(ValueError):verify(c)
 def test_malformed(self):
  for c in (None,[],{}, {'points':[]},{'points':None}):
   with self.assertRaises(ValueError):verify(c)
 def test_bool_coordinate(self):
  c=construct();c['points']['A']=(False,0)
  with self.assertRaises(ValueError):verify(c)
 def test_diagonal(self):
  p=construct()['points']
  self.assertEqual(area(p,'EQD'),0);self.assertEqual(area(p,'EKD'),0)
if __name__=='__main__':unittest.main()
