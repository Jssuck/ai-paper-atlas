import unittest
from fractions import Fraction as F
from geometry import *

S=((0,0),(3,0),(1,2))
R=((5,-2),(5,1),(3,-1))
H=((0,0),(3,0),(1,-2))

class GeometryTests(unittest.TestCase):
    def test_side_order(self): self.assertEqual(sides_squared(S),(9,5,8))
    def test_polarization(self): self.assertEqual(gram_from_sides(sides_squared(S)),gram(S))
    def test_gram(self): self.assertEqual(gram(S),((9,3),(3,5)))
    def test_identity(self): self.assertEqual(certificate(S,S),(((1,0),(0,1)),(0,0)))
    def test_rotation(self): self.assertEqual(certificate(S,R),(((0,-1),(1,0)),(5,-2)))
    def test_reflection(self): self.assertEqual(determinant(certificate(S,H)[0]),-1)
    def test_rotation_orientation(self): self.assertEqual(determinant(certificate(S,R)[0]),1)
    def test_map(self): self.assertTrue(verify_certificate(S,R,*certificate(S,R)))
    def test_bad_translation(self): self.assertFalse(verify_certificate(S,R,certificate(S,R)[0],(0,0)))
    def test_bad_matrix(self): self.assertFalse(verify_certificate(S,R,((2,0),(0,2)),(5,-2)))
    def test_fixed_correspondence(self):
        with self.assertRaises(CorrespondenceMismatch): certificate(S,(S[0],S[2],S[1]))
    def test_degenerate_source(self):
        with self.assertRaises(DegenerateTriangle): certificate(((0,0),(1,0),(2,0)),S)
    def test_degenerate_target(self):
        with self.assertRaises(DegenerateTriangle): certificate(S,((0,0),(1,0),(2,0)))
    def test_repeated_vertex(self):
        with self.assertRaises(DegenerateTriangle): certificate(((0,0),(0,0),(2,0)),S)
    def test_zero_arm(self):
        with self.assertRaises(DegenerateTriangle): angle_signature(((0,0),(0,0),(1,0)))
    def test_float_rejected(self):
        with self.assertRaises(TypeError): triangle(((0.0,0),(1,0),(0,1)))
    def test_bool_rejected(self):
        with self.assertRaises(TypeError): point((True,0))
    def test_wrong_vertex_count(self):
        with self.assertRaises(ValueError): triangle(((0,0),(1,0)))
    def test_fraction_rotation(self):
        m=((F(3,5),F(-4,5)),(F(4,5),F(3,5))); t=(F(2,7),F(-5,9))
        target=tuple(apply(m,t,p) for p in S)
        self.assertEqual(certificate(S,target),(m,t))
    def test_top_angle(self): self.assertEqual(angle_signature(S),angle_signature(R))
    def test_acute_obtuse_sign(self):
        self.assertNotEqual(angle_signature(((0,0),(1,0),(1,1))),angle_signature(((0,0),(1,0),(-1,1))))
    def test_right_angle(self): self.assertEqual(angle_signature(((0,0),(1,0),(0,1))),(0,0))
    def test_two_sides_insufficient(self):
        p=((0,0),(3,0),(0,4)); q=((0,0),(3,0),(F(12,5),F(16,5)))
        self.assertEqual(sides_squared(p)[:2],sides_squared(q)[:2])
        self.assertNotEqual(sides_squared(p)[2],sides_squared(q)[2])
        self.assertNotEqual(angle_signature(p),angle_signature(q))
        with self.assertRaises(CorrespondenceMismatch): certificate(p,q)
    def test_large_exact(self):
        big=10**60; q=tuple((x+big,y-big) for x,y in S)
        self.assertEqual(certificate(S,q)[1],(big,-big))
    def test_reverse_certificate(self): self.assertTrue(verify_certificate(R,S,*certificate(R,S)))

if __name__=='__main__': unittest.main(verbosity=2)
