import unittest,copy
from geometry import *
class GeometryTests(unittest.TestCase):
 def c(self):return certificate(*EXAMPLES['simple'])
 def test_simple(self):self.assertEqual(self.c()['distance_squared'],'17')
 def test_extrema(self):self.assertEqual((self.c()['minimum_squared'],self.c()['maximum_squared']),('9','49'))
 def test_mirror(self):self.assertEqual(self.c()['mirror'],['3','-4'])
 def test_margins(self):self.assertEqual((self.c()['above_minimum'],self.c()['below_maximum']),('8','32'))
 def test_examples(self):self.assertTrue(all(verify(certificate(*v)) for v in EXAMPLES.values()))
 def test_grid(self):self.assertEqual(sum(verify(certificate(*v)) for v in grid()),504)
 def test_identity(self):
  for args in grid():
   c=certificate(*args);r=scalar(c['input']['radius']);d=scalar(c['input']['offset']);x=scalar(c['projection']);self.assertEqual(scalar(c['distance_squared']),r*r+d*d-2*d*x)
 def test_mirror_twice(self):
  c=self.c();e=certificate((0,0),5,2,(1,0),c['mirror']);self.assertEqual(e['mirror'],['3','4'])
 def test_compare(self):self.assertTrue(compare((0,0),5,2,(1,0),(-3,4),(3,4))['p_longer'])
 def test_compare_reverse(self):self.assertFalse(compare((0,0),5,2,(1,0),(3,4),(-3,4))['p_longer'])
 def test_opposite_semicircle(self):self.assertRaises(ValueError,compare,(0,0),5,2,(1,0),(3,4),(3,-4))
 def test_duplicate(self):self.assertRaises(ValueError,compare,(0,0),5,2,(1,0),(3,4),(3,4))
 def test_center(self):self.assertRaises(ValueError,certificate,(0,0),5,0,(1,0),(3,4))
 def test_boundary(self):self.assertRaises(ValueError,certificate,(0,0),5,5,(1,0),(3,4))
 def test_outside(self):self.assertRaises(ValueError,certificate,(0,0),5,6,(1,0),(3,4))
 def test_negative_radius(self):self.assertRaises(ValueError,certificate,(0,0),-5,2,(1,0),(3,4))
 def test_zero_axis(self):self.assertRaises(ValueError,certificate,(0,0),5,2,(0,0),(3,4))
 def test_nonunit(self):self.assertRaises(ValueError,certificate,(0,0),5,2,(2,0),(3,4))
 def test_extreme_rejected(self):
  for p in [(5,0),(-5,0)]:self.assertRaises(ValueError,certificate,(0,0),5,2,(1,0),p)
 def test_off_circle(self):self.assertRaises(ValueError,certificate,(0,0),5,2,(1,0),(2,4))
 def test_inexact(self):
  for x in [True,2.0,None,'1/0']:
   self.assertRaises(ValueError,certificate,(0,0),5,x,(1,0),(3,4))
 def test_tamper(self):
  for k in self.c():
   c=self.c();c[k]='tampered';self.assertFalse(verify(c))
 def test_type_sensitive(self):
  c=self.c();c['distinct_mirror']=1;self.assertFalse(verify(c));c=self.c();c['schema']=True;self.assertFalse(verify(c))
 def test_malformed(self):
  for c in [None,[],{}, {'input':{}}, {'input':None}]:self.assertFalse(verify(c))
if __name__=='__main__':unittest.main()
