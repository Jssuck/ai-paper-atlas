import unittest
from fractions import Fraction as F
from geometry import construct, sqrt_interval, check_interval

class ConstructionTests(unittest.TestCase):
    def test_unequal_integer(self):
        r=construct(9,4)
        self.assertEqual((r['radius'],r['offset'],r['side_squared']),(F(13,2),F(5,2),36))
    def test_equal_branch(self):
        r=construct(F(7,3),F(7,3))
        self.assertEqual(r['branch'],'already_square'); self.assertEqual(r['side'],F(7,3))
        self.assertNotIn('offset',r)
    def test_swapped(self):
        self.assertEqual(construct(9,4),construct(4,9))
    def test_rational(self):
        self.assertEqual(construct(F(3,2),F(2,3))['area'],1)
    def test_irrational_side(self):
        r=construct(2,1); lo,hi=sqrt_interval(r['area'])
        self.assertLess(lo,hi); self.assertTrue(check_interval(2,lo,hi))
    def test_extreme_ratio(self):
        r=construct(10**120,F(1,10**120))
        self.assertEqual(r['side_squared'],1); self.assertTrue(all(r['checks'].values()))
    def test_tiny_area(self):
        r=construct(F(1,10**100),F(1,10**101))
        self.assertGreater(r['side_squared'],0)
    def test_near_equal(self):
        r=construct(1,1+F(1,10**100)); self.assertEqual(r['branch'],'semicircle')
        self.assertEqual(r['offset'],F(1,2*10**100))
    def test_scaling(self):
        for k in (F(1,7),F(5,3),100):
            self.assertEqual(construct(7*k,2*k)['side_squared'],k*k*14)
    def test_grid(self):
        count=0
        for a in range(1,21):
            for b in range(1,21):
                r=construct(F(a,3),F(b,7)); self.assertEqual(r['side_squared'],F(a*b,21)); count+=1
        self.assertEqual(count,400)
    def test_invalid_lengths(self):
        for x in (True,False,1.0,float('nan'),float('inf'),'2',None,1j,[],{}):
            for pair in ((x,1),(1,x)):
                with self.subTest(pair=repr(pair)),self.assertRaises(TypeError):construct(*pair)
    def test_nonpositive(self):
        for x in (0,-1,F(-1,10)):
            for pair in ((x,1),(1,x)):
                with self.subTest(pair=pair),self.assertRaises(ValueError):construct(*pair)
    def test_order_and_circle(self):
        r=construct(8,3)
        self.assertLess(r['B'],r['G']);self.assertLess(r['G'],r['E']);self.assertLess(r['E'],r['F'])
        self.assertEqual((r['E']-r['G'])**2+r['side_squared'],r['radius_squared'])
    def test_wrong_total_semicircle(self):
        self.assertNotEqual(F(9,2)**2-F(9-4,2)**2,9*4)
    def test_wrong_half_difference_as_side(self):
        self.assertNotEqual(F(9-4,2)**2,9*4)
    def test_wrong_arithmetic_mean(self):
        self.assertNotEqual(F(9+4,2)**2,9*4)

class RootTests(unittest.TestCase):
    def test_exact_root(self):
        self.assertEqual(sqrt_interval(1),(1,1))
        self.assertEqual(sqrt_interval(4),(2,2))
    def test_initial_bracket(self):
        self.assertEqual(sqrt_interval(F(1,7),0),(0,1))
        self.assertEqual(sqrt_interval(7,0),(0,7))
    def test_width_bound(self):
        for x in (F(2),F(1,13),F(90,7)):
            for n in (1,7,40):
                lo,hi=sqrt_interval(x,n);self.assertTrue(check_interval(x,lo,hi))
                self.assertLessEqual(hi-lo,max(1,x)/2**n)
    def test_invalid_steps(self):
        for n in (True,1.0,'2'):
            with self.assertRaises(TypeError):sqrt_interval(2,n)
        for n in (-1,10001):
            with self.assertRaises(ValueError):sqrt_interval(2,n)
    def test_invalid_radicand(self):
        for x in (0,-1):
            with self.assertRaises(ValueError):sqrt_interval(x)
        with self.assertRaises(TypeError):sqrt_interval(2.0)
    def test_false_interval(self):
        self.assertFalse(check_interval(2,2,3));self.assertFalse(check_interval(2,-1,2))
        self.assertFalse(check_interval(2,2,1))
    def test_no_float_endpoints(self):
        with self.assertRaises(TypeError):check_interval(2,1.0,2)

if __name__=='__main__':unittest.main()
