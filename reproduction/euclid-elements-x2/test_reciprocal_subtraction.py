from fractions import Fraction as F
from itertools import product
from math import gcd,lcm
import unittest

from reciprocal_subtraction import rational_trace,sqrt2_trace,mul


class TestReciprocal(unittest.TestCase):
    def test_same_digits(self):
        rational=rational_trace(F(99,70),1)
        symbolic=sqrt2_trace(7)
        self.assertEqual(len(rational),6)
        self.assertEqual([row[2] for row in rational],[row[2] for row in symbolic[:6]])
        self.assertEqual(rational[-1][-1],0)
        self.assertNotEqual(symbolic[-1][-1],(0,0))

    def test_symbolic_identity(self):
        t=(-1,1)
        self.assertEqual(mul(t,t),(3,-2))
        self.assertEqual(tuple(a+2*b for a,b in zip(mul(t,t),t)),(1,0))
        self.assertEqual(sqrt2_trace(2)[1],((1,0),t,2,(3,-2)))

    def test_bad_domain_and_equality(self):
        for args in ((0,0),(1,2),(2.,1),(True,1)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                rational_trace(*args)
        self.assertEqual(rational_trace(3,3),((3,3,1,0),))
        with self.assertRaises(ValueError):
            sqrt2_trace(0)

    def test_rational_grid(self):
        values=sorted({F(p,d) for p,d in product(range(1,17),range(1,5))})
        pairs=rows_count=contractions=0
        for a,b in product(values,repeat=2):
            if a<b:
                continue
            rows=rational_trace(a,b)
            scale=lcm(a.denominator,b.denominator)
            measure=F(gcd(int(a*scale),int(b*scale)),scale)
            self.assertEqual(rows[-1][1],measure)
            self.assertEqual(rows[-1][-1],0)
            for x,y,q,r in rows:
                self.assertTrue(0<=r<y and x==q*y+r)
                self.assertEqual(gcd(int(x*scale),int(y*scale)),gcd(int(y*scale),int(r*scale)))
                if r:
                    self.assertLess(2*r,x)
                    contractions+=1
            pairs+=1
            rows_count+=len(rows)
        print(f"Grid: {pairs} rational pairs; {rows_count} divisions; {contractions} positive two-index contractions")
