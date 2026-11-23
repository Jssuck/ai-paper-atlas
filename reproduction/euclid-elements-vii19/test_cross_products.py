from fractions import Fraction
from itertools import product
import unittest

from cross_products import Trace, check


class TestCross(unittest.TestCase):
    def test_equal(self):
        self.assertEqual(check(4,6,10,15), Trace(40,60,60,(2,3),(2,3),True,True))

    def test_unequal(self):
        self.assertEqual(check(4,6,10,16), Trace(40,64,60,(2,3),(5,8),False,False))

    def test_grid(self):
        counts = {True:0, False:0}
        for a,b,c,d in product(range(2,11), repeat=4):
            t = check(a,b,c,d)
            g,e,f = a*c,a*d,b*c
            self.assertEqual((t.g,t.e,t.f),(g,e,f))
            self.assertEqual(Fraction(c,d),Fraction(g,e))
            self.assertEqual(Fraction(a,b),Fraction(g,f))
            self.assertEqual(Fraction(*t.first),Fraction(a,b))
            self.assertEqual(Fraction(*t.second),Fraction(c,d))
            self.assertEqual(t.ratios_equal,Fraction(a,b)==Fraction(c,d))
            self.assertEqual(t.products_equal,a*d==b*c)
            self.assertEqual(t.ratios_equal,t.products_equal)
            counts[t.ratios_equal] += 1
        self.assertEqual(sum(counts.values()),6561)
        self.assertGreater(counts[True],0)
        self.assertGreater(counts[False],0)
        print("Exact grid:",counts)

    def test_equal_reverse_boundaries(self):
        self.assertTrue(check(6,4,15,10).ratios_equal)
        self.assertTrue(check(4,4,9,9).products_equal)
        self.assertEqual(Fraction(1,2),Fraction(3,6))
        for args in ((1,2,3,6),(0,2,3,6),(4,0,3,6),(4,6,3.0,6),(True,2,3,6)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                check(*args)

    def test_zero_denominator_does_not_define_ratios(self):
        a,b,c,d = 4,0,6,0
        self.assertEqual(a*d,b*c)
        for x,y in ((a,b),(c,d)):
            with self.assertRaises(ZeroDivisionError):
                Fraction(x,y)
        self.assertEqual(Fraction(0,2),Fraction(0,9))
        self.assertEqual(Fraction(0,2),Fraction(0,3))  # fixed zero not injective


if __name__ == "__main__":
    unittest.main()
