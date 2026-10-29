import unittest
from fractions import Fraction as F
from geometry import verify

class ExactGeometryTests(unittest.TestCase):
    def test_01_original_interior(self):
        r=verify((2,4),(0,0),(5,0),original_only=True)
        self.assertEqual((r['case'],r['domain']),('interior','original-domain'))
        self.assertEqual((r['lhs'],r['rhs'],r['twice_rectangle']),(45,45,20))
    def test_02_beyond_c(self):
        r=verify((7,3),(0,0),(5,0))
        self.assertEqual((r['case'],r['domain'],r['t']),('beyond-C','modern-extension',F(7,5)))
        self.assertEqual(r['lhs'],83)
    def test_03_at_c(self):
        r=verify((5,3),(0,0),(5,0))
        self.assertEqual((r['case'],r['domain'],r['t']),('at-C','modern-extension',1))
    def test_04_obtuse_a_interior_is_extension(self):
        r=verify((2,1),(0,0),(5,0))
        self.assertEqual((r['case'],r['domain']),('interior','modern-extension'))
    def test_05_right_a_is_extension(self):
        self.assertEqual(verify((2,2),(0,0),(4,0))['domain'],'modern-extension')
    def test_06_strict_rejects_obtuse_a(self):
        with self.assertRaises(ValueError): verify((2,1),(0,0),(5,0),original_only=True)
    def test_07_strict_rejects_endpoint(self):
        with self.assertRaises(ValueError): verify((5,3),(0,0),(5,0),original_only=True)
    def test_08_strict_rejects_external(self):
        with self.assertRaises(ValueError): verify((7,3),(0,0),(5,0),original_only=True)
    def test_09_right_b_rejected(self):
        with self.assertRaises(ValueError): verify((0,4),(0,0),(5,0))
    def test_10_obtuse_b_rejected(self):
        with self.assertRaises(ValueError): verify((-2,4),(0,0),(5,0))
    def test_11_collinear_rejected(self):
        with self.assertRaises(ValueError): verify((2,0),(0,0),(5,0))
    def test_12_coincident_rejected(self):
        for A,B,C in [((0,0),(0,0),(5,0)),((2,4),(0,0),(0,0)),((5,0),(0,0),(5,0))]:
            with self.subTest(A=A,B=B,C=C), self.assertRaises(ValueError): verify(A,B,C)
    def test_13_bool_rejected(self):
        with self.assertRaises(TypeError): verify((True,4),(0,0),(5,0))
    def test_14_float_rejected(self):
        with self.assertRaises(TypeError): verify((2.0,4),(0,0),(5,0))
    def test_15_bad_shape_rejected(self):
        for bad in [(2,), (2,4,6), '24', None]:
            with self.subTest(bad=bad), self.assertRaises(TypeError): verify(bad,(0,0),(5,0))
    def test_16_tiny_positive_projection(self):
        r=verify((F(1,10**100),4),(0,0),(5,0),original_only=True)
        self.assertGreater(r['t'],0)
        self.assertEqual(r['twice_rectangle'],F(1,10**99))
    def test_17_translation(self):
        r=verify((F(7,3),F(18,5)),(F(1,3),F(-2,5)),(F(16,3),F(-2,5)))
        self.assertEqual((r['t'],r['lhs']),(F(2,5),45))
    def test_18_rational_rotation(self):
        def rot(p): return (F(3,5)*p[0]-F(4,5)*p[1],F(4,5)*p[0]+F(3,5)*p[1])
        r=verify(rot((2,4)),rot((0,0)),rot((5,0)))
        self.assertEqual((r['t'],r['lhs']),(F(2,5),45))
    def test_19_scale_and_reflection(self):
        r=verify((F(-4,3),F(8,3)),(0,0),(F(-10,3),0))
        self.assertEqual((r['t'],r['lhs']),(F(2,5),20))
    def test_20_irrational_lengths_rational_product(self):
        r=verify((0,2),(0,0),(1,1))
        self.assertEqual((r['bc2'],r['bd2'],r['rectangle']),(2,2,2))
    def test_21_many_rational_triangles(self):
        count=0
        for x in range(1,10):
            for y in range(1,7):
                r=verify((F(x,3),F(y,7)),(0,0),(2,0))
                self.assertEqual(r['lhs'],r['rhs']); self.assertTrue(all(r['checks'].values())); count+=1
        self.assertEqual(count,54)
    def test_22_projection_and_pythagoras(self):
        r=verify((2,4),(0,0),(5,0))
        self.assertEqual((r['D'],r['bd2'],r['dc2'],r['ad2']),((2,0),4,9,16))
        self.assertEqual(r['ba2'],r['ad2']+r['bd2'])
    def test_23_strict_flag_type(self):
        with self.assertRaises(TypeError): verify((2,4),(0,0),(5,0),original_only=1)

if __name__=='__main__': unittest.main(verbosity=2)
