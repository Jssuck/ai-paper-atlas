import unittest,copy,json
from geometry import *
from cases import *
class Tests(unittest.TestCase):
 def setUp(self):self.d=copy.deepcopy(EXAMPLE);self.c=make_certificate(self.d)
 def test_example(self):self.assertTrue(verify_certificate(self.d,self.c))
 def test_lengths(self):self.assertEqual(self.c['opposite_sides_squared'],{'AB':'16','CD':'16','AC':'10','BD':'10'})
 def test_area(self):self.assertEqual(self.c['area'],{'parallelogram':'12','ABC':'6','DCB':'6'})
 def test_alternate_one(self):self.assertEqual(self.c['alternate_angles']['ABC'],self.c['alternate_angles']['BCD'])
 def test_alternate_two(self):self.assertEqual(self.c['alternate_angles']['ACB'],self.c['alternate_angles']['CBD'])
 def test_opposite_one(self):self.assertEqual(self.c['opposite_angles']['BAC'],self.c['opposite_angles']['CDB'])
 def test_opposite_two(self):self.assertEqual(self.c['opposite_angles']['ABD'],self.c['opposite_angles']['ACD'])
 def test_side(self):self.assertLess(F(self.c['triangles']['BC_side_A'])*F(self.c['triangles']['BC_side_D']),0)
 def test_all_positive(self):
  for d in positives():
   c=make_certificate(d);self.assertTrue(verify_certificate(d,c));self.assertEqual(c['triangles']['ABC_squared'],c['triangles']['DCB_squared']);self.assertEqual(c['triangles']['ABC_twice_area'],c['triangles']['DCB_twice_area'])
 def test_all_negative(self):
  for d in negatives():
   with self.assertRaises(ValueError):make_certificate(d)
 def test_bool(self):
  self.d['A'][0]=False
  with self.assertRaises(ValueError):make_certificate(self.d)
 def test_float(self):
  self.d['A'][0]=0.0
  with self.assertRaises(ValueError):make_certificate(self.d)
 def test_nan(self):
  self.d['A'][0]=float('nan')
  with self.assertRaises(ValueError):make_certificate(self.d)
 def test_fraction(self):
  self.d['A'][0]=F(0)
  with self.assertRaises(ValueError):make_certificate(self.d)
 def test_tuple(self):
  self.d['A']=(0,0)
  with self.assertRaises(ValueError):make_certificate(self.d)
 def test_missing(self):
  del self.d['A']
  with self.assertRaises(ValueError):make_certificate(self.d)
 def test_extra(self):
  self.d['E']=[0,0]
  with self.assertRaises(ValueError):make_certificate(self.d)
 def test_bad_string(self):
  for x in ['0/1','01','1/0','nan',' 0','']:
   self.d['A'][0]=x
   with self.assertRaises(ValueError):make_certificate(self.d)
 def test_input_binding(self):
  d={k:[v[0]+1,v[1]+2] for k,v in self.d.items()};self.assertFalse(verify_certificate(d,self.c))
 def test_cert_bool(self):self.c['area']['ABC']=True;self.assertFalse(verify_certificate(self.d,self.c))
 def test_cert_int(self):self.c['area']['ABC']=6;self.assertFalse(verify_certificate(self.d,self.c))
 def test_cert_extra(self):self.c['extra']='x';self.assertFalse(verify_certificate(self.d,self.c))
 def test_cert_missing(self):del self.c['area'];self.assertFalse(verify_certificate(self.d,self.c))
 def test_cert_tamper(self):self.c['area']['ABC']='7';self.assertFalse(verify_certificate(self.d,self.c))
 def test_round_trip(self):self.assertTrue(verify_certificate(json.loads(json.dumps(self.d)),json.loads(json.dumps(self.c))))
 def test_reflection(self):d={k:[v[0],-v[1]] for k,v in self.d.items()};self.assertEqual(make_certificate(d)['area'],self.c['area'])
 def test_scale(self):d={k:[3*v[0],3*v[1]] for k,v in self.d.items()};self.assertEqual(make_certificate(d)['area']['ABC'],'54')
if __name__=='__main__':unittest.main(verbosity=2)
