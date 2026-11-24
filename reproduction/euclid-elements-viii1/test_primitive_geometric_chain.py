from fractions import Fraction
from itertools import product
from math import gcd
import unittest

from primitive_geometric_chain import Trace, inspect


def direct(terms):
    length = len(terms)
    step = Fraction(terms[1],terms[0])
    for i in range(1, terms[0]+1):
        values = tuple(i*step**j for j in range(length))
        if all(x.denominator == 1 for x in values):
            return tuple(x.numerator for x in values)
    raise ArithmeticError("the input itself is a candidate")


class TestChain(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(inspect((8,12,18,27)),Trace(Fraction(3,2),1,(8,12,18,27),True))
        self.assertEqual(inspect((16,24,36,54)),Trace(Fraction(3,2),2,(8,12,18,27),False))

    def test_grid(self):
        entered = excluded = 0
        for u,v,scale,n in product(range(1,6),range(1,6),range(1,4),range(2,6)):
            if gcd(u,v) != 1:
                continue
            xs = tuple(scale*u**(n-1-i)*v**i for i in range(n))
            if min(xs) < 2:
                continue
            t = inspect(xs)
            self.assertEqual(t.least_by_vii33,direct(xs))
            self.assertEqual(t.adjacent,Fraction(v,u))
            self.assertEqual(t.endpoint_measure,max(d for d in range(1,min(xs[0],xs[-1])+1)
                                                    if xs[0]%d == xs[-1]%d == 0))
            if t.enters_viii1:
                self.assertEqual(t.least_by_vii33,xs)
                entered += 1
            else:
                excluded += 1
        self.assertGreater(entered,0)
        self.assertGreater(excluded,0)
        print(f"Exact grid: {entered+excluded} chains, {entered} coprime endpoints, {excluded} outside endpoint premise")

    def test_directions(self):
        self.assertEqual(inspect((27,18,12,8)).adjacent,Fraction(2,3))
        self.assertTrue(inspect((27,18,12,8)).enters_viii1)
        self.assertEqual(inspect((5,5,5)).least_by_vii33,(1,1,1))
        self.assertFalse(inspect((5,5,5)).enters_viii1)

    def test_not_constant_adjacent(self):
        self.assertEqual(gcd(6,15),3)
        for xs in ((6,10,15),(8,13,27)):
            with self.subTest(xs=xs),self.assertRaisesRegex(ValueError,"adjacent"):
                inspect(xs)

    def test_invalid(self):
        for xs in ((),(8,),(1,2,4),(0,2,4),(-2,4,8),(True,2,4),(2.0,4,8)):
            with self.subTest(xs=xs),self.assertRaises(ValueError):
                inspect(xs)
