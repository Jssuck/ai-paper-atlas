import unittest
from fractions import Fraction as F
from copy import deepcopy
from geometry import *
from cases import positive_cases,negative_cases,evaluate

BASE=((0,0),(1,0),(-2,0),(1,2))
class GeometryTests(unittest.TestCase):
    def test_sample(self):self.assertTrue(verify_certificate(build_certificate(*BASE),*BASE))
    def test_all_finite(self):self.assertEqual(evaluate()['positive_certificates'],360)
    def test_negative_set(self):self.assertEqual(evaluate()['negative_certificates'],16)
    def test_translation(self):
        cert=build_certificate(*[(x+F(2,3),y-F(5,7)) for x,y in BASE]);self.assertEqual(cert['rotation_product'],['-10','0'])
    def test_before(self):self.assertEqual(build_certificate(*BASE)['ray_order_case'],'before_perpendicular')
    def test_after(self):self.assertEqual(build_certificate(*BASE[:3],(-1,2))['ray_order_case'],'after_perpendicular')
    def test_right(self):self.assertEqual(build_certificate(*BASE[:3],(0,2))['ray_order_case'],'right')
    def test_reflection(self):self.assertEqual(build_certificate(*BASE[:3],(1,-2))['orientation'],'-1')
    def test_zero_c(self):
        with self.assertRaises(ValueError):build_certificate((0,0),(0,0),(-1,0),(1,1))
    def test_zero_d(self):
        with self.assertRaises(ValueError):build_certificate((0,0),(1,0),(0,0),(1,1))
    def test_same_ray(self):
        with self.assertRaises(ValueError):build_certificate((0,0),(1,0),(2,0),(1,1))
    def test_not_line(self):
        with self.assertRaises(ValueError):build_certificate((0,0),(1,0),(-1,1),(1,1))
    def test_a_on_line(self):
        with self.assertRaises(ValueError):build_certificate(*BASE[:3],(3,0))
    def test_a_at_b(self):
        with self.assertRaises(ValueError):build_certificate(*BASE[:3],(0,0))
    def test_float(self):
        with self.assertRaises(TypeError):build_certificate(*BASE[:3],(0.5,1))
    def test_bool(self):
        with self.assertRaises(TypeError):vector((True,1))
    def test_wrong_dimension(self):
        with self.assertRaises(ValueError):vector((1,2,3))
    def test_string(self):
        with self.assertRaises(TypeError):angle_partition('1/4')
    def test_turn_before(self):self.assertEqual(angle_partition(F(1,8))['ordered_sectors'],(F(1,8),F(1,8),F(1,4)))
    def test_turn_after(self):self.assertEqual(angle_partition(F(3,8))['ordered_sectors'],(F(1,4),F(1,8),F(1,8)))
    def test_turn_right(self):self.assertEqual(angle_partition(F(1,4))['second'],F(1,4))
    def test_zero_turn(self):
        with self.assertRaises(ValueError):angle_partition(0)
    def test_half_turn(self):
        with self.assertRaises(ValueError):angle_partition(F(1,2))
    def test_reflex_turn(self):
        with self.assertRaises(ValueError):angle_partition(F(3,4))
    def test_input_binding(self):self.assertFalse(verify_certificate(build_certificate(*BASE),*BASE[:3],(2,2)))
    def test_extra_field(self):
        cert=build_certificate(*BASE);cert['x']=0;self.assertFalse(verify_certificate(cert,*BASE))
    def test_product_identity(self):
        for inputs in positive_cases():
            cert=build_certificate(*inputs);self.assertEqual(cert['rotation_product'],cert['expected_product'])
    def test_angle_count(self):self.assertEqual(evaluate()['angle_partition_cases'],66)
if __name__=='__main__':unittest.main(verbosity=2)
