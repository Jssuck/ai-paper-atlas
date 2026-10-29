import unittest,copy
from fractions import Fraction as Q
from geometry import *
class Tests(unittest.TestCase):
    def setUp(self): self.cs=examples();self.c=self.cs['neither_midpoint']
    def test_01_examples(self): self.assertTrue(all(verify(c) for c in self.cs.values()))
    def test_02_neither(self): self.assertFalse(self.c['midpoint_AC']);self.assertFalse(self.c['midpoint_BD'])
    def test_03_single(self): c=self.cs['only_AC_midpoint'];self.assertTrue(c['theorem_applies']);self.assertTrue(c['midpoint_AC']);self.assertFalse(c['midpoint_BD'])
    def test_04_reverse(self): c=self.cs['only_BD_midpoint'];self.assertFalse(c['midpoint_AC']);self.assertTrue(c['midpoint_BD'])
    def test_05_one_diameter(self): c=self.cs['one_diameter'];self.assertFalse(c['theorem_applies']);self.assertFalse(c['both_midpoints'])
    def test_06_two_diameters(self): c=self.cs['two_diameters'];self.assertTrue(c['both_midpoints']);self.assertTrue(c['at_center'])
    def test_07_expected_E(self): self.assertEqual(self.c['E'],['3','3']);self.assertEqual(self.cs['only_AC_midpoint']['E'],['0','3'])
    def test_08_expected_parameters(self): self.assertEqual(self.c['t'],'7/8');self.assertEqual(self.c['u'],'1/8')
    def test_09_scalar_float(self): self.assertRaises(ValueError,scalar,0.5)
    def test_10_scalar_bool(self): self.assertRaises(ValueError,scalar,True)
    def test_11_scalar_bad(self): self.assertRaises(ValueError,scalar,'1/0')
    def test_12_scalar_canonical(self): self.assertRaises(ValueError,scalar,'2/2')
    def test_13_point(self): self.assertRaises(ValueError,point,[0,1,2])
    def test_14_radius(self): z=copy.deepcopy(self.c['input']);z['r2']='0';self.assertRaises(ValueError,certificate,**z)
    def test_15_offcircle(self): z=copy.deepcopy(self.c['input']);z['B']=[2,2];self.assertRaises(ValueError,certificate,**z)
    def test_16_zerochord(self): z=copy.deepcopy(self.c['input']);z['C']=z['A'];self.assertRaises(ValueError,certificate,**z)
    def test_17_parallel(self): self.assertRaises(ValueError,certificate,(0,0),25,(-4,3),(4,3),(-4,-3),(4,-3))
    def test_18_endpoint(self): self.assertRaises(ValueError,certificate,(0,0),25,(-4,3),(4,3),(4,3),(3,-4))
    def test_19_tamper(self):
        for key in self.c:
            c=copy.deepcopy(self.c);c[key]=None;self.assertFalse(verify(c))
    def test_20_bool_integer(self): c=copy.deepcopy(self.c);c['theorem_applies']=1;self.assertFalse(verify(c))
    def test_21_extra_missing(self): c=copy.deepcopy(self.c);c['extra']=0;self.assertFalse(verify(c));self.assertFalse(verify({}))
    def test_22_transform(self): self.assertTrue(verify(transformed(self.c,-2,(3,1),3,True)));self.assertRaises(ValueError,transformed,self.c,0)
    def test_23_grid(self):
        rows=grid();self.assertEqual(len(rows),600);self.assertTrue(all(verify(c) for c in rows));self.assertEqual(sum(c['both_midpoints'] for c in rows),120)
    def test_24_residuals(self):
        self.assertEqual(self.cs['only_AC_midpoint']['dot_v'],'0');self.assertNotEqual(self.cs['only_AC_midpoint']['dot_w'],'0')
if __name__=='__main__': unittest.main()
