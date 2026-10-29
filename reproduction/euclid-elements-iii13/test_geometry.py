import unittest
from fractions import Fraction as Q
from geometry import *

class TestGeometry(unittest.TestCase):
 def setUp(self):self.a=Circle((0,0),5);self.b=Circle((8,0),3);self.i=Circle((2,0),3)
 def test_external(self):self.assertEqual(contact_certificate(self.a,self.b,(5,0),'external')['point'],(5,0))
 def test_internal(self):self.assertTrue(same_contact(self.a,self.i,(5,0),(5,0),'internal'))
 def test_swap(self):self.assertEqual(contact_certificate(self.i,self.a,(5,0),'internal')['unique_candidate'],(5,0))
 def test_equal_external(self):self.assertTrue(same_contact(Circle((0,0),2),Circle((4,0),2),(2,0),(2,0),'external'))
 def test_coincident(self):self.assertEqual(relation(self.a,self.a),'coincident')
 def test_coincident_rejected(self):
  with self.assertRaises(ValueError):contact_certificate(self.a,self.a,(5,0),'internal')
 def test_concentric(self):self.assertEqual(relation(self.a,Circle((0,0),3)),'concentric_distinct')
 def test_strict_containment(self):self.assertEqual(relation(self.a,Circle((1,0),3)),'strict_containment')
 def test_separate(self):self.assertEqual(relation(self.a,Circle((9,0),3)),'separate')
 def test_intersections(self):self.assertEqual(relation(self.a,Circle((6,0),5)),'two_intersections')
 def test_chord(self):self.assertEqual(chord_midpoint_certificate(self.a,Circle((6,0),5),(3,4),(3,-4)),{'midpoint':(Q(3),Q(0)),'strict_squared_gap':Q(16)})
 def test_chord_coincident_valid(self):self.assertEqual(chord_midpoint_certificate(self.a,self.a,(3,4),(3,-4))['strict_squared_gap'],16)
 def test_two_points_not_external(self):
  with self.assertRaises(ValueError):contact_certificate(self.a,Circle((6,0),5),(3,4),'external')
 def test_two_points_not_internal(self):
  with self.assertRaises(ValueError):contact_certificate(self.a,Circle((6,0),5),(3,4),'internal')
 def test_wrong_witness(self):
  with self.assertRaises(ValueError):contact_certificate(self.a,self.b,(3,4),'external')
 def test_duplicate_chord(self):
  with self.assertRaises(ValueError):chord_midpoint_certificate(self.a,self.a,(3,4),(3,4))
 def test_wrong_chord(self):
  with self.assertRaises(ValueError):chord_midpoint_certificate(self.a,self.b,(3,4),(3,-4))
 def test_kind(self):
  with self.assertRaises(ValueError):contact_certificate(self.a,self.b,(5,0),'tangent')
 def test_zero(self):
  with self.assertRaises(ValueError):Circle((0,0),0)
 def test_negative(self):
  with self.assertRaises(ValueError):Circle((0,0),-1)
 def test_float_radius(self):
  with self.assertRaises(TypeError):Circle((0,0),1.0)
 def test_bool_radius(self):
  with self.assertRaises(TypeError):Circle((0,0),True)
 def test_bool_coordinate(self):
  with self.assertRaises(TypeError):Circle((False,0),1)
 def test_dimension(self):
  with self.assertRaises(TypeError):Circle((0,0,0),1)
 def test_bad_circle(self):
  with self.assertRaises(TypeError):relation(None,self.a)
 def test_tiny_gap(self):self.assertEqual(relation(Circle((0,0),1),Circle((2+Q(1,10**50),0),1)),'separate')
 def test_tiny_overlap(self):self.assertEqual(relation(Circle((0,0),1),Circle((2-Q(1,10**50),0),1)),'two_intersections')
 def test_grid(self):
  count=0
  for o in [(0,0),(2,-3),(Q(1,7),Q(-2,5))]:
   for u in [(1,0),(-1,0),(0,1),(0,-1),(Q(3,5),Q(4,5)),(Q(-5,13),Q(12,13))]:
    for r in [Q(1,3),Q(1),Q(2),Q(7,3)]:
     for delta in [Q(1,5),Q(1),Q(3)]:
      R=r+delta;a=Circle(o,R);t=tuple(x+R*v for x,v in zip(o,u))
      for kind,d in [('external',R+r),('internal',R-r)]:
       b=Circle(tuple(x+d*v for x,v in zip(o,u)),r)
       for x,y in [(a,b),(b,a)]:self.assertTrue(same_contact(x,y,t,t,kind));count+=1
  self.assertEqual(count,864)
  print('grid: 432 contact configurations, 864 circle-order certificates')
if __name__=='__main__':unittest.main()
