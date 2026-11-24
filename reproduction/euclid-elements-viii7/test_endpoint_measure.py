from fractions import Fraction
from itertools import product
from math import gcd
import unittest

from endpoint_measure import Trace, inspect


class TestEndpoint(unittest.TestCase):
    def test_forward_premise(self):
        self.assertEqual(inspect((5,15,45,135)),Trace(Fraction(3),3,Fraction(27),True,True))

    def test_direction_and_ascending(self):
        self.assertEqual(inspect((24,12,6,3)),Trace(Fraction(1,2),3,Fraction(1,8),False,False))
        self.assertEqual(inspect((8,12,18,27)),Trace(Fraction(3,2),3,Fraction(27,8),False,False))
        self.assertTrue(inspect((3,6,12,24)).measures_last)
        self.assertEqual(24%3,0)

    def test_grid(self):
        counts = [0,0]
        for u,v,k,s in product(range(1,7),range(1,7),range(2,6),range(1,4)):
            if gcd(u,v) != 1:
                continue
            xs = tuple(s*u**(k-i)*v**i for i in range(k+1))
            t = inspect(xs,modern=True)
            self.assertEqual(t.measures_second,xs[1]%xs[0]==0)
            self.assertEqual(t.measures_last,xs[-1]%xs[0]==0)
            self.assertEqual(t.measures_second,t.measures_last)
            self.assertEqual(t.endpoint_growth,Fraction(xs[-1],xs[0]))
            self.assertEqual(t.endpoint_growth.denominator,u**k)
            counts[t.measures_last] += 1
        self.assertEqual(counts,[204,72])
        print("Exact grid: 276 chains, last not measured/measured:",counts)

    def test_nonconstant_countercontrol(self):
        self.assertEqual(6%2,0)
        self.assertNotEqual(3%2,0)
        with self.assertRaisesRegex(ValueError,"adjacent"):
            inspect((2,3,6))

    def test_modern_and_invalid(self):
        for xs in ((5,5,5),(1,3,9)):
            with self.assertRaises(ValueError):
                inspect(xs)
            self.assertTrue(inspect(xs,modern=True).measures_last)
        for xs in ((2,6),(0,2,4),(False,2,4),(2,4.0,8)):
            with self.subTest(xs=xs),self.assertRaises(ValueError):
                inspect(xs,modern=True)
