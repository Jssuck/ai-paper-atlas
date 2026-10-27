import unittest,copy,json
from fractions import Fraction as Q
from geometry import *
from cases import positive_cases,invalid_cases
class Tests(unittest.TestCase):
 def cert(self): return build_certificate([0,0],[3,0],[0,4])
 def test_example(self): self.assertEqual(self.cert()['observation']['side_relation'],1)
 def test_angle_independent(self): self.assertEqual(angle_compare((1,0),(0,1),(1,0),(1,1)),1)
 def test_acute(self): self.assertEqual(angle_compare((1,0),(2,1),(1,0),(1,1)),-1)
 def test_obtuse(self): self.assertEqual(angle_compare((1,0),(-2,1),(1,0),(-1,1)),1)
 def test_right(self): self.assertEqual(angle_compare((1,0),(0,3),(2,0),(0,1)),0)
 def test_reflected(self): self.assertEqual(inspect_triangle([0,0],[3,0],[0,-4])['angle_relation'],1)
 def test_equal(self): self.assertEqual(inspect_triangle([0,0],[3,0],[0,3])['angle_relation'],0)
 def test_reverse(self): self.assertEqual(inspect_triangle([0,0],[4,0],[0,3])['angle_relation'],-1)
 def test_obtuse_triangle(self): self.assertEqual(inspect_triangle([0,0],[2,0],[4,1])['angle_relation'],1)
 def test_grid(self):
  for x in range(-4,5):
   for y in range(-4,5):
    if y:
     r=inspect_triangle([0,0],[2,0],[x,y]);self.assertEqual(r['angle_relation'],r['side_relation']);self.assertEqual(r['identity_residual'],'0')
 def test_positive(self):
  for case in positive_cases():self.assertTrue(verify_certificate(*case,build_certificate(*case)))
 def test_negative(self):
  for case in invalid_cases():
   with self.assertRaises(ValueError): build_certificate(*case)
 def test_rational(self): self.assertEqual(inspect_triangle(['1/2',0],['3/2',0],['1/2','5/2'])['side_relation'],1)
 def test_roundtrip(self): self.assertTrue(verify_certificate([0,0],[3,0],[0,4],json.loads(json.dumps(self.cert()))))
 def test_binding(self): self.assertFalse(verify_certificate([0,0],[3,0],[0,5],self.cert()))
 def test_schema_bool(self):
  c=self.cert();c['schema']=True;self.assertFalse(verify_certificate([0,0],[3,0],[0,4],c))
 def test_schema_float(self):
  c=self.cert();c['schema']=1.0;self.assertFalse(verify_certificate([0,0],[3,0],[0,4],c))
 def test_nested_bool(self):
  c=self.cert();c['observation']['angle_relation']=True;self.assertFalse(verify_certificate([0,0],[3,0],[0,4],c))
 def test_extra(self):
  c=self.cert();c['extra']=1;self.assertFalse(verify_certificate([0,0],[3,0],[0,4],c))
 def test_missing(self):
  c=self.cert();del c['remaining'];self.assertFalse(verify_certificate([0,0],[3,0],[0,4],c))
 def test_branch_tamper(self):
  c=self.cert();c['excluded'][0]['prediction']='beta > gamma';self.assertFalse(verify_certificate([0,0],[3,0],[0,4],c))
 def test_tuple(self):
  c=self.cert();c['remaining']=('greater',);self.assertFalse(verify_certificate([0,0],[3,0],[0,4],c))
 def test_non_json(self): self.assertFalse(verify_certificate([0,0],[3,0],[0,4],set()))
 def test_nan(self):
  c=self.cert();c['schema']=float('nan');self.assertFalse(verify_certificate([0,0],[3,0],[0,4],c))
 def test_total(self): self.assertEqual(infer_side(1),['greater'])
 def test_no_total(self): self.assertEqual(infer_side(1,total=False),['greater','incomparable'])
 def test_no_equal(self): self.assertEqual(infer_side(1,equal_implies_equal=False),['equal','greater'])
 def test_no_reverse(self): self.assertEqual(infer_side(1,less_implies_less=False),['less','greater'])
 def test_relation_bool(self):
  with self.assertRaises(ValueError):infer_side(True)
 def test_flag_int(self):
  with self.assertRaises(ValueError):infer_side(1,total=1)
 def test_zero_angle(self):
  with self.assertRaises(ValueError):angle_compare((1,0),(2,0),(1,0),(0,1))
 def test_straight_angle(self):
  with self.assertRaises(ValueError):angle_compare((1,0),(-2,0),(1,0),(0,1))
 def test_scaling(self):
  self.assertEqual(angle_compare((2,0),(4,2),(3,0),(3,3)),-1)
 def test_translation(self):
  self.assertEqual(inspect_triangle([100,100],[103,100],[100,104])['angle_relation'],1)
if __name__=='__main__': unittest.main(verbosity=2)
