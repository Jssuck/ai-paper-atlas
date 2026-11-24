from fractions import Fraction
from itertools import product
from math import gcd
import unittest

from forward_measure import inspect


class TestForwardMeasure(unittest.TestCase):
    def test_descending(self):
        xs = (24,12,6,3)
        t = inspect(xs)
        self.assertTrue(t.antecedent)
        self.assertFalse(any(flag for _,_,flag in t.forward))
        self.assertTrue(all(xs[i]%xs[j] == 0 for i,j,_ in t.forward))

    def test_ascending(self):
        self.assertTrue(inspect((8,12,18,27)).antecedent)
        self.assertFalse(inspect((5,15,45,135)).antecedent)
        self.assertTrue(all(flag for _,_,flag in inspect((5,15,45,135)).forward))

    def test_grid(self):
        counts = [0,0]
        pairs = 0
        for a,b,n,s in product(range(1,7),range(1,7),range(3,7),range(1,4)):
            if gcd(a,b) != 1:
                continue
            xs = tuple(s*a**(n-1-i)*b**i for i in range(n))
            t = inspect(xs,modern=True)
            self.assertEqual(t.growth,Fraction(xs[1],xs[0]))
            self.assertEqual(t.antecedent,xs[1]%xs[0] != 0)
            self.assertEqual(len(t.forward),n*(n-1)//2)
            for i,j,flag in t.forward:
                self.assertEqual(flag,xs[j]%xs[i] == 0)
                self.assertEqual(Fraction(xs[j],xs[i]).denominator,a**(j-i))
                pairs += 1
            counts[t.antecedent] += 1
        print("Exact grid:",sum(counts),"chains; antecedent false/true:",counts,"forward pairs:",pairs)

    def test_modern(self):
        self.assertTrue(all(f for _,_,f in inspect((5,5,5),modern=True).forward))
        self.assertTrue(all(f for _,_,f in inspect((1,3,9),modern=True).forward))
        for xs in ((5,5,5),(1,3,9)):
            with self.assertRaises(ValueError):
                inspect(xs)

    def test_invalid(self):
        for xs in ((8,9),(8,12,19),(0,3,9),(True,3,9),(2.0,4,8)):
            with self.subTest(xs=xs),self.assertRaises(ValueError):
                inspect(xs,modern=True)
