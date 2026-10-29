import unittest,copy
from fractions import Fraction as Q
from geometry import construct,verify,side_diagonal
class GeometryTests(unittest.TestCase):
 def run_case(self,h=3,t=2,**kw):return verify(construct(h,t,**kw),h,t,**kw)
 def test_default(self):self.assertEqual(self.run_case()['lhs'],68)
 def test_routes(self):self.assertTrue(all(a==b for a,b in self.run_case()['routes'].values()))
 def test_grid(self):
  for h in range(1,9):
   for t in range(1,9):self.assertEqual(self.run_case(h,t)['lhs'],(2*h+t)**2+t*t)
 def test_fraction(self):self.run_case(Q(3,7),Q(5,11))
 def test_translation(self):self.assertEqual(self.run_case(origin=(13,-8))['lhs'],68)
 def test_rotation(self):self.run_case(u=(Q(3,5),Q(4,5)),v=(-Q(4,5),Q(3,5)))
 def test_reflection(self):self.run_case(u=(1,0),v=(0,-1))
 def test_scaled_basis(self):self.assertEqual(self.run_case(u=(2,0),v=(0,2))['lhs'],272)
 def test_tiny_extension(self):self.run_case(3,Q(1,10**8))
 def test_large_extension(self):self.run_case(1,10**8)
 def test_zero_negative(self):
  for h,t in [(0,1),(1,0),(-1,1),(1,-1)]:
   with self.assertRaises(ValueError):construct(h,t)
 def test_bad_scalars(self):
  for x in [True,False,1.0,'1',None,[],{}]:
   for args in [(x,1),(1,x)]:
    with self.assertRaises(ValueError):construct(*args)
 def test_bad_basis(self):
  for u,v in [((0,0),(0,0)),((1,0),(1,1)),((1,0),(0,2))]:
   with self.assertRaises(ValueError):construct(u=u,v=v)
 def test_bad_vectors(self):
  for o in [None,{},'12',(1,),[1,2,3],[True,0],[1.0,0]]:
   with self.assertRaises(ValueError):construct(origin=o)
 def test_point_tamper(self):
  for label in 'ABCDEFG':
   c=construct();x,y=c['points'][label];c['points'][label]=(x+1,y)
   with self.assertRaises(ValueError):verify(c)
 def test_labels(self):
  c=construct();c['points']['Z']=c['points'].pop('G')
  with self.assertRaises(ValueError):verify(c)
 def test_bad_certificate(self):
  for c in [None,[],{}, {'points':[]},{'points':{}},{'points':{},'extra':1}]:
   with self.assertRaises(ValueError):verify(c)
 def test_certificate_scalar_types(self):
  for bad in [True,1.0,'0']:
   c=construct();c['points']['A']=(bad,0)
   with self.assertRaises(ValueError):verify(c)
 def test_recurrence(self):
  rows=side_diagonal(8);self.assertEqual([(r['s'],r['d']) for r in rows[:4]],[(1,1),(2,3),(5,7),(12,17)])
  self.assertTrue(all(r['next_difference']==-r['difference'] for r in rows))
 def test_recurrence_domain(self):
  for n in [True,0,-1,1.0,'2',1001]:
   with self.assertRaises(ValueError):side_diagonal(n)
if __name__=='__main__':unittest.main()
