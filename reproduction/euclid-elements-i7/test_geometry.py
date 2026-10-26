import unittest
from fractions import Fraction as F
from geometry import certificate as c, reflect, verify_claim, distance2, point
class GeometryTests(unittest.TestCase):
    def test_valid(self): self.assertTrue(verify_claim((0,0),(4,0),(1,2),(1,2)))
    def test_mirror(self):
        r=c((0,0),(4,0),(1,2),(1,-2)); self.assertTrue(r['equal_a'] and r['equal_b']); self.assertFalse(r['premises'])
    def test_wrong_a(self): self.assertFalse(c((0,0),(4,0),(1,2),(4,2))['equal_a'])
    def test_wrong_b(self):
        r=c((0,0),(4,0),(1,2),(-1,2)); self.assertTrue(r['equal_a']); self.assertFalse(r['equal_b'])
    def test_wrong_correspondence(self):
        r=c((0,0),(4,0),(1,2),(3,2)); self.assertFalse(r['premises']); self.assertEqual(distance2((0,0),(1,2)),distance2((4,0),(3,2)))
    def test_coincident_baseline(self):
        with self.assertRaises(ValueError): c((0,0),(0,0),(1,2),(1,2))
    def test_base_c(self): self.assertFalse(c((0,0),(4,0),(1,0),(1,0))['premises'])
    def test_endpoint_c(self): self.assertFalse(c((0,0),(4,0),(0,0),(0,0))['premises'])
    def test_endpoint_b(self): self.assertFalse(c((0,0),(4,0),(4,0),(4,0))['premises'])
    def test_one_on_base(self): self.assertFalse(c((0,0),(4,0),(1,2),(1,0))['nondegenerate'])
    def test_negative_side(self): self.assertTrue(verify_claim((0,0),(4,0),(-1,-2),(-1,-2)))
    def test_beyond_base(self): self.assertTrue(verify_claim((0,0),(4,0),(8,2),(8,2)))
    def test_fraction(self): self.assertTrue(verify_claim((F(1,2),0),(F(7,3),1),(F(3,7),F(-1,2)),(F(3,7),F(-1,2))))
    def test_reversal(self): self.assertTrue(verify_claim((4,0),(0,0),(1,2),(1,2)))
    def test_translated(self): self.assertTrue(verify_claim((3,4),(7,4),(4,6),(4,6)))
    def test_vertical(self): self.assertTrue(verify_claim((1,1),(1,5),(3,2),(3,2)))
    def test_float(self):
        with self.assertRaises(TypeError): point((1.0,2))
    def test_bool(self):
        with self.assertRaises(TypeError): point((True,2))
    def test_dimension(self):
        with self.assertRaises(TypeError): point((1,2,3))
    def test_string(self):
        with self.assertRaises(TypeError): point('12')
    def test_bad_coordinate(self):
        with self.assertRaises(TypeError): point(('1',2))
    def test_reflect_horizontal(self): self.assertEqual(reflect((0,0),(4,0),(1,2)),(1,-2))
    def test_reflect_vertical(self): self.assertEqual(reflect((1,1),(1,5),(3,2)),(-1,2))
    def test_reflect_oblique(self): self.assertEqual(reflect((0,0),(1,1),(1,0)),(0,1))
    def test_reflect_twice(self):
        A=(F(1,2),2);B=(3,F(5,3));C=(F(-1,7),4);self.assertEqual(reflect(A,B,reflect(A,B,C)),point(C))
    def test_reflect_bad_base(self):
        with self.assertRaises(ValueError): reflect((0,0),(0,0),(1,2))
    def test_identities(self):
        r=c((1,2),(4,6),(-2,3),(7,-1))
        for key in ('distance_difference_identity','norm_cross_identity_c','norm_cross_identity_d','reconstruction_c','reconstruction_d'):self.assertTrue(r[key])
    def test_vacuity(self):
        r=c((0,0),(4,0),(1,2),(3,5));self.assertTrue(r['implication']);self.assertFalse(verify_claim((0,0),(4,0),(1,2),(3,5)))
if __name__=='__main__': unittest.main()
