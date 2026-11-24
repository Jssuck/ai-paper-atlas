from fractions import Fraction
from itertools import product
from math import gcd
import unittest

from join_unit_chains import Trace, join


class TestJoin(unittest.TestCase):
    def test_example(self):
        self.assertEqual(join((1,4,16,64),(1,6,36,216)),
                         Trace((64,96,144,216),Fraction(3,2),8))

    def test_grid(self):
        count = historical = 0
        for a,b,n in product(range(1,8),range(1,8),range(2,6)):
            x,y = tuple(a**i for i in range(n+1)),tuple(b**i for i in range(n+1))
            t = join(x,y,modern=True)
            raw = [Fraction(x[-1])]
            for _ in range(n):
                raw.append(raw[-1]*Fraction(b,a))
            self.assertTrue(all(r.denominator==1 for r in raw))
            self.assertEqual(t.mixed,tuple(r.numerator for r in raw))
            self.assertEqual(t.growth,Fraction(b,a))
            self.assertEqual(t.endpoint_measure,gcd(a,b)**n)
            if min(a,b)>1 and a!=b:
                self.assertEqual(join(x,y),t)
                historical += 1
            count += 1
        self.assertEqual((count,historical),(196,120))
        print(f"Exact grid: {count} chains, {historical} default-domain chains")

    def test_swapped(self):
        self.assertEqual(join((1,6,36,216),(1,4,16,64)).mixed,(216,144,96,64))

    def test_malformed(self):
        for x,y in (((1,2,4),(1,3,9,27)),((1,2),(1,3)),((2,4,8),(1,3,9)),
                    ((1,2,5),(1,3,9)),((1,2,4),(1,3,8)),((1,2,4),(True,3,9)),
                    ((1,2,4),(1,0,9)),((1,2,4),(1,3.0,9))):
            with self.subTest(x=x,y=y),self.assertRaises(ValueError):
                join(x,y,modern=True)

    def test_modern(self):
        for x,y,out in (((1,1,1),(1,3,9),(1,3,9)),((1,2,4),(1,2,4),(4,4,4))):
            with self.assertRaises(ValueError):
                join(x,y)
            self.assertEqual(join(x,y,modern=True).mixed,out)
