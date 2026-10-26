import unittest
from fractions import Fraction as Q
from geometry import angle_equal, certificate, family, outward, squared, transform

class GeometryTests(unittest.TestCase):
    def setUp(self): self.p=family(3,4,2)
    def test_example(self): self.assertTrue(certificate(*self.p)['accepted'])
    def test_all_steps(self): self.assertTrue(all(certificate(*self.p)['steps'].values()))
    def test_base(self): self.assertTrue(certificate(*self.p)['conclusions']['base_ABC_ACB'])
    def test_external(self): self.assertTrue(certificate(*self.p)['conclusions']['external_FBC_GCB'])
    def test_squared_lengths(self):
        a,b,c,f,g=self.p
        self.assertEqual([squared(a,b),squared(a,f),squared(b,f),squared(f,c)], [25,100,25,97])
    def test_fractional(self): self.assertTrue(certificate(*family(Q(1,3),Q(2,5),Q(7,6)))['accepted'])
    def test_rotation(self): self.assertTrue(certificate(*transform(self.p,Q(3,5),Q(4,5)))['accepted'])
    def test_reflection(self): self.assertTrue(certificate(*transform(self.p,0,1,-1))['accepted'])
    def test_translation(self): self.assertTrue(certificate(*transform(self.p,translation=(Q(1,7),-6)))['accepted'])
    def test_swap_sides(self):
        a,b,c,f,g=self.p
        self.assertTrue(certificate(a,c,b,g,f)['accepted'])
    def test_wrong_correspondence(self):
        a,b,c,f,g=self.p
        self.assertFalse(certificate(a,b,c,g,f)['accepted'])
    def test_wrong_ray(self):
        a,b,c,f,g=self.p
        self.assertFalse(certificate(a,b,c,(0,4),g)['accepted'])
    def test_f_at_b(self):
        a,b,c,f,g=self.p
        self.assertFalse(certificate(a,b,c,b,g)['accepted'])
    def test_g_at_c(self):
        a,b,c,f,g=self.p
        self.assertFalse(certificate(a,b,c,f,c)['accepted'])
    def test_inside(self):
        a,b,c,f,g=self.p
        self.assertFalse(certificate(a,b,c,(-Q(3,2),2),g)['accepted'])
    def test_unequal_legs(self):
        a,b,c,f,g=self.p
        self.assertFalse(certificate(a,b,(4,0),f,g)['accepted'])
    def test_unequal_AF_AG(self):
        a,b,c,f,g=self.p
        self.assertFalse(certificate(a,b,c,f,(9,-8))['accepted'])
    def test_collinear(self): self.assertFalse(certificate((0,0),(-1,0),(1,0),(-2,0),(2,0))['accepted'])
    def test_zero_leg(self): self.assertFalse(certificate((0,0),(0,0),(1,0),(0,0),(2,0))['accepted'])
    def test_outward_false_behind(self): self.assertFalse(outward((0,0),(1,0),(-2,0)))
    def test_outward_false_noncollinear(self): self.assertFalse(outward((0,0),(1,0),(2,1)))
    def test_acute_obtuse_not_equal(self): self.assertFalse(angle_equal((1,0),(0,0),(1,1),(1,0),(0,0),(-1,1)))
    def test_right_angles(self): self.assertTrue(angle_equal((1,0),(0,0),(0,1),(0,3),(0,0),(-2,0)))
    def test_zero_and_straight(self): self.assertFalse(angle_equal((1,0),(0,0),(2,0),(1,0),(0,0),(-2,0)))
    def test_zero_ray_raises(self):
        with self.assertRaises(ValueError): angle_equal((0,0),(0,0),(1,0),(1,0),(0,0),(0,1))
    def test_float_rejected(self):
        with self.assertRaises(TypeError): family(1.0,2,3)
    def test_bool_rejected(self):
        with self.assertRaises(TypeError): family(True,2,3)
    def test_bad_point_rejected(self):
        with self.assertRaises(TypeError): certificate((0,),*self.p[1:])
    def test_t_boundary(self):
        with self.assertRaises(ValueError): family(1,2,1)
    def test_height_boundary(self):
        with self.assertRaises(ValueError): family(1,0,2)
    def test_width_boundary(self):
        with self.assertRaises(ValueError): family(0,1,2)
    def test_nonorthogonal(self):
        with self.assertRaises(ValueError): transform(self.p,1,1)
    def test_bad_orientation(self):
        with self.assertRaises(ValueError): transform(self.p,orientation=0)
    def test_orientation_bool(self):
        with self.assertRaises(ValueError): transform(self.p,orientation=True)

if __name__=='__main__': unittest.main()
