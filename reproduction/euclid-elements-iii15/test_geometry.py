import unittest
from geometry import *
class GeometryTests(unittest.TestCase):
 def setUp(self):self.c=Circle((0,0),5)
 def test_longer_nearer(self):
  x=compare(self.c,(-4,3),(4,3),(-3,4),(3,4));self.assertEqual((x['length_order'],x['distance_order']),(1,-1))
 def test_shorter_farther(self):
  x=compare(self.c,(-3,4),(3,4),(-4,3),(4,3));self.assertEqual((x['length_order'],x['distance_order']),(-1,1))
 def test_equal_tie(self):
  x=compare(self.c,(-4,3),(4,3),(3,-4),(3,4));self.assertEqual((x['length_order'],x['distance_order']),(0,0))
 def test_diameter_strict(self):
  x=compare(self.c,(-5,0),(5,0),(-4,3),(4,3));self.assertEqual(x['length_order'],1);self.assertTrue(x['order_reversal_holds'])
 def test_diameters_tie(self):self.assertEqual(compare(self.c,(-5,0),(5,0),(0,-5),(0,5))['length_order'],0)
 def test_foot(self):self.assertEqual(chord(self.c,(-4,3),(4,3))['foot'],(0,3))
 def test_midpoint(self):self.assertEqual(chord(self.c,(-4,3),(4,3))['projection_parameter'],F(1,2))
 def test_pythagoras(self):q=chord(self.c,(-4,3),(4,3));self.assertEqual(q['half_length2']+q['distance2'],25)
 def test_diameter_bound(self):self.assertLess(chord(self.c,(-4,3),(4,3))['length2'],100)
 def test_zero_distance(self):self.assertEqual(chord(self.c,(-5,0),(5,0))['distance2'],0)
 def test_reverse(self):self.assertEqual(chord(self.c,(-4,3),(4,3))['foot'],chord(self.c,(4,3),(-4,3))['foot'])
 def test_translation(self):self.assertEqual(chord(Circle((2,-7),5),(-2,-4),(6,-4))['distance2'],9)
 def test_reflection(self):self.assertEqual(chord(self.c,(-4,-3),(4,-3))['distance2'],9)
 def test_scaling(self):self.assertEqual(chord(Circle((0,0),10),(-8,6),(8,6))['length2'],256)
 def test_fraction(self):self.assertEqual(chord(Circle((0,0),F(5,2)),(-2,F(3,2)),(2,F(3,2)))['distance2'],F(9,4))
 def test_validate(self):self.assertTrue(validate(self.c,chord(self.c,(-4,3),(4,3))))
 def test_tamper(self):q=chord(self.c,(-4,3),(4,3));q['distance2']=F(8);self.assertFalse(validate(self.c,q))
 def test_bool_tamper(self):q=chord(self.c,(-5,0),(5,0));q['distance2']=False;self.assertFalse(validate(self.c,q))
 def test_missing(self):self.assertFalse(validate(self.c,{}))
 def test_extra(self):q=chord(self.c,(-4,3),(4,3));q['extra']=1;self.assertFalse(validate(self.c,q))
 def test_off_circle(self):self.assertRaises(ValueError,chord,self.c,(0,0),(5,0))
 def test_equal_endpoints(self):self.assertRaises(ValueError,chord,self.c,(5,0),(5,0))
 def test_zero_radius(self):self.assertRaises(ValueError,Circle,(0,0),0)
 def test_negative_radius(self):self.assertRaises(ValueError,Circle,(0,0),-5)
 def test_bool(self):self.assertRaises(ValueError,Circle,(False,0),5)
 def test_float(self):self.assertRaises(ValueError,Circle,(0,0),5.0)
 def test_bad_point(self):self.assertRaises(ValueError,Circle,(0,0,0),5)
 def test_different_radii_counterexample(self):
  a=chord(self.c,(-4,3),(4,3));b=chord(Circle((0,0),1),(-1,0),(1,0))
  self.assertGreater(a['length2'],b['length2']);self.assertGreater(a['distance2'],b['distance2'])
 def test_grid(self):
  count=pairs=diameters=0
  for r in (F(1),F(5),F(7,3)):
   for center in ((0,0),(2,-3),(-7,4)):
    c=Circle(center,r);points=[rational_circle_point(c,F(t,2)) for t in range(-4,5)]+[add(c.center,(-r,F(0)))];cert=[]
    for i in range(len(points)):
     for j in range(i+1,len(points)):
      q=chord(c,points[i],points[j]);count+=1;cert.append(q);diameters+=q['diameter']
      self.assertEqual(q['projection_parameter'],F(1,2));self.assertTrue(validate(c,q))
      self.assertEqual(q['half_length2']+q['distance2'],r*r)
      self.assertLessEqual(q['length2'],4*r*r)
      self.assertEqual(q['length2']==4*r*r,q['diameter'])
    for a in cert:
     for b in cert:
      pairs+=1;self.assertEqual(sign(a['length2']-b['length2']),-sign(a['distance2']-b['distance2']))
  print('grid:',count,'chords;',pairs,'ordered comparisons;',diameters,'diameters')
if __name__=='__main__':unittest.main()
