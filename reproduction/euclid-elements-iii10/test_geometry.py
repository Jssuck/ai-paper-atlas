import unittest
from fractions import Fraction as F
from geometry import *
class Tests(unittest.TestCase):
 def test_external_disjoint(self):self.assertEqual(classify((0,0),1,(3,0),1)['count'],0)
 def test_internal_disjoint(self):self.assertEqual(classify((0,0),25,(1,0),1)['count'],0)
 def test_external_tangent(self):self.assertEqual(rational_intersections((0,0),1,(2,0),1),((F(1),F(0)),))
 def test_internal_tangent(self):self.assertEqual(rational_intersections((0,0),25,(3,0),4),((F(5),F(0)),))
 def test_two_points(self):self.assertEqual(rational_intersections((0,0),25,(6,0),25),((F(3),F(4)),(F(3),F(-4))))
 def test_vertical(self):self.assertEqual(set(rational_intersections((0,0),25,(0,6),25)),{(F(4),F(3)),(F(-4),F(3))})
 def test_concentric(self):self.assertEqual(classify((1,2),1,(1,2),4)['kind'],'concentric-disjoint')
 def test_coincident(self):self.assertIsNone(classify((0,0),1,(0,0),1)['count'])
 def test_irrational(self):self.assertEqual(classify((0,0),1,(1,0),1)['count'],2);self.assertIsNone(rational_intersections((0,0),1,(1,0),1))
 def test_near_tangent(self):
  for d,n in [('1999999999999999999/1000000000000000000',2),('2000000000000000001/1000000000000000000',0)]:self.assertEqual(classify((0,0),1,(d,0),1)['count'],n)
 def test_small_scale(self):self.assertEqual(classify((0,0),'1/100000000000000000000',(F(1,10**10),0),'1/100000000000000000000')['count'],2)
 def test_three_points(self):self.assertTrue(same_circle_from_three([(5,0),(0,5),(-5,0)],(0,0),25,(0,0),25)['equal_centers'])
 def test_false_common(self):
  with self.assertRaises(ValueError):same_circle_from_three([(5,0),(0,5),(-5,0)],(0,0),25,(1,0),25)
 def test_collinear(self):
  with self.assertRaises(ValueError):same_circle_from_three([(0,0),(1,0),(2,0)],(0,0),1,(0,0),1)
 def test_duplicates(self):
  with self.assertRaises(ValueError):same_circle_from_three([(1,0),(1,0),(0,1)],(0,0),1,(0,0),1)
 def test_nonpositive(self):
  for r in [0,-1]:
   with self.assertRaises(ValueError):classify((0,0),r,(1,0),1)
 def test_bad_numbers(self):
  for v in [True,1.0,float('nan'),'1/0','bad',None]:
   with self.assertRaises(ValueError):classify((v,0),1,(1,0),1)
 def test_bad_shapes(self):
  for p in [[],[1],[1,2,3],'12',None]:
   with self.assertRaises(ValueError):classify(p,1,(1,0),1)
 def test_wrong_point_count(self):
  with self.assertRaises(ValueError):same_circle_from_three([(0,0)],(0,0),1,(0,0),1)
 def test_symmetry(self):
  for d in range(1,9):self.assertEqual(classify((0,0),25,(d,0),4)['count'],classify((d,0),4,(0,0),25)['count'])
 def test_family_600(self):
  count=0
  for x in range(-2,3):
   for y in range(-2,3):
    for s in [F(1,3),F(1),F(3,2),F(7)]:
     for vx,vy in [(6,0),(0,6),(-6,0),(0,-6),(F(18,5),F(24,5)),(F(-24,5),F(18,5))]:
      a=(F(x),F(y));b=(x+s*vx,y+s*vy);R=25*s*s
      pts=rational_intersections(a,R,b,R)
      self.assertEqual(len(set(pts)),2)
      for p in pts:self.assertEqual(sqdist(p,a),R);self.assertEqual(sqdist(p,b),R)
      count+=1
  self.assertEqual(count,600)
if __name__=='__main__':unittest.main()
