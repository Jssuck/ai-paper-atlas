import unittest
from copy import deepcopy
from geometry import make_certificate,verify_certificate
from cases import example,positives,negatives
class GeometryTests(unittest.TestCase):
 def test_example(self):
  d=example();self.assertTrue(verify_certificate(d,make_certificate(d)))
 def test_family(self):
  for d in positives(): self.assertTrue(verify_certificate(d,make_certificate(d)))
 def test_negative_geometry(self):
  for d in negatives():
   with self.assertRaises(ValueError): make_certificate(d)
 def test_rebinding(self):
  d=example();c=make_certificate(d);d['B']=['3','1'];self.assertFalse(verify_certificate(d,c))
 def test_no_alias(self):
  d=example();c=make_certificate(d);d['E'][0]='9';self.assertEqual(c['input']['E'][0],'0')
 def test_scalar_types(self):
  for v in (True,False,1,1.0,None,[],{},'1.0','01','1/1',' 1','1/0','nan'):
   d=example();d['A'][0]=v
   with self.assertRaises(ValueError): make_certificate(d)
 def test_root(self):
  for d in (None,[],True,dict(A=['0','0'])):
   with self.assertRaises(ValueError): make_certificate(d)
 def test_points(self):
  for v in (('0','1'),['0'],['0','1','2'],'01',None):
   d=example();d['A']=v
   with self.assertRaises(ValueError): make_certificate(d)
 def test_extra_field(self):
  d=example();d['extra']=0
  with self.assertRaises(ValueError): make_certificate(d)
 def test_verifier_invalid(self):
  for d in negatives(): self.assertFalse(verify_certificate(d,{}))
 def test_antiparallel(self):
  c=make_certificate(example());self.assertEqual(c['scales'],['2','-1'])
 def test_intersections(self):
  c=make_certificate(example());self.assertEqual(c['transversal']['parameters'],['1','3','0'])
 def test_vertical(self):
  d={k:[str(-int(v[1])),v[0]] for k,v in example().items()};self.assertTrue(verify_certificate(d,make_certificate(d)))
 def test_rational(self):
  d={k:[str(__import__('fractions').Fraction(x)/3) for x in v] for k,v in example().items()};self.assertTrue(verify_certificate(d,make_certificate(d)))

def attack(field,value):
 def test(self):
  d=example();c=make_certificate(d);c[field]=value;self.assertFalse(verify_certificate(d,c))
 return test
for i,(key,value) in enumerate([('schema',True),('schema',1.0),('schema',2),('model','wrong'),('input',{}),('input_sha256','0'*64),('premise_determinants',[0,0]),('premise_determinants',('0','0')),('scales',['1','1']),('distinctness_determinants',['0','0','0']),('transversal',{}),('conclusion',{'determinant':'0','distinct':1,'parallel':1}),('conclusion',{'determinant':'0','distinct':True,'parallel':False})]):
 setattr(GeometryTests,f'test_attack_{i:02}',attack(key,value))
if __name__=='__main__': unittest.main()
