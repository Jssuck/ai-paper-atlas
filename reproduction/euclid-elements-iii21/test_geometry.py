import unittest
from fractions import Fraction as F
from geometry import certificate,verify,CASES,grid

class GeometryTests(unittest.TestCase):
 def test_major(self):
  c=certificate(*CASES['same_major_segment']); self.assertEqual(c['cotangents'],(F(4,3),F(4,3)));self.assertTrue(c['equal'])
 def test_minor(self):
  c=certificate(*CASES['same_minor_segment']);self.assertEqual(c['cotangents'],(F(-4,3),F(-4,3)))
 def test_opposite(self):
  c=certificate(*CASES['opposite_not_equal']);self.assertFalse(c['equal']);self.assertEqual(c['relation'],'supplementary')
 def test_diameter(self):
  c=certificate(*CASES['diameter_exception']);self.assertTrue(c['equal']);self.assertTrue(c['diameter']);self.assertEqual(c['cotangents'],(0,0))
 def test_same_vertex(self):
  a=list(CASES['same_major_segment']);a[-1]=a[-2];self.assertTrue(certificate(*a)['equal'])
 def test_translation_scale(self):
  a=CASES['same_minor_segment']; transform=lambda p:tuple(3*x+y for x,y in zip(p,(7,-11)))
  b=(transform(a[0]),9*a[1],*(transform(p) for p in a[2:]));self.assertEqual(certificate(*a),certificate(*b))
 def test_chord_reversal(self):
  a=list(CASES['opposite_not_equal']);c=certificate(*a);a[2],a[3]=a[3],a[2];d=certificate(*a);self.assertEqual(d['sides'],tuple(-s for s in c['sides']));self.assertEqual(d['cotangents'],c['cotangents'])
 def invalid(self,index,value):
  a=list(CASES['same_major_segment']);a[index]=value
  with self.assertRaises(ValueError): certificate(*a)
 def test_offcircle(self):self.invalid(4,(0,0))
 def test_other_radius(self):self.invalid(1,26)
 def test_zero_radius(self):self.invalid(1,0)
 def test_negative_radius(self):self.invalid(1,-25)
 def test_duplicate_chord(self):self.invalid(3,(-3,4))
 def test_endpoint_vertex(self):self.invalid(4,(3,4))
 def test_float(self):self.invalid(1,25.0)
 def test_bool(self):self.invalid(1,True)
 def test_badpoint(self):self.invalid(4,(0,5,0))
 def test_tamper(self):
  a=CASES['same_minor_segment'];c=certificate(*a)
  for key in c:
   d=dict(c);d[key]=None;self.assertFalse(verify(*a,d))
  d=dict(c);d['extra']=0;self.assertFalse(verify(*a,d))
  d=dict(c);d['sides']=tuple(bool(s) for s in d['sides']);self.assertFalse(verify(*a,d))
 def test_grid(self):
  c=grid();self.assertEqual(c['configurations'],1260);self.assertGreater(c['same_side'],0);self.assertGreater(c['opposite_side'],0)

if __name__=='__main__':unittest.main(verbosity=2)
