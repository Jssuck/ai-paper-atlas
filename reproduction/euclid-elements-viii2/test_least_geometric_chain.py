from fractions import Fraction
from itertools import product
import unittest

from least_geometric_chain import Trace, construct


def direct(a,b,n):
    step = Fraction(b,a)
    upper = a**(n-1)  # Unreduced powers already give an integer chain.
    for first in range(1,upper+1):
        values = tuple(first*step**j for j in range(n))
        if all(x.denominator == 1 for x in values):
            return tuple(x.numerator for x in values)
    raise ArithmeticError("search exhausted a guaranteed witness")


class TestConstruction(unittest.TestCase):
    def test_example(self):
        self.assertEqual(construct(2,3,3),Trace((2,3),(4,6,9)))
        self.assertEqual(construct(2,3,4),Trace((2,3),(8,12,18,27)))

    def test_grid(self):
        count = historical = 0
        for a,b,n in product(range(1,7),range(1,7),range(2,6)):
            t = construct(a,b,n,modern=True)
            self.assertEqual(t.terms,direct(a,b,n))
            self.assertEqual(t.terms,tuple(t.bases[0]**(n-1-i)*t.bases[1]**i for i in range(n)))
            self.assertEqual(tuple(Fraction(x,y) for x,y in zip(t.terms,t.terms[1:])),
                             (Fraction(a,b),)*(n-1))
            if min(t.bases) > 1:
                self.assertEqual(construct(a,b,n),t)
                historical += 1
            count += 1
        self.assertEqual(count,144)
        print(f"Exact grid: {count} chains, {historical} nonunit-base cases")

    def test_unreduced(self):
        a,b = 4,6
        self.assertEqual((a*a,a*b,b*b),(16,24,36))
        self.assertEqual(construct(a,b,3).terms,(4,6,9))
        self.assertEqual(construct(6,4,3).terms,(9,6,4))

    def test_modern_scope(self):
        self.assertEqual(construct(4,4,4,modern=True).terms,(1,1,1,1))
        self.assertEqual(construct(2,4,3,modern=True).terms,(1,2,4))
        self.assertEqual(construct(3,1,3,modern=True).terms,(9,3,1))
        for values in ((4,4,4),(2,4,3),(3,1,3)):
            with self.subTest(values=values),self.assertRaises(ValueError):
                construct(*values)

    def test_invalid(self):
        for values in ((0,3,3),(-2,3,3),(True,3,3),(2,3.0,3),(2,3,1),(2,3,3.0)):
            with self.subTest(values=values),self.assertRaises(ValueError):
                construct(*values,modern=True)
