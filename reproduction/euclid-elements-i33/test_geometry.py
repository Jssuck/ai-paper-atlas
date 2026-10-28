import unittest,copy
from geometry import *
from cases import *

class TestGeometry(unittest.TestCase):
 def test_all_positive(self):
  for d in positive_cases():
   c=make_certificate(d); self.assertTrue(verify_certificate(d,c))
   self.assertEqual(c['conclusion']['AC_vector'],c['conclusion']['BD_vector'])
   self.assertEqual(c['sas']['included_dot_ABC'],c['sas']['included_dot_DCB'])
 def test_hand(self):
  c=make_certificate(BASE);self.assertEqual(c['conclusion']['AC_squared'],'5');self.assertEqual(c['sas']['included_dot_ABC'],'6')
 def test_input_binding(self):
  d=copy.deepcopy(BASE)
  for k in d:d[k][0]+=1
  self.assertFalse(verify_certificate(d,make_certificate(BASE)))
 def test_missing(self):
  c=make_certificate(BASE);del c['sas'];self.assertFalse(verify_certificate(BASE,c))
 def test_extra(self):
  c=make_certificate(BASE);c['extra']='1';self.assertFalse(verify_certificate(BASE,c))
 def test_scalar_mutations(self):
  for value in [True,False,0,1,0.0,None,float('nan'),[],{}]:
   c=make_certificate(BASE);c['premises']['base_cross']=value;self.assertFalse(verify_certificate(BASE,c))
 def test_nested_binding(self):
  c=make_certificate(BASE);c['input']['A'][0]='1';self.assertFalse(verify_certificate(BASE,c))
 def test_false_conclusion(self):
  c=make_certificate(BASE);c['conclusion']['AC_squared']='6';self.assertFalse(verify_certificate(BASE,c))
 def test_tuple_certificate(self):
  c=make_certificate(BASE);c['input']['A']=tuple(c['input']['A']);self.assertFalse(verify_certificate(BASE,c))
 def test_non_dict(self):
  for d in [[],None,0,'ABCD']:
   with self.assertRaises(ValueError):make_certificate(d)
 def test_bad_point(self):
  for point in [[0],[0,0,0],(0,0),None]:
   d=copy.deepcopy(BASE);d['A']=point
   with self.assertRaises(ValueError):make_certificate(d)
 def test_bad_rational(self):
  for s in ['1/0','NaN','1.0','+1',' 1','01']:
   d=copy.deepcopy(BASE);d['A'][0]=s
   with self.assertRaises(ValueError):make_certificate(d)
 def test_certificate_cycle(self):
  c=make_certificate(BASE);c['cycle']=c;self.assertFalse(verify_certificate(BASE,c))
 def test_reorder_keys(self):
  c=make_certificate(BASE);self.assertTrue(verify_certificate(BASE,dict(reversed(list(c.items())))))
 def test_equivalent_rational_input(self):
  d={k:list(map(str,v)) for k,v in BASE.items()};self.assertTrue(verify_certificate(d,make_certificate(BASE)))
 def test_reverse_both(self):
  d={'A':BASE['B'],'B':BASE['A'],'C':BASE['D'],'D':BASE['C']};self.assertTrue(verify_certificate(d,make_certificate(d)))
 def test_reject_certificate_for_invalid_input(self):
  for d in NEGATIVE:self.assertFalse(verify_certificate(d,make_certificate(BASE)))

for i,d in enumerate(NEGATIVE):
 def test(self,d=d):
  with self.assertRaises(ValueError):make_certificate(d)
 setattr(TestGeometry,'test_negative_%02d'%i,test)
if __name__=='__main__':unittest.main(verbosity=2)
