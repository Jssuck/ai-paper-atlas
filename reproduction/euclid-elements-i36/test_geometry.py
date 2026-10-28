import unittest,copy,json
from fractions import Fraction as F
from geometry import *
from cases import *
class Tests(unittest.TestCase):
 def test_positive_family(self):
  for d in positives():
   c=make_certificate(d);self.assertTrue(verify_certificate(d,c));self.assertEqual(len(set(c['area'].values())),1)
 def test_negative_geometry(self):
  for d in negatives():
   with self.assertRaises(ValueError):make_certificate(d)
 def test_cases(self):
  for t,case in [(0,'identical'),('1/2','overlapping'),(1,'touching'),(2,'separated'),(-2,'separated')]:
   c=make_certificate(build(t,t));self.assertEqual(c['bridge']['upper_case'],case);self.assertEqual(c['bridge']['lower_case'],case)
 def test_example(self):
  c=make_certificate(EXAMPLE);self.assertEqual(c['area'],dict(ABCD='12',EFGH='12',EBCH='12'));self.assertEqual(c['bridge']['BE_CH_cross'],'0')
 def test_rebinding(self):
  c=make_certificate(EXAMPLE);d={k:[x+1 for x in v] for k,v in EXAMPLE.items()};self.assertFalse(verify_certificate(d,c))
 def test_json_roundtrip(self):self.assertTrue(verify_certificate(EXAMPLE,json.loads(json.dumps(make_certificate(EXAMPLE)))))
 def test_extra_cert(self):
  c=make_certificate(EXAMPLE);c['extra']='x';self.assertFalse(verify_certificate(EXAMPLE,c))
 def test_missing_cert(self):
  c=make_certificate(EXAMPLE);del c['input'];self.assertFalse(verify_certificate(EXAMPLE,c))
 def test_cut_tamper(self):
  c=make_certificate(EXAMPLE);c['bridge']['first_I35_shared_base']='FG';self.assertFalse(verify_certificate(EXAMPLE,c))
 def test_coordinate_tamper(self):
  c=make_certificate(EXAMPLE);c['input']['A'][0]='1';self.assertFalse(verify_certificate(EXAMPLE,c))
 def test_extra_input(self):
  d=copy.deepcopy(EXAMPLE);d['X']=[1,2]
  with self.assertRaises(ValueError):make_certificate(d)
 def test_missing_input(self):
  d=copy.deepcopy(EXAMPLE);del d['F']
  with self.assertRaises(ValueError):make_certificate(d)
 def test_tuple_point(self):
  d=copy.deepcopy(EXAMPLE);d['A']=(0,3)
  with self.assertRaises(ValueError):make_certificate(d)
 def test_bad_length(self):
  d=copy.deepcopy(EXAMPLE);d['A']=[0,3,1]
  with self.assertRaises(ValueError):make_certificate(d)
def input_test(value):
 def test(self):
  d=copy.deepcopy(EXAMPLE);d['A'][0]=value
  with self.assertRaises(ValueError):make_certificate(d)
 return test
def cert_test(value):
 def test(self):
  c=make_certificate(EXAMPLE);c['area']['ABCD']=value;self.assertFalse(verify_certificate(EXAMPLE,c))
 return test
for i,v in enumerate([True,0.0,None,'0/2',' 0','1/0',F(0)]):setattr(Tests,'test_input_type_'+str(i),input_test(v))
for i,v in enumerate([True,12,12.0,None,[],{'x':'12'}]):setattr(Tests,'test_cert_type_'+str(i),cert_test(v))
if __name__=='__main__':unittest.main(verbosity=2)
