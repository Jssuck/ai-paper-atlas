import unittest
from fractions import Fraction as F
from geometry import *

class GeometryTests(unittest.TestCase):
    def test_isosceles(self): self.assertTrue(triangle_certificate((0,3),(-2,0),(2,0))['base_angles_equal'])
    def test_scalene(self): self.assertFalse(triangle_certificate((0,0),(5,0),(0,3))['base_angles_equal'])
    def test_implication_vacuous(self): self.assertTrue(triangle_certificate((0,0),(5,0),(0,3))['implication_holds'])
    def test_reflection(self): self.assertTrue(triangle_certificate((0,-3),(-2,0),(2,0))['opposite_sides_equal'])
    def test_translation(self): self.assertTrue(triangle_certificate((7,8),(5,5),(9,5))['base_angles_equal'])
    def test_scaling(self): self.assertTrue(triangle_certificate((0,F(3,7)),(F(-2,7),0),(F(2,7),0))['base_angles_equal'])
    def test_swap(self): self.assertTrue(triangle_certificate((0,3),(2,0),(-2,0))['base_angles_equal'])
    def test_collinear(self):
        with self.assertRaises(ValueError): triangle_certificate((0,0),(1,0),(2,0))
    def test_repeated(self):
        with self.assertRaises(ValueError): triangle_certificate((0,0),(0,0),(2,0))
    def test_float(self):
        with self.assertRaises(TypeError): point((0.1,0))
    def test_bool(self):
        with self.assertRaises(TypeError): point((True,0))
    def test_shape(self):
        with self.assertRaises(TypeError): point((1,2,3))
    def test_angle_same(self): self.assertTrue(angle_equal((1,0),(1,1),(2,0),(4,4)))
    def test_angle_supplement(self): self.assertFalse(angle_equal((1,0),(1,1),(1,0),(-1,1)))
    def test_angle_right(self): self.assertTrue(angle_equal((1,0),(0,2),(0,3),(4,0)))
    def test_zero_ray(self):
        with self.assertRaises(ValueError): angle_equal((0,0),(1,0),(1,0),(1,1))
    def test_straight_zero(self): self.assertFalse(angle_equal((1,0),(1,0),(1,0),(-1,0)))
    def test_cut(self):
        q=strict_cut_certificate((0,0),(5,0),(0,3),(2,0))
        self.assertTrue(q['valid_cut']); self.assertEqual(q['area_ratio'],F(3,5)); self.assertFalse(q['contradiction_premises'])
    def test_wrong_cut(self): self.assertFalse(strict_cut_certificate((0,0),(5,0),(0,3),(3,0))['valid_cut'])
    def test_wrong_ray(self): self.assertFalse(strict_cut_certificate((0,0),(5,0),(0,3),(8,0))['valid_cut'])
    def test_off_line(self): self.assertFalse(strict_cut_certificate((0,0),(5,0),(0,3),(5,3))['valid_cut'])
    def test_endpoint(self): self.assertFalse(strict_cut_certificate((0,0),(3,0),(0,3),(0,0))['valid_cut'])
    def test_construct(self): self.assertEqual(cut_from_rational_ratio((0,0),(5,0),(0,3),F(3,5)),(F(2),F(0)))
    def test_wrong_ratio(self):
        with self.assertRaises(ValueError): cut_from_rational_ratio((0,0),(5,0),(0,3),F(2,5))
    def test_ratio_endpoint(self):
        with self.assertRaises(ValueError): cut_from_rational_ratio((0,0),(3,0),(0,3),1)
    def test_factor_equal(self): self.assertTrue(factor_certificate(5,5,6)['angle_equation'])
    def test_factor_unequal(self): self.assertFalse(factor_certificate(3,5,4)['angle_equation'])
    def test_factor_identity(self): self.assertTrue(factor_certificate(F(3,2),F(5,2),2)['identity_holds'])
    def test_factor_degenerate(self):
        with self.assertRaises(ValueError): factor_certificate(1,2,3)
    def test_factor_negative(self):
        with self.assertRaises(ValueError): factor_certificate(-1,2,2)

if __name__=='__main__': unittest.main()
