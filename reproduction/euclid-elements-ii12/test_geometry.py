import unittest
from fractions import Fraction as F
from geometry import construct, normalized, squared_distance

class GeometryTests(unittest.TestCase):
    def test_integer_example(self):
        r=normalized(5,2,3)
        self.assertEqual((r['AB2'],r['AC2'],r['BC2'],r['correction']),(13,25,58,20))
    def test_fractional_example(self):
        r=normalized(F(3,2),F(1,3),F(4,5))
        self.assertEqual(r['correction'],1)
        self.assertEqual(r['BC2'],F(3601,900))
    def test_grid(self):
        values=[F(1,7),F(1,2),F(1),F(3),F(11,2)]
        count=0
        for c in values:
            for d in values:
                for h in values:
                    for sign in [-1,1]:
                        self.assertTrue(all(normalized(c,d,sign*h)['checks'].values())); count+=1
        self.assertEqual(count,250)
    def test_translation(self):
        r=construct((7,-4),(5,-1),(12,-4))
        self.assertEqual(r['D'],(5,-4)); self.assertEqual(r['BC2'],58)
    def test_rational_rotation(self):
        def rot(p):return (F(3,5)*p[0]-F(4,5)*p[1],F(4,5)*p[0]+F(3,5)*p[1])
        r=construct(rot((0,0)),rot((-2,3)),rot((5,0)))
        self.assertEqual(r['BC2'],58);self.assertEqual(r['correction'],20)
    def test_reflection(self):self.assertEqual(normalized(5,2,-3)['BC2'],58)
    def test_scale(self):
        r=normalized(10,4,6);self.assertEqual(r['BC2'],232);self.assertEqual(r['correction'],80)
    def test_irrational_length_product(self):
        r=construct((0,0),(-2,0),(1,1))
        self.assertEqual(r['AC2'],2);self.assertEqual(r['AD2'],2);self.assertEqual(r['AC_times_AD'],2)
    def test_wrong_sign_counterexample(self):
        r=normalized(5,2,3);self.assertNotEqual(r['BC2'],r['AB2']+r['AC2']-r['correction'])
    def test_missing_double_counterexample(self):
        r=normalized(5,2,3);self.assertNotEqual(r['BC2'],r['AB2']+r['AC2']+r['AC_times_AD'])
    def test_right_boundary_rejected(self):
        with self.assertRaises(ValueError):construct((0,0),(0,3),(5,0))
    def test_acute_rejected(self):
        with self.assertRaises(ValueError):construct((0,0),(2,3),(5,0))
    def test_collinear_rejected(self):
        with self.assertRaises(ValueError):construct((0,0),(-2,0),(5,0))
    def test_repeated_base_rejected(self):
        with self.assertRaises(ValueError):construct((0,0),(-2,3),(0,0))
    def test_zero_negative_dimensions(self):
        for args in [(0,2,3),(-1,2,3),(5,0,3),(5,-1,3),(5,2,0)]:
            with self.assertRaises(ValueError):normalized(*args)
    def test_float_bool_string_rejected(self):
        for x in [1.0,True,'1']:
            with self.assertRaises(TypeError):normalized(x,2,3)
    def test_bad_point_rejected(self):
        for p in [None,(0,),[0,0,0],'00']:
            with self.assertRaises(TypeError):construct(p,(-2,3),(5,0))
    def test_tiny_positive_excess(self):
        r=normalized(1,F(1,10**30),1);self.assertGreater(r['correction'],0)
    def test_huge_exact(self):
        r=normalized(10**60,2,3);self.assertEqual(r['correction'],4*10**60)
    def test_height_does_not_change_excess(self):
        self.assertEqual(normalized(5,2,1)['correction'],normalized(5,2,100)['correction'])

if __name__=='__main__':unittest.main()
