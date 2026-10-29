import unittest
from fractions import Fraction as Q
from geometry import *

BASE=((0,0),25,(-3,4),(3,4),(0,4))
class Tests(unittest.TestCase):
    def test_midpoint(self): self.assertTrue(certificate(*BASE)['bisects'])
    def test_right(self): self.assertTrue(certificate(*BASE)['perpendicular'])
    def test_oblique(self):
        c=certificate(*BASE[:-1],(1,4));self.assertFalse(c['bisects']);self.assertFalse(c['perpendicular'])
    def test_identity(self):
        c=certificate(*BASE[:-1],(-1,4));self.assertEqual(2*c['dot_EF_AB'],c['AF_squared']-c['BF_squared'])
    def test_reverse(self): self.assertTrue(certificate(BASE[0],25,BASE[3],BASE[2],BASE[4])['bisects'])
    def test_grid(self):
        rows=list(grid());self.assertEqual(len(rows),900)
        for c in rows: self.assertTrue(verify_certificate(c));self.assertEqual(c['bisects'],c['parameter']==Q(1,2))
    def test_rational(self): self.assertTrue(certificate((Q(0),0),25,(-3,4),(3,4),(0,4))['equivalent'])
    def test_diameter(self):
        with self.assertRaises(ValueError): certificate((0,0),25,(-5,0),(5,0),(0,0))
    def test_zero_vector(self):
        with self.assertRaises(ValueError): perpendicular((0,0),(1,0))
    def test_zero_other(self):
        with self.assertRaises(ValueError): perpendicular((1,0),(0,0))
    def test_not_on_circle(self):
        with self.assertRaises(ValueError): certificate((0,0),25,(-3,4),(4,4),(0,4))
    def test_same_endpoints(self):
        with self.assertRaises(ValueError): certificate((0,0),25,(-3,4),(-3,4),(-3,4))
    def test_endpoint(self):
        with self.assertRaises(ValueError): certificate(*BASE[:-1],(-3,4))
    def test_exterior(self):
        with self.assertRaises(ValueError): certificate(*BASE[:-1],(4,4))
    def test_noncollinear(self):
        with self.assertRaises(ValueError): certificate(*BASE[:-1],(0,3))
    def test_radius(self):
        with self.assertRaises(ValueError): certificate((0,0),0,(-3,4),(3,4),(0,4))
    def test_bool(self):
        with self.assertRaises(TypeError): certificate((True,0),25,(-3,4),(3,4),(0,4))
    def test_float(self):
        with self.assertRaises(TypeError): certificate((0,0),25.0,(-3,4),(3,4),(0,4))
    def test_shape(self):
        with self.assertRaises(TypeError): certificate((0,0,0),25,(-3,4),(3,4),(0,4))
    def test_forged_field(self):
        c=certificate(*BASE);c['AF_squared']=Q(10);self.assertFalse(verify_certificate(c))
    def test_bool_integer_alias(self):
        c=certificate(*BASE);c['bisects']=1;self.assertFalse(verify_certificate(c))
    def test_missing_extra(self):
        c=certificate(*BASE);c.pop('branch');self.assertFalse(verify_certificate(c))
        c=certificate(*BASE);c['extra']=0;self.assertFalse(verify_certificate(c))
    def test_bad_certificate(self):
        for c in (None,[],{},True): self.assertFalse(verify_certificate(c))
    def test_list_not_canonical(self):
        c=certificate(*BASE);c['E']=list(c['E']);self.assertFalse(verify_certificate(c))
if __name__=='__main__': unittest.main(verbosity=2)
