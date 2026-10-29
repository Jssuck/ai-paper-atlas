import unittest,copy,json
from fractions import Fraction as F
from geometry import *
class TestGeometry(unittest.TestCase):
 def test_external(self):self.assertEqual(certificate(*EXAMPLES['external'])['contact'],['2','0'])
 def test_internal(self):self.assertEqual(certificate(*EXAMPLES['internal'])['contact'],['5','0'])
 def test_swapped(self):self.assertEqual(certificate(*EXAMPLES['internal_swapped'])['contact'],['5','0'])
 def test_oblique_external(self):self.assertTrue(verify(certificate(*EXAMPLES['oblique_external'])))
 def test_oblique_internal(self):self.assertTrue(verify(certificate(*EXAMPLES['oblique_internal'])))
 def test_grid(self):
  rows=list(grid());self.assertEqual(len(rows),600)
  for a in rows:
   c=certificate(*a);self.assertTrue(verify(c));t=point(c['contact']);o,r=circle(a[0],a[1]);p,s=circle(a[2],a[3]);self.assertEqual(d2(t,o),r*r);self.assertEqual(d2(t,p),s*s)
 def test_coincident(self):self.assertEqual(relation((0,0),2,(0,0),2),'coincident')
 def test_concentric(self):self.assertEqual(relation((0,0),2,(0,0),3),'concentric_disjoint')
 def test_crossing(self):self.assertEqual(relation((0,0),5,(6,0),5),'two_intersections')
 def test_external_disjoint(self):self.assertEqual(relation((0,0),1,(3,0),1),'external_disjoint')
 def test_containment(self):self.assertEqual(relation((0,0),5,(1,0),1),'strict_containment')
 def test_reject_non_tangent(self):
  for a in [((0,0),2,(0,0),2),((0,0),2,(0,0),3),((0,0),5,(6,0),5),((0,0),1,(3,0),1),((0,0),5,(1,0),1)]:
   with self.assertRaises(ValueError):certificate(*a)
 def test_bool(self):
  for x in (True,False):
   with self.assertRaises(ValueError):certificate((0,0),x,(5,0),3)
 def test_float(self):
  with self.assertRaises(ValueError):certificate((0.0,0),2,(5,0),3)
 def test_zero_radius(self):
  with self.assertRaises(ValueError):certificate((0,0),0,(3,0),3)
 def test_negative_radius(self):
  with self.assertRaises(ValueError):certificate((0,0),-2,(5,0),3)
 def test_bad_rational(self):
  for x in ('1/0','nan',None,[],{}):
   with self.assertRaises(ValueError):q(x)
 def test_bad_point(self):
  for p in ((0,), (0,0,0), '00',None):
   with self.assertRaises(ValueError):certificate(p,2,(5,0),3)
 def test_tamper_each_field(self):
  c=certificate(*EXAMPLES['external'])
  for key in c:
   b=copy.deepcopy(c);b[key]='tampered';self.assertFalse(verify(b))
 def test_bool_integer(self):
  c=certificate(*EXAMPLES['external']);c['same_center']=0;self.assertFalse(verify(c));c=certificate(*EXAMPLES['external']);c['unique_contact']=1;self.assertFalse(verify(c))
 def test_extra_missing(self):
  c=certificate(*EXAMPLES['external']);c['extra']=True;self.assertFalse(verify(c));del c['extra'];del c['schema'];self.assertFalse(verify(c))
 def test_malformed(self):
  for c in (None,[],{},True,1,'x'):self.assertFalse(verify(c))
 def test_radical_line(self):
  for a in grid():
   c=certificate(*a);n=point(c['radical_normal']);t=point(c['contact']);self.assertEqual(sum(x*y for x,y in zip(n,t)),q(c['radical_offset']))
 def test_json_roundtrip(self):
  for a in EXAMPLES.values():self.assertTrue(verify(json.loads(json.dumps(certificate(*a)))))
if __name__=='__main__':unittest.main()
