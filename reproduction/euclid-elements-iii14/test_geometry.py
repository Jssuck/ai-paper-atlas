import unittest
from geometry import *
class GeometryTests(unittest.TestCase):
 def setUp(self):self.c=Circle((0,0),5)
 def test_equal(self):self.assertTrue(compare(self.c,(-4,3),(4,3),(-4,-3),(4,-3))['equal_chords'])
 def test_unequal(self):self.assertFalse(compare(self.c,(-4,3),(4,3),(-3,4),(3,4))['equal_chords'])
 def test_diameters(self):self.assertTrue(compare(self.c,(-5,0),(5,0),(0,-5),(0,5))['equal_distances'])
 def test_one_diameter(self):self.assertFalse(compare(self.c,(-5,0),(5,0),(-4,3),(4,3))['equal_distances'])
 def test_foot(self):self.assertEqual(chord(self.c,(-4,3),(4,3))['foot'],(0,3))
 def test_parameter(self):self.assertEqual(chord(self.c,(-4,3),(4,3))['projection_parameter'],F(1,2))
 def test_pythagoras(self):q=chord(self.c,(-4,3),(4,3));self.assertEqual(q['half_length2']+q['distance2'],25)
 def test_full_length(self):self.assertEqual(chord(self.c,(-4,3),(4,3))['length2'],64)
 def test_zero_distance(self):self.assertEqual(chord(self.c,(-5,0),(5,0))['distance2'],0)
 def test_reverse(self):self.assertEqual(chord(self.c,(-4,3),(4,3))['foot'],chord(self.c,(4,3),(-4,3))['foot'])
 def test_translated(self):self.assertEqual(chord(Circle((2,-7),5),(-2,-4),(6,-4))['distance2'],9)
 def test_reflected(self):self.assertEqual(chord(self.c,(-4,-3),(4,-3))['distance2'],9)
 def test_scaled(self):self.assertEqual(chord(Circle((0,0),10),(-8,6),(8,6))['length2'],256)
 def test_fraction(self):self.assertEqual(chord(Circle((0,0),F(5,2)),(-2,F(3,2)),(2,F(3,2)))['distance2'],F(9,4))
 def test_validate(self):self.assertTrue(validate(self.c,chord(self.c,(-4,3),(4,3))))
 def test_tamper(self):q=chord(self.c,(-4,3),(4,3));q['distance2']=8;self.assertFalse(validate(self.c,q))
 def test_missing(self):self.assertFalse(validate(self.c,{}))
 def test_extra(self):q=chord(self.c,(-4,3),(4,3));q['extra']=1;self.assertFalse(validate(self.c,q))
 def test_off_circle(self):self.assertRaises(ValueError,chord,self.c,(0,0),(5,0))
 def test_equal_endpoints(self):self.assertRaises(ValueError,chord,self.c,(5,0),(5,0))
 def test_zero_radius(self):self.assertRaises(ValueError,Circle,(0,0),0)
 def test_negative_radius(self):self.assertRaises(ValueError,Circle,(0,0),-5)
 def test_bool(self):self.assertRaises(ValueError,Circle,(False,0),5)
 def test_float(self):self.assertRaises(ValueError,Circle,(0,0),5.0)
 def test_bad_point(self):self.assertRaises(ValueError,Circle,(0,0,0),5)
 def test_cross_circle_counterexample(self):
  # equal chord length but different distances, because radii differ
  a=chord(Circle((0,0),5),(-4,3),(4,3));b=chord(Circle((0,0),4),(-4,0),(4,0))
  self.assertEqual(a['length2'],b['length2']);self.assertNotEqual(a['distance2'],b['distance2'])
 def test_equal_circle_translation(self):
  a=chord(self.c,(-4,3),(4,3));b=chord(Circle((9,2),5),(5,5),(13,5))
  self.assertEqual((a['length2'],a['distance2']),(b['length2'],b['distance2']))
 def test_grid(self):
  count=0;pairs=0
  for r in (F(1),F(5),F(7,3)):
   for center in ((0,0),(2,-3),(-7,4)):
    c=Circle(center,r);points=[rational_circle_point(c,F(t,3)) for t in range(-4,5)]
    cert=[]
    for i in range(9):
     for j in range(i+1,9):
      q=chord(c,points[i],points[j]);count+=1;cert.append(q)
      self.assertEqual(q['projection_parameter'],F(1,2));self.assertTrue(validate(c,q))
      self.assertEqual(q['half_length2']+q['distance2'],r*r)
      self.assertEqual(q['length2'],4*q['half_length2'])
    for a in cert:
     for b in cert:
      pairs+=1;self.assertEqual(a['length2']==b['length2'],a['distance2']==b['distance2'])
  print('grid:',count,'chords;',pairs,'ordered comparisons')
if __name__=='__main__':unittest.main()
