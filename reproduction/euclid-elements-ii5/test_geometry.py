import unittest,copy
from fractions import Fraction as Q
from geometry import construct,verify

class Tests(unittest.TestCase):
 def test_default(self):
  a=verify(construct());self.assertEqual(a['AH'],21);self.assertEqual(a['LG'],4);self.assertEqual(a['square'],25)
 def test_grid(self):
  for u,v in [((5,0),(0,5)),((3,4),(-4,3)),((-3,-4),(-4,3)),((Q(1,2),Q(1,3)),(Q(-1,3),Q(1,2)))]:
   for C in [(0,0),(7,-11)]:
    for t in [Q(i,9) for i in range(1,9)]:verify(construct(C,u,v,t),C,u,v,t)
 def test_fraction(self):
  a=verify(construct(u=(1,0),v=(0,1),t=Q(2,7)),u=(1,0),v=(0,1),t=Q(2,7));self.assertEqual(a['LG'],Q(4,49))
 def test_zero_basis(self):
  with self.assertRaises(ValueError):construct(u=(0,0))
 def test_rectangle(self):
  with self.assertRaises(ValueError):construct(v=(0,6))
 def test_rhombus(self):
  with self.assertRaises(ValueError):construct(u=(5,0),v=(3,4))
 def test_endpoint(self):
  for t in (0,1):
   with self.assertRaises(ValueError):construct(t=t)
 def test_external(self):
  for t in (-1,2):
   with self.assertRaises(ValueError):construct(t=t)
 def test_bool(self):
  with self.assertRaises(ValueError):construct(t=True)
 def test_float(self):
  with self.assertRaises(ValueError):construct(t=0.4)
 def test_string(self):
  with self.assertRaises(ValueError):construct(C=('0',0))
 def test_bad_container(self):
  for C in (None,{'x':0,'y':0},(0,),[0,0,0]):
   with self.assertRaises(ValueError):construct(C=C)
 def test_missing_field(self):
  c=construct();del c['points']
  with self.assertRaises(ValueError):verify(c)
 def test_extra_field(self):
  c=construct();c['ignored']=0
  with self.assertRaises(ValueError):verify(c)
 def test_point_tamper(self):
  for name in construct()['points']:
   for i in range(2):
    c=construct();p=list(c['points'][name]);p[i]+=1;c['points'][name]=p
    with self.assertRaises(ValueError):verify(c)
 def test_whole_translate(self):
  c=construct();c['points']={k:(x+1,y+1) for k,(x,y) in c['points'].items()}
  with self.assertRaises(ValueError):verify(c)
 def test_reverse_regions(self):
  for name in construct()['regions']:
   c=construct();c['regions'][name]=tuple(reversed(c['regions'][name]))
   with self.assertRaises(ValueError):verify(c)
 def test_wrong_diagonal(self):
  c=construct();c['points']['H']=(Q(2),Q(2))
  with self.assertRaises(ValueError):verify(c)
 def test_bad_certificate_point(self):
  for p in (None,[True,0],['0',0],{'x':0,'y':0}):
   c=construct();c['points']['H']=p
   with self.assertRaises(ValueError):verify(c)
 def test_verifier_inputs(self):
  for t in (True,0,1,-1,1.0):
   with self.assertRaises(ValueError):verify(construct(),t=t)

if __name__=='__main__':unittest.main()
