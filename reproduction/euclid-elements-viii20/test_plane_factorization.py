import unittest
from fractions import Fraction
from math import gcd, isqrt
from itertools import product

from plane_factorization import Factorization, factor_planes


class TestPlaneFactorization(unittest.TestCase):
    def test_worked_and_reverse(self):
        self.assertEqual(factor_planes(18,30,50), Factorization(3,5,6,10))
        self.assertEqual(factor_planes(50,30,18), Factorization(5,3,10,6))

    def test_nonunique_factor_pairs(self):
        r = factor_planes(18,30,50)
        self.assertEqual((r.d*r.f,r.e*r.g),(18,50))
        self.assertNotEqual(((r.d,r.f),(r.e,r.g)), ((6,3),(10,5)))
        self.assertEqual(Fraction(6,10),Fraction(3,5))
        self.assertEqual((6*3,10*5),(18,50))

    def test_modern_boundaries(self):
        self.assertEqual(factor_planes(12,12,12), Factorization(1,1,12,12))
        self.assertEqual(factor_planes(1,3,9), Factorization(1,3,1,3))
        self.assertEqual(factor_planes(3,6,12), Factorization(1,2,3,6))

    def test_rejects(self):
        for terms in [(18,31,50),(3,3,7),(0,0,9),(-1,2,4),(True,3,9),(1.,3,9)]:
            with self.subTest(terms=terms), self.assertRaises(ValueError):
                factor_planes(*terms)

    def test_bounded_grid(self):
        accepted = rejected = 0
        for a,b in product(range(1,101), repeat=2):
            c = isqrt(a*b)
            if c*c != a*b:
                with self.assertRaises(ValueError):
                    factor_planes(a,c,b)
                rejected += 1
                continue
            r = factor_planes(a,c,b)
            t = gcd(a,b)
            self.assertEqual((r.d,r.e),(isqrt(a//t),isqrt(b//t)))
            self.assertEqual((r.f,r.g),(t*r.d,t*r.e))
            self.assertEqual((r.d*r.f,r.e*r.f,r.d*r.g,r.e*r.g),(a,c,c,b))
            self.assertEqual(Fraction(r.d,r.e),Fraction(r.f,r.g))
            self.assertEqual(gcd(r.d,r.e),1)
            accepted += 1
        self.assertEqual(accepted+rejected,10000)
        print(f"Endpoint grid: {accepted+rejected} ordered pairs; {accepted} exact means, {rejected} rejected floors")
