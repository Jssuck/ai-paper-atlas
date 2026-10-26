"""Executable finite checks, not a proof of universal correctness."""
import unittest
from fractions import Fraction as F
from euclid_i1 import Q3, point, distance2, orientation, construct, certificate, enumerate_grid, examples


class ExactArithmetic(unittest.TestCase):
    def test_normalizes_coefficients(self): self.assertEqual(Q3(2, F(2, 4)), Q3(F(2), F(1, 2)))
    def test_sqrt_square(self): self.assertEqual(Q3(0, 1) * Q3(0, 1), Q3(3))
    def test_product(self): self.assertEqual(Q3(1, 2) * Q3(3, 4), Q3(27, 10))
    def test_add_subtract(self): self.assertEqual(Q3(1, 2) + Q3(3, 4) - Q3(4, 5), Q3(0, 1))
    def test_conjugate_product(self): self.assertEqual(Q3(2, 1) * Q3(2, -1), Q3(1))
    def test_scale(self): self.assertEqual(Q3(2, 3).scale(F(1, 2)), Q3(1, F(3, 2)))
    def test_rational_signs(self): self.assertEqual([Q3(x).sign() for x in [-2, 0, 2]], [-1, 0, 1])
    def test_irrational_signs(self): self.assertEqual([Q3(0, x).sign() for x in [-2, 2]], [-1, 1])
    def test_opposed_signs(self): self.assertEqual([Q3(a, b).sign() for a, b in [(1,-1),(2,-1),(-1,1),(-2,1)]], [-1,1,1,-1])
    def test_same_signs(self): self.assertEqual([Q3(1,1).sign(), Q3(-1,-1).sign()], [1,-1])
    def test_no_float(self):
        for v in [0.5, True, '1/2', None]:
            with self.assertRaises(TypeError): Q3(v)
    def test_field_axioms_finite(self):
        vals = [Q3(a,b) for a in range(-2,3) for b in range(-2,3)]
        for x in vals:
            for y in vals:
                self.assertEqual(x*y, y*x)
                self.assertEqual((x+y)*Q3(1,1), x*Q3(1,1)+y*Q3(1,1))
                self.assertEqual((-x).sign(), -x.sign())


class Construction(unittest.TestCase):
    def test_unit_vertices(self): self.assertEqual(construct((0,0),(1,0)), ((Q3(F(1,2)),Q3(0,F(1,2))), (Q3(F(1,2)),Q3(0,F(-1,2)))))
    def test_vertical_base(self): self.assertTrue(all(certificate((0,0),(0,2),c)['accepted'] for c in construct((0,0),(0,2))))
    def test_rational_base(self): self.assertTrue(all(certificate((F(1,3),F(-2,5)),(F(7,4),F(3,2)),c)['accepted'] for c in construct((F(1,3),F(-2,5)),(F(7,4),F(3,2)))))
    def test_reverse_swaps_branches(self): self.assertEqual(construct((1,2),(3,4)), tuple(reversed(construct((3,4),(1,2)))))
    def test_translation(self):
        c = construct((0,0),(1,0))[0]
        self.assertEqual(construct((2,-3),(3,-3))[0], (c[0]+Q3(2),c[1]+Q3(-3)))
    def test_distance_symmetry(self): self.assertEqual(distance2(point((1,2)),point((3,4))), distance2(point((3,4)),point((1,2))))
    def test_orientation(self):
        a,b=(0,0),(2,1)
        self.assertEqual([orientation(point(a),point(b),c).sign() for c in construct(a,b)], [1,-1])
    def test_degenerate_rejected(self):
        with self.assertRaises(ValueError): construct((1,2),(1,2))
    def test_degenerate_certificate_rejected(self): self.assertFalse(certificate((0,0),(0,0),point((0,0)))['accepted'])
    def test_single_circle_insufficient(self):
        c=certificate((0,0),(1,0),point((0,1)))
        self.assertTrue(c['first_circle']); self.assertFalse(c['second_circle']); self.assertFalse(c['accepted'])
    def test_off_circle_rejected(self): self.assertFalse(certificate((0,0),(1,0),point((0,2)))['accepted'])
    def test_collinear_rejected(self): self.assertFalse(certificate((0,0),(1,0),point((F(1,2),0)))['accepted'])
    def test_bad_endpoints(self):
        for x in [(0,), (0,1,2), 'ab', (0.1,0), (True,0)]:
            with self.assertRaises(TypeError): construct(x,(1,0))
    def test_bad_certificate(self):
        with self.assertRaises(TypeError): certificate((0,0),(1,0),(0,1))
    def test_all_grid(self): self.assertEqual(enumerate_grid(), {'integer_grid_points':25,'ordered_distinct_bases':600,'triangles_checked':1200,'violations':0})
    def test_rational_obligation(self): self.assertEqual(examples()['rational_plane_obligation']['y_squared'], '3/4')


if __name__ == '__main__': unittest.main(verbosity=2)
