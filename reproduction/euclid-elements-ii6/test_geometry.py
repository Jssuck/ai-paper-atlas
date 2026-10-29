import unittest,copy
from fractions import Fraction as Q
from geometry import construct,verify,area
class GeometryTests(unittest.TestCase):
 def test_01_default(self):self.assertEqual(verify(construct())['AM'],16)
 def test_02_grid(self):
  for a in range(1,9):
   for b in range(1,9):
    r=verify(construct(a,b),a,b);self.assertEqual(r['square'],r['AM']+r['LG'])
 def test_03_fraction(self):self.assertEqual(verify(construct(Q(2,3),Q(5,7)),Q(2,3),Q(5,7))['LG'],Q(4,9))
 def test_04_rotation(self):self.assertEqual(verify(construct(u=(3,4),v=(-4,3)),u=(3,4),v=(-4,3))['AM'],400)
 def test_05_reflection(self):self.assertEqual(verify(construct(v=(0,-1)),v=(0,-1))['AM'],16)
 def test_06_translation(self):self.assertEqual(verify(construct(origin=(-9,12)),origin=(-9,12))['LG'],9)
 def test_07_a_zero(self):self.assertRaises(ValueError,construct,0,2)
 def test_08_b_zero(self):self.assertRaises(ValueError,construct,3,0)
 def test_09_negative(self):self.assertRaises(ValueError,construct,3,-1)
 def test_10_float(self):self.assertRaises(ValueError,construct,3.0,2)
 def test_11_boolean(self):self.assertRaises(ValueError,construct,True,2)
 def test_12_basis(self):self.assertRaises(ValueError,construct,u=(0,0))
 def test_13_oblique(self):self.assertRaises(ValueError,construct,v=(1,1))
 def test_14_unequal(self):self.assertRaises(ValueError,construct,v=(0,2))
 def test_15_tamper_all(self):
  for n in construct()['points']:
   c=construct();x,y=c['points'][n];c['points'][n]=(x+Q(1,7),y);self.assertRaises(ValueError,verify,c)
 def test_16_missing(self):
  c=construct();del c['points']['H'];self.assertRaises(ValueError,verify,c)
 def test_17_extra(self):
  c=construct();c['points']['I']=(0,0);self.assertRaises(ValueError,verify,c)
 def test_18_schema(self):
  for c in (None,{},[],{'points':[]},{'points':construct()['points'],'area':16}):self.assertRaises(ValueError,verify,c)
 def test_19_bad_point(self):
  for p in (None,[1],True,[True,0],[1.0,0]):
   c=construct();c['points']['H']=p;self.assertRaises(ValueError,verify,c)
 def test_20_shoelace(self):self.assertEqual(area([(0,0),(4,0),(4,3),(0,3)]),12)
if __name__=='__main__':unittest.main()
