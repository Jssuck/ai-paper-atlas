import unittest, copy
from geometry import *
from cases import *
class GeometryTests(unittest.TestCase):
    def setUp(self):
        self.args=((0,0),(3,0),(0,4));self.c=construct(*self.args)
    def test_01_valid(self):self.assertTrue(verify(*self.args,self.c))
    def test_02_family(self):
        for args in valid_cases():self.assertTrue(verify(*args,construct(*args)))
    def test_03_invalid(self):
        for args in invalid_cases():
            with self.assertRaises(ValueError):construct(*args)
    def test_04_areas(self):self.assertEqual([report(self.c)[k] for k in ['AB_square','AC_square','BC_square']],['9','16','25'])
    def test_05_sas_left(self):self.assertEqual(area(self.c['A'],self.c['B'],self.c['D']),area(self.c['F'],self.c['B'],self.c['C']))
    def test_06_sas_right(self):self.assertEqual(area(self.c['A'],self.c['C'],self.c['E']),area(self.c['K'],self.c['C'],self.c['B']))
    def test_07_wrong_point(self):
        for key in self.c:
            c=copy.deepcopy(self.c);c[key]=add(c[key],(1,0));self.assertFalse(verify(*self.args,c),key)
    def test_08_missing(self):
        c=dict(self.c);del c['L'];self.assertFalse(verify(*self.args,c))
    def test_09_extra(self):
        c=dict(self.c);c['Z']=(0,0);self.assertFalse(verify(*self.args,c))
    def test_10_swap_fg(self):
        c=dict(self.c);c['F'],c['G']=c['G'],c['F'];self.assertFalse(verify(*self.args,c))
    def test_11_swap_hk(self):
        c=dict(self.c);c['H'],c['K']=c['K'],c['H'];self.assertFalse(verify(*self.args,c))
    def test_12_inward_ab(self):
        c=dict(self.c);c['F']=(3,3);c['G']=(0,3);self.assertFalse(verify(*self.args,c))
    def test_13_inward_ac(self):
        c=dict(self.c);c['H']=(4,0);c['K']=(4,4);self.assertFalse(verify(*self.args,c))
    def test_14_inward_bc(self):
        c=dict(self.c);w=sub(c['D'],c['B']);c['D']=sub(c['B'],w);c['E']=sub(c['C'],w);self.assertFalse(verify(*self.args,c))
    def test_15_foot_endpoint(self):
        c=dict(self.c);c['M']=c['B'];c['L']=c['D'];self.assertFalse(verify(*self.args,c))
    def test_16_float_certificate(self):
        c=dict(self.c);c['A']=(0.0,0);self.assertFalse(verify(*self.args,c))
    def test_17_bool_certificate(self):
        c=dict(self.c);c['A']=(False,0);self.assertFalse(verify(*self.args,c))
    def test_18_different_input(self):self.assertFalse(verify((0,0),(4,0),(0,3),self.c))
    def test_19_invalid_certificate(self):self.assertFalse(verify(*self.args,None))
    def test_20_mirror(self):
        args=((0,0),(3,0),(0,-4));self.assertTrue(verify(*args,construct(*args)))
    def test_21_no_triples_needed(self):
        args=((0,0),(1,0),(0,1));self.assertTrue(verify(*args,construct(*args)))
if __name__=='__main__':unittest.main(verbosity=2)
