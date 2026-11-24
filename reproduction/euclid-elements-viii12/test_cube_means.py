from itertools import product
from fractions import Fraction
import unittest
from cube_means import Trace, between, from_sides


def direct(a,b):
    for h in range(min(a,b),max(a,b)+1):
        r = Fraction(h,a)
        k = h*r
        if k.denominator == 1 and k*r == b:
            return a,h,k.numerator,b
    return None


class TestMeans(unittest.TestCase):
    def test_bridge(self):
        self.assertEqual(from_sides(2,3),Trace((2,3),(4,6,9),1,(8,12,18,27)))
        self.assertEqual(from_sides(3,2).chain,(27,18,12,8))
        self.assertEqual(from_sides(4,6).chain,(64,96,144,216))

    def test_examples(self):
        self.assertEqual(between(16,54),Trace((2,3),(4,6,9),2,(16,24,36,54)))
        self.assertIsNone(between(4,16))

    def test_grid(self):
        yes = 0
        for a,b in product(range(1,41),repeat=2):
            t = between(a,b)
            self.assertEqual(t.chain if t else None,direct(a,b))
            if t:
                x,h,k,y = t.chain
                c,d = t.sides
                self.assertEqual(Fraction(x,h),Fraction(h,k))
                self.assertEqual(Fraction(h,k),Fraction(k,y))
                self.assertEqual(Fraction(x,y),Fraction(c,d)**3)
                yes += 1
        print(f"Exact grid: 1600 ordered pairs; {yes} succeed, {1600-yes} fail")

    def test_modern_scope(self):
        self.assertEqual(between(1,27).chain,(1,3,9,27))
        self.assertEqual(between(27,1).chain,(27,9,3,1))
        self.assertEqual(between(7,7).chain,(7,7,7,7))
        for args in ((1,3),(3,3),(True,2),(2,2.0),(2,-3)):
            with self.assertRaises(ValueError):
                from_sides(*args)
        for args in ((0,2),(2,-3),(True,2),(2,3.0)):
            with self.assertRaises(ValueError):
                between(*args)

    def test_big_integer(self):
        c,d = 10**30,10**30+1
        self.assertEqual(between(7*c**3,7*d**3).chain,
                         tuple(7*c**(3-i)*d**i for i in range(4)))
        self.assertIsNone(between(c**3,c**3+1))
