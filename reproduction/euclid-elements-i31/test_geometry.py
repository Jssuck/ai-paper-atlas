import unittest
from copy import deepcopy
from geometry import make_certificate,verify_certificate
from cases import fixture,positives,negatives

class Tests(unittest.TestCase):
 def test_positive_family(self):
  for x in positives(): self.assertTrue(verify_certificate(x,make_certificate(x)))
 def test_scales(self): self.assertEqual(make_certificate(fixture())['scales'],{'t':'1','u':'1'})
 def test_D_outside_segment(self):
  x=fixture();x['B']=['2','0'];self.assertTrue(verify_certificate(x,make_certificate(x)))
 def test_schema_bool(self):
  x=fixture();c=make_certificate(x);c['schema']=True;self.assertFalse(verify_certificate(x,c))
 def test_conclusion_int(self):
  x=fixture();c=make_certificate(x);c['conclusion']['A_between_E_F']=1;self.assertFalse(verify_certificate(x,c))
 def test_extra_certificate(self):
  x=fixture();c=make_certificate(x);c['extra']=1;self.assertFalse(verify_certificate(x,c))
 def test_rebinding(self):
  x=fixture();c=make_certificate(x);self.assertFalse(verify_certificate(fixture(a=2),c))
 def test_altered_digest(self):
  x=fixture();c=make_certificate(x);c['input_sha256']='0'*64;self.assertFalse(verify_certificate(x,c))
 def test_altered_scale(self):
  x=fixture();c=make_certificate(x);c['scales']['t']='2';self.assertFalse(verify_certificate(x,c))
 def test_missing_certificate(self): self.assertFalse(verify_certificate(fixture(),{}))

def negative_test(x):
 def test(self):
  with self.assertRaises(ValueError): make_certificate(x)
 return test
for name,x in negatives(): setattr(Tests,'test_negative_'+name,negative_test(x))
for name,value in [('bool',True),('int',1),('float',1.0),('space',' 1'),('ratio','2/2'),('zero_den','1/0'),('nan','NaN')]:
 x=fixture();x['A'][0]=value;setattr(Tests,'test_type_'+name,negative_test(x))
if __name__=='__main__': unittest.main(verbosity=2)
