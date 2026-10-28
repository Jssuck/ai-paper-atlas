import unittest,copy
from fractions import Fraction as Q
from geometry import construct,verify,REGIONS
class GeometryTests(unittest.TestCase):
 def test_integer(self): self.assertEqual(verify(construct()),{'whole':25,'HF':4,'CK':9,'AG':6,'GE':6})
 def test_grid(self):
  for u,v in [((5,0),(0,5)),((3,4),(-4,3)),((3,4),(4,-3)),((-5,0),(0,5))]:
   for t in [Q(k,9) for k in range(1,9)]:
    for A in [(0,0),(-2,Q(1,3))]:
     got=verify(construct(A,u,v,t),A,u,v,t)
     self.assertEqual(got['HF'],25*t*t); self.assertEqual(got['CK'],25*(1-t)**2)
 def test_endpoints(self):
  for t in [-1,0,1,2]:
   with self.assertRaises(ValueError): construct(t=t)
 def test_zero_side(self):
  with self.assertRaises(ValueError): construct(u=(0,0),v=(0,0))
 def test_rectangle_not_square(self):
  with self.assertRaises(ValueError): construct(v=(0,4))
 def test_rhombus_not_square(self):
  with self.assertRaises(ValueError): construct(u=(5,0),v=(3,4))
 def test_float(self):
  with self.assertRaises(ValueError): construct(t=.4)
 def test_bool(self):
  with self.assertRaises(ValueError): construct(t=True)
 def test_bad_point(self):
  with self.assertRaises(ValueError): construct(A=(1,2,3))
 def test_missing_point(self):
  c=construct(); del c['points']['G']
  with self.assertRaises(ValueError): verify(c)
 def test_diagonal(self):
  c=construct();c['points']['G']=(2,2)
  with self.assertRaises(ValueError): verify(c)
 def test_each_shifted_point(self):
  for n in construct()['points']:
   c=construct();p=c['points'][n];c['points'][n]=(p[0]+1,p[1])
   with self.assertRaises(ValueError):verify(c)
 def test_swapped_squares(self):
  c=construct();c['regions']['HF']=REGIONS['CK']
  with self.assertRaises(ValueError):verify(c)
 def test_reversed_region(self):
  c=construct();c['regions']['AG']=tuple(reversed(REGIONS['AG']))
  with self.assertRaises(ValueError):verify(c)
 def test_area_equal_shift_impostor(self):
  c=construct();c['points']={n:(p[0]+10,p[1]) for n,p in c['points'].items()}
  with self.assertRaises(ValueError):verify(c)
 def test_fraction(self):
  A=(Q(1,3),Q(-1,7));u=(Q(3,5),Q(4,5));v=(Q(-4,5),Q(3,5));t=Q(2,7)
  self.assertEqual(verify(construct(A,u,v,t),A,u,v,t)['whole'],1)
 def test_missing_field(self):
  with self.assertRaises(ValueError):verify({'points':{}})
 def test_string(self):
  with self.assertRaises(ValueError):construct(u=('5',0))
if __name__=='__main__':unittest.main()
