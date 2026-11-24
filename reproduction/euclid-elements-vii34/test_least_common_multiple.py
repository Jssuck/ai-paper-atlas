from itertools import product
from fractions import Fraction
import unittest

from least_common_multiple import Trace, construct, multiple_witness


def direct(a,b):
    return next(m for m in range(max(a,b),a*b+1) if m%a == m%b == 0)


class TestLeastCommonMultiple(unittest.TestCase):
    def test_two_branches(self):
        self.assertEqual(construct(12,18),Trace("noncoprime",6,(2,3),36))
        self.assertEqual(construct(8,15),Trace("coprime",1,(8,15),120))

    def test_boundaries(self):
        self.assertEqual(construct(12,12).least_ratio,(1,1))
        self.assertEqual(construct(12,12).multiple,12)
        self.assertEqual(construct(6,18).least_ratio,(1,3))
        self.assertEqual(construct(18,6).multiple,18)

    def test_witness(self):
        self.assertEqual(multiple_witness(12,18,72),((4,6),2))
        self.assertEqual(multiple_witness(12,18,36),((2,3),1))
        with self.assertRaises(ValueError):
            multiple_witness(12,18,18)

    def test_grid(self):
        counts = {"coprime":0,"noncoprime":0}
        for a,b in product(range(2,31),repeat=2):
            t = construct(a,b)
            self.assertEqual(t.multiple,direct(a,b))
            self.assertEqual(Fraction(*t.least_ratio),Fraction(a,b))
            for c in range(1,a*b+1):
                if c%a == c%b == 0:
                    pair,k = multiple_witness(a,b,c)
                    self.assertEqual(tuple(k*x for x in t.least_ratio),pair)
                    self.assertGreaterEqual(c,t.multiple)
            counts[t.branch] += 1
        self.assertEqual(sum(counts.values()),841)
        print("Exact grid:",counts)

    def test_invalid(self):
        for args in ((1,8),(0,5),(-2,4),(True,4),(2.0,4)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                construct(*args)
        with self.assertRaises(ValueError):
            multiple_witness(12,18,0)
