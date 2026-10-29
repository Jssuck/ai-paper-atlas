import unittest,copy
from fractions import Fraction as Q
from geometry import construct,verify,normalized_segments
class GeometryTests(unittest.TestCase):
 def test_default(self):self.assertEqual(verify(construct())['lhs'],58)
 def test_routes(self):self.assertEqual(verify(construct())['squares']['AF'],58)
 def test_grid(self):
  for h in range(2,10):
   for k in range(1,9):
    d=Q(h*k,9);self.assertEqual(verify(construct(h,d),h,d)['lhs'],2*(h*h+d*d))
 def test_fraction(self):self.assertEqual(verify(construct(Q(5,2),Q(1,3)),Q(5,2),Q(1,3))['lhs'],Q(229,18))
 def test_translation(self):verify(construct(origin=(7,-2)),origin=(7,-2))
 def test_rotation(self):verify(construct(u=(0,1),v=(-1,0)),u=(0,1),v=(-1,0))
 def test_reflection(self):verify(construct(v=(0,-1)),v=(0,-1))
 def test_scale(self):self.assertEqual(verify(construct(u=(3,4),v=(-4,3)),u=(3,4),v=(-4,3))['lhs'],1450)
 def test_negative_h(self):
  with self.assertRaises(ValueError):construct(-1,1)
 def test_midpoint(self):
  with self.assertRaises(ValueError):construct(5,0)
 def test_endpoint(self):
  with self.assertRaises(ValueError):construct(5,5)
 def test_exterior(self):
  with self.assertRaises(ValueError):construct(5,6)
 def test_bool(self):
  with self.assertRaises(ValueError):construct(True,1)
 def test_float(self):
  with self.assertRaises(ValueError):construct(5,2.0)
 def test_basis(self):
  for u,v in [((0,0),(0,0)),((1,0),(1,1)),((1,0),(0,2))]:
   with self.assertRaises(ValueError):construct(u=u,v=v)
 def test_tamper(self):
  c=construct();c['points']['F']=(7,4)
  with self.assertRaises(ValueError):verify(c)
 def test_labels(self):
  for mode in ('extra','missing'):
   c=construct()
   if mode=='extra':c['points']['Z']=(0,0)
   else:del c['points']['E']
   with self.assertRaises(ValueError):verify(c)
 def test_bad_certificate(self):
  for c in [None,[],{}, {'points':[]},{'points':None}]:
   with self.assertRaises(ValueError):verify(c)
 def test_bad_coordinate(self):
  for val in [(True,0),(1.0,0),(1,),None]:
   c=construct();c['points']['A']=val
   with self.assertRaises(ValueError):verify(c)
 def test_left_normalization(self):
  n=normalized_segments(5,-2);self.assertTrue(n['swap_endpoints']);self.assertEqual((n['AD_original'],n['DB_original']),(3,7));self.assertEqual(verify(construct(n['h'],n['d']),n['h'],n['d'])['lhs'],58)
if __name__=='__main__':unittest.main()
