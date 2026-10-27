import unittest
from copy import deepcopy
from geometry import *
from cases import *
class Tests(unittest.TestCase):
 def setUp(self):
  self.data=(point(0,4),point(-3,0),point(4,0),point(0,1));self.c=construct(*self.data)
 def test_positive(self):
  for d in positive_cases():self.assertTrue(accepted(*d,construct(*d)))
 def test_negative(self):
  for d in invalid_cases():
   with self.assertRaises(ValueError):construct(*d)
 def test_checks(self):self.assertTrue(all(self.c['checks'].values()))
 def test_E(self):self.assertEqual(self.c['E'],[[9,4],[7,4]])
 def test_factor(self):self.assertEqual(self.c['extension_factor'],[7,4])
 def test_json_roundtrip(self):self.assertTrue(accepted(*self.data,json.loads(json.dumps(self.c))))
 def test_bool_integer(self):
  c=deepcopy(self.c);c['checks']['strict_interior']=1;self.assertFalse(accepted(*self.data,c))
 def test_integer_float(self):
  c=deepcopy(self.c);c['E'][0][0]=float(c['E'][0][0]);self.assertFalse(accepted(*self.data,c))
 def test_nan(self):
  c=deepcopy(self.c);c['E'][0][0]=float('nan');self.assertFalse(accepted(*self.data,c))
 def test_tuple(self):
  c=deepcopy(self.c);c['E']=tuple(c['E']);self.assertFalse(accepted(*self.data,c))
 def test_missing(self):
  c=deepcopy(self.c);del c['checks'];self.assertFalse(accepted(*self.data,c))
 def test_extra(self):
  c=deepcopy(self.c);c['extra']=None;self.assertFalse(accepted(*self.data,c))
 def test_wrong_input(self):self.assertFalse(accepted(*self.data[:3],point(0,2),self.c))
 def test_tamper_coordinate(self):
  c=deepcopy(self.c);c['E'][0][0]+=1;self.assertFalse(accepted(*self.data,c))
 def test_tamper_factor(self):
  c=deepcopy(self.c);c['extension_factor'][0]+=1;self.assertFalse(accepted(*self.data,c))
 def test_tamper_squared(self):
  c=deepcopy(self.c);c['squared_lengths']['AB'][0]+=1;self.assertFalse(accepted(*self.data,c))
 def test_false_check(self):
  c=deepcopy(self.c);c['checks']['outer_gt_inner']=False;self.assertFalse(accepted(*self.data,c))
 def test_reflection(self):
  d=tuple(point(x,-y) for x,y in self.data);self.assertTrue(accepted(*d,construct(*d)))
 def test_translation(self):
  d=tuple(add(p,point(100,-50)) for p in self.data);self.assertTrue(accepted(*d,construct(*d)))
 def test_scaling(self):
  d=tuple(mul(Q(7,3),p) for p in self.data);self.assertTrue(accepted(*d,construct(*d)))
 def test_near_boundary(self):
  A,B,C=self.data[:3];D=mul(Q(1,10**30),add(A,mul(10**30-1,mul(Q(1,2),add(B,C)))))
  self.assertTrue(accepted(A,B,C,D,construct(A,B,C,D)))
 def test_length_zero(self):self.assertEqual(sum_compare(0,0,0,0),0)
 def test_length_rational(self):self.assertEqual(sum_compare(1,4,9,0),0)
 def test_length_irrational_equal(self):self.assertEqual(sum_compare(2,8,18,0),0)
 def test_length_swapped(self):self.assertEqual(sum_compare(2,3,3,2),0)
 def test_length_irrational_order(self):self.assertEqual(sum_compare(2,3,1,4),1)
 def test_length_reverse(self):self.assertEqual(sum_compare(1,4,2,3),-1)
 def test_length_tiny_gap(self):self.assertEqual(sum_compare(Q(1)+Q(1,10**40),0,1,0),1)
 def test_length_invalid(self):
  with self.assertRaises(ValueError):sum_compare(-1,0,0,0)
 def test_angle_equal(self):self.assertEqual(angle_compare(point(1,0),point(0,1),point(2,0),point(0,3)),0)
 def test_angle_acute_obtuse(self):self.assertEqual(angle_compare(point(1,0),point(1,1),point(1,0),point(-1,1)),-1)
 def test_angle_obtuse(self):self.assertEqual(angle_compare(point(1,0),point(-2,1),point(1,0),point(-1,2)),1)
 def test_zero_ray(self):
  with self.assertRaises(ValueError):angle_compare(point(0,0),point(1,0),point(1,0),point(0,1))
 def test_squared_grid(self):
  for a in range(6):
   for b in range(6):
    for c in range(6):
     for d in range(6):self.assertEqual(sum_compare(a*a,b*b,c*c,d*d),sign(a+b-c-d))
if __name__=='__main__':unittest.main(verbosity=2)
