from fractions import Fraction
from itertools import product, permutations
from math import prod
import unittest

from named_parts_lcm import Trace, check, construct


def direct(ds):
    for whole in range(1,prod(ds)+1):
        parts = tuple(Fraction(whole,d) for d in ds)
        if all(p.denominator == 1 for p in parts):
            return Trace(whole,tuple(p.numerator for p in parts))
    raise ArithmeticError("product should always work")


class TestParts(unittest.TestCase):
    def test_example(self):
        t = construct(4,6,10)
        self.assertEqual(t,Trace(60,(15,10,6)))
        self.assertNotEqual(sum(t.parts),t.whole)
        self.assertEqual(check(240,4,6,10),Trace(240,(60,40,24)))

    def test_grid(self):
        count = 0
        for ds in product(range(2,11),repeat=3):
            self.assertEqual(construct(*ds),direct(ds))
            count += 1
        self.assertEqual(count,729)
        print("Exact grid:",count)

    def test_missing_part(self):
        with self.assertRaisesRegex(ValueError,"denominator 4"):
            check(30,4,6,10)

    def test_order_and_nesting(self):
        for ds in permutations((4,6,10)):
            self.assertEqual(construct(*ds),Trace(60,tuple(60//d for d in ds)))
        self.assertEqual(construct(3,6,12),Trace(12,(4,2,1)))
        self.assertEqual(construct(7,7,7),Trace(7,(1,1,1)))

    def test_scope(self):
        self.assertEqual(construct(1,4,6,modern=True),Trace(12,(12,3,2)))
        for ds in ((1,4,6),(0,4,6),(-2,4,6),(True,4,6),(2,4.0,6),(2,4)):
            with self.subTest(ds=ds),self.assertRaises(ValueError):
                construct(*ds)
        with self.assertRaises(ValueError):
            check(0,4,6,10)
