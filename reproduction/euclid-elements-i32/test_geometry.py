import unittest
from copy import deepcopy
from geometry import make_certificate, verify_certificate, pair, multiply
from cases import fixture, positives, negatives
class Tests(unittest.TestCase):
 def test_positive_family(self):
  for x in positives(): self.assertTrue(verify_certificate(x,make_certificate(x)))
 def test_example(self):
  c=make_certificate(fixture());self.assertEqual(c['angles']['ACD'],['-4','2']);self.assertEqual(c['products']['A_plus_B_plus_C'],['-20','0'])
 def test_reflection(self): self.assertTrue(verify_certificate(fixture(h=-1),make_certificate(fixture(h=-1))))
 def test_obtuse(self): self.assertTrue(verify_certificate(fixture(a=-3),make_certificate(fixture(a=-3))))
 def test_rebinding(self): self.assertFalse(verify_certificate(fixture(h=2),make_certificate(fixture())))
 def test_schema_bool(self):
  x=fixture();c=make_certificate(x);c['schema']=True;self.assertFalse(verify_certificate(x,c))
 def test_conclusion_int(self):
  x=fixture();c=make_certificate(x);c['conclusion']['ray_inside_exterior']=1;self.assertFalse(verify_certificate(x,c))
 def test_digest(self):
  x=fixture();c=make_certificate(x);c['input_sha256']='bad';self.assertFalse(verify_certificate(x,c))
 def test_extra(self):
  x=fixture();c=make_certificate(x);c['extra']=True;self.assertFalse(verify_certificate(x,c))
 def test_missing(self): self.assertFalse(verify_certificate(fixture(),{}))
 def test_changed_product(self):
  x=fixture();c=make_certificate(x);c['products']['A_plus_B_plus_C']=['1','0'];self.assertFalse(verify_certificate(x,c))
def negative_test(x):
 def test(self):
  with self.assertRaises(ValueError):make_certificate(x)
 return test
for name,x in negatives():setattr(Tests,'test_negative_'+name,negative_test(x))
for name,val in [('bool',True),('int',1),('float',1.0),('space',' 1'),('ratio','2/2'),('zero_den','1/0'),('nan','NaN')]:
 x=fixture();x['A'][0]=val;setattr(Tests,'test_type_'+name,negative_test(x))
if __name__=='__main__':unittest.main(verbosity=2)
