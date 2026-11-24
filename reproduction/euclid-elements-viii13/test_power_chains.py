from fractions import Fraction
from itertools import product
from math import gcd
import unittest

from power_chains import construct


class TestPowerChains(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(construct((4,6,9),2).stitched,(16,24,36,54,81))
        self.assertEqual(construct((4,6,9),3).stitched,(64,96,144,216,324,486,729))
        self.assertEqual(construct((8,12,18,27),2).extracted,(64,144,324,729))
        self.assertEqual(construct((8,12,18,27),3).extracted,(512,1728,5832,19683))

    def test_grid(self):
        count=0
        for u,v,n,s,p in product(range(1,5),range(1,5),range(3,6),range(1,4),(2,3)):
            if gcd(u,v)!=1:
                continue
            xs=tuple(s*u**(n-1-i)*v**i for i in range(n))
            t=construct(xs,p,modern=True)
            oracle=tuple(xs[0]**p*Fraction(v,u)**k for k in range((n-1)*p+1))
            self.assertEqual(t.stitched,oracle)
            self.assertEqual(t.extracted,tuple(x**p for x in xs))
            for i,row in enumerate(t.local):
                self.assertEqual(row,oracle[i*p:(i+1)*p+1])
            count+=1
        self.assertEqual(count,198)
        print("Exact grid:",count,"input/power combinations")

    def test_scaling_reversal(self):
        for p in (2,3):
            t=construct((4,6,9),p)
            self.assertEqual(construct((9,6,4),p).stitched,t.stitched[::-1])
            self.assertEqual(construct((8,12,18),p).stitched,tuple(2**p*x for x in t.stitched))

    def test_non_geometric(self):
        with self.assertRaisesRegex(ValueError,"adjacent"):
            construct((4,7,9),2)
        self.assertNotEqual(49**2,16*81)

    def test_scope(self):
        self.assertEqual(construct((1,3,9),2,modern=True).extracted,(1,9,81))
        self.assertEqual(construct((5,5,5),3,modern=True).extracted,(125,125,125))
        for xs,k in (((1,3,9),2),((2,2,2),2),((2,3),2),((0,2,4),2),
                     ((2,4,8),True),((2,4,8),4),((2,4.0,8),3)):
            with self.subTest(xs=xs,k=k),self.assertRaises(ValueError):
                construct(xs,k)
