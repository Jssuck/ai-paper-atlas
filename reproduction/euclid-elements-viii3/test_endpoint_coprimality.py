from fractions import Fraction
from itertools import product
from math import gcd
import unittest

from endpoint_coprimality import Trace, inspect


def search(terms):
    ratio = Fraction(terms[1],terms[0])
    for first in range(1,terms[0]+1):
        row = [Fraction(first)]
        for _ in terms[1:]:
            row.append(row[-1]*ratio)
        if all(x.denominator == 1 for x in row):
            return tuple(x.numerator for x in row)
    raise ArithmeticError("input provides upper bound")


class TestEndpoint(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(inspect((8,12,18,27)),Trace(Fraction(2,3),(8,12,18,27),True,1))
        self.assertEqual(inspect((16,24,36,54)),Trace(Fraction(2,3),(8,12,18,27),False,2))

    def test_grid(self):
        minimal = scaled = 0
        for a,b,n,s in product(range(1,6),range(1,6),range(2,6),range(1,4)):
            if gcd(a,b)>1:
                continue
            terms = tuple(s*a**(n-1-i)*b**i for i in range(n))
            t = inspect(terms,modern=True)
            self.assertEqual(t.least_chain, search(terms))
            self.assertEqual(t.is_least,t.least_chain==terms)
            self.assertEqual(t.endpoint_measure,max(d for d in range(1,min(terms[0],terms[-1])+1)
                                                    if terms[0]%d == terms[-1]%d == 0))
            self.assertEqual(t.is_least,t.endpoint_measure==1)
            minimal += t.is_least
            scaled += not t.is_least
        self.assertEqual((minimal,scaled),(76,152))
        print(f"Exact grid: {minimal} least, {scaled} scaled")

    def test_unit_branches(self):
        for xs in ((1,3,9,27),(27,9,3,1)):
            self.assertTrue(inspect(xs,modern=True).is_least)
        scaled = inspect((9,27,81),modern=True)
        self.assertEqual(scaled,Trace(Fraction(1,3),(1,3,9),False,9))
        self.assertFalse(inspect((5,5,5),modern=True).is_least)
        for xs in ((1,3,9,27),(9,27,81),(5,5,5)):
            with self.subTest(xs=xs),self.assertRaises(ValueError):
                inspect(xs)

    def test_non_geometric(self):
        for xs in ((6,10,15),(8,12,19,27),(1,3,8)):
            with self.subTest(xs=xs),self.assertRaisesRegex(ValueError,"adjacent"):
                inspect(xs,modern=True)

    def test_invalid(self):
        for xs in ((),(3,),(0,3),(-3,9),(True,3),(2.0,3)):
            with self.subTest(xs=xs),self.assertRaises(ValueError):
                inspect(xs,modern=True)
