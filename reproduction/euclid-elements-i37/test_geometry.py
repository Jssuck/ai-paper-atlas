import unittest,copy
from geometry import *
from cases import *
class Tests(unittest.TestCase):
 def test_example(self):self.assertEqual(make_certificate(EXAMPLE)['area'],{'ABC':'6','DBC':'6','EBCA':'12','DBCF':'12'})
 def test_vertices(self):self.assertEqual(make_certificate(EXAMPLE)['vertices'],{'E':['-3','3'],'F':['13','3']})
 def test_halves(self):self.assertEqual(set(make_certificate(EXAMPLE)['halves'].values()),{'6'})
 def test_parallel(self):self.assertEqual(set(make_certificate(EXAMPLE)['parallel_checks'].values()),{'0'})
 def test_family(self):
  for d in positives():
   c=make_certificate(d);self.assertTrue(verify_certificate(d,c));self.assertEqual(c['area']['ABC'],c['area']['DBC']);self.assertEqual(F(c['area']['EBCA']),2*F(c['area']['ABC']))
 def test_negative_direct(self):
  for d in negatives():
   with self.assertRaises(ValueError):make_certificate(d)
 def test_coincidence(self):self.assertEqual(make_certificate(build(0))['top_case'],'coincident')
 def test_backward(self):self.assertEqual(make_certificate(build(-2))['top_case'],'backward')
 def test_height_sign(self):self.assertLess(F(make_certificate(build(h=-3))['signed_double_triangle_area']),0)
 def test_fraction(self):self.assertTrue(verify_certificate(build('1/2'),make_certificate(build('1/2'))))
 def test_missing_key(self):
  d=copy.deepcopy(EXAMPLE);del d['A']
  with self.assertRaises(ValueError):make_certificate(d)
 def test_extra_key(self):
  d=copy.deepcopy(EXAMPLE);d['X']=[0,0]
  with self.assertRaises(ValueError):make_certificate(d)
 def test_bad_scalar(self):
  for x in [True,False,1.0,None,{},[],'0.5','2/4','01','nan','1/0']:
   d=copy.deepcopy(EXAMPLE);d['A'][0]=x
   with self.assertRaises(ValueError):make_certificate(d)
 def test_bad_point(self):
  for x in [(1,3),[1],[1,2,3],None,'1,3']:
   d=copy.deepcopy(EXAMPLE);d['A']=x
   with self.assertRaises(ValueError):make_certificate(d)
 def test_bad_root(self):
  for x in [None,[],True,'ABCD']:
   with self.assertRaises(ValueError):make_certificate(x)
 def test_empty_cert(self):self.assertFalse(verify_certificate(EXAMPLE,{}))
 def test_bool_cert(self):
  c=make_certificate(EXAMPLE);c['base_squared']=True;self.assertFalse(verify_certificate(EXAMPLE,c))
 def test_number_cert(self):
  c=make_certificate(EXAMPLE);c['base_squared']=16;self.assertFalse(verify_certificate(EXAMPLE,c))
 def test_area_attack(self):
  c=make_certificate(EXAMPLE);c['area']['ABC']='7';self.assertFalse(verify_certificate(EXAMPLE,c))
 def test_vertex_attack(self):
  c=make_certificate(EXAMPLE);c['vertices']['E'][0]='0';self.assertFalse(verify_certificate(EXAMPLE,c))
 def test_input_attack(self):
  c=make_certificate(EXAMPLE);c['input']['A'][0]='2';self.assertFalse(verify_certificate(EXAMPLE,c))
 def test_rebind(self):self.assertFalse(verify_certificate(build(3),make_certificate(EXAMPLE)))
 def test_translation_rebind(self):
  d={k:[v[0]+1,v[1]+1] for k,v in EXAMPLE.items()};self.assertFalse(verify_certificate(d,make_certificate(EXAMPLE)))
 def test_extra_cert(self):
  c=make_certificate(EXAMPLE);c['extra']='x';self.assertFalse(verify_certificate(EXAMPLE,c))
 def test_missing_cert(self):
  c=make_certificate(EXAMPLE);del c['halves'];self.assertFalse(verify_certificate(EXAMPLE,c))
 def test_tuple_cert(self):
  c=make_certificate(EXAMPLE);c['vertices']['E']=tuple(c['vertices']['E']);self.assertFalse(verify_certificate(EXAMPLE,c))
 def test_nonjson_cert(self):self.assertFalse(verify_certificate(EXAMPLE,float('nan')))
if __name__=='__main__':unittest.main(verbosity=2)
