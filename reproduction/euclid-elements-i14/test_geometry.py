import unittest
from fractions import Fraction as F
from copy import deepcopy
from geometry import *
from cases import run_cases,positives,negatives
BASE=((0,0),(1,0),(1,1),(-1,-1))

class GeometryTests(unittest.TestCase):
    def test_positive_batch(self):self.assertEqual(run_cases()['positive_certificates'],180)
    def test_negative_batch(self):self.assertEqual(run_cases()['negative_certificates'],16)
    def test_scale(self):self.assertEqual(build_certificate(*BASE)['positive_scale'],'1')
    def test_fraction_scale(self):self.assertEqual(build_certificate((0,0),(1,0),(2,2),(-1,-1))['positive_scale'],'1/2')
    def test_reflection(self):self.assertTrue(verify_certificate(build_certificate((0,0),(1,0),(1,-1),(-1,1)),(0,0),(1,0),(1,-1),(-1,1)))
    def test_translation(self):self.assertTrue(build_certificate((3,4),(4,4),(4,5),(2,3))['opposite_rays'])
    def test_rotation(self):self.assertTrue(build_certificate((0,0),(0,1),(-1,1),(1,-1))['opposite_rays'])
    def test_zero_common(self):self.assertRaises(ValueError,build_certificate,(0,0),(0,0),(1,1),(-1,-1))
    def test_zero_c(self):self.assertRaises(ValueError,build_certificate,(0,0),(1,0),(0,0),(-1,-1))
    def test_zero_d(self):self.assertRaises(ValueError,build_certificate,(0,0),(1,0),(1,1),(0,0))
    def test_collinear_common(self):self.assertRaises(ValueError,build_certificate,(0,0),(1,0),(1,0),(-1,-1))
    def test_same_side(self):self.assertRaises(ValueError,build_certificate,(0,0),(1,0),(1,1),(-1,1))
    def test_missing_sum(self):self.assertRaises(ValueError,build_certificate,(0,0),(1,0),(1,1),(1,-1))
    def test_same_side_sum(self):self.assertTrue(inspect_configuration((0,0),(1,0),(1,1),(-1,1))['supplementary'])
    def test_right_overlap(self):self.assertFalse(inspect_configuration((0,0),(1,0),(0,1),(0,2))['opposite_rays'])
    def test_float(self):self.assertRaises(TypeError,vector,(1.0,2))
    def test_bool(self):self.assertRaises(TypeError,vector,(True,2))
    def test_bad_vector(self):self.assertRaises(ValueError,vector,(1,2,3))
    def test_certificate_replay(self):self.assertTrue(verify_certificate(build_certificate(*BASE),*BASE))
    def test_certificate_missing(self):c=build_certificate(*BASE);del c['angle_pairs'];self.assertFalse(verify_certificate(c,*BASE))
    def test_certificate_extra(self):c=build_certificate(*BASE);c['extra']=1;self.assertFalse(verify_certificate(c,*BASE))
    def test_binding(self):self.assertFalse(verify_certificate(build_certificate(*BASE),(0,0),(2,0),(1,1),(-1,-1)))
    def test_angle_converse(self):self.assertTrue(angle_model(F(1,6),F(1,3))['opposite_rays'])
    def test_sixty_one_twenty(self):self.assertFalse(angle_model(F(1,6),F(1,3),1,1)['opposite_rays'])
    def test_ninety_overlap(self):self.assertEqual(angle_model(F(1,4),F(1,4),1,1)['directed_separation'],0)
    def test_angle_zero(self):self.assertRaises(ValueError,angle_model,0,F(1,2))
    def test_angle_side(self):self.assertRaises(ValueError,angle_model,F(1,4),F(1,4),True,-1)
    def test_bool_integer_confusion(self):
        c=build_certificate(*BASE);c['opposite_sides']=1
        self.assertFalse(verify_certificate(c,*BASE))
    def test_non_json_tuple(self):
        c=build_certificate(*BASE);c['angle_product']=tuple(c['angle_product'])
        self.assertFalse(verify_certificate(c,*BASE))
    def test_non_finite_json(self):
        c=build_certificate(*BASE);c['positive_scale']=float('nan')
        self.assertFalse(verify_certificate(c,*BASE))
    def test_algebra(self):self.assertEqual(multiply((2,3),(5,7)),(-11,29))

if __name__=='__main__':unittest.main(verbosity=2)
