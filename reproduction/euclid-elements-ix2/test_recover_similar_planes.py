from fractions import Fraction
from itertools import product
from math import isqrt
import unittest
from recover_similar_planes import PlaneTrace, recover_similar_planes


def ratio_witnesses(n):
    return {Fraction(x,n//x) for x in range(1,n+1) if n%x == 0}


class TestRecovery(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(recover_similar_planes(50,8),
                         PlaneTrace(400,(2500,1000,400),20,2,(5,2),((5,10),(2,4))))

    def test_reversed(self):
        result = recover_similar_planes(8,50)
        self.assertEqual(result.lifted_chain,(64,160,400))
        self.assertEqual(result.factors,((2,4),(5,10)))

    def test_invalid(self):
        for args in ((6,10),(0,1),(-1,1),(True,1),(4.0,9)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                recover_similar_planes(*args)

    def test_modern_boundaries(self):
        self.assertEqual(recover_similar_planes(1,9).factors,((1,1),(3,3)))
        self.assertEqual(recover_similar_planes(12,12).factors,((1,12),(1,12)))
        self.assertEqual(recover_similar_planes(18,50).factors,((3,6),(5,10)))

    def test_grid(self):
        bound=150
        witnesses = {n: ratio_witnesses(n) for n in range(1,bound+1)}
        yes = no = 0
        for a,b in product(witnesses,repeat=2):
            common = witnesses[a] & witnesses[b]
            root = isqrt(a*b)
            self.assertEqual(bool(common),root*root==a*b)
            if not common:
                with self.assertRaises(ValueError):
                    recover_similar_planes(a,b)
                no += 1
                continue
            r = recover_similar_planes(a,b)
            (x,y),(z,w) = r.factors
            self.assertEqual((x*y,z*w),(a,b))
            self.assertEqual(Fraction(x,y),Fraction(z,w))
            self.assertIn(Fraction(x,y),common)
            self.assertEqual(r.middle,root)
            yes += 1
        self.assertEqual(yes+no,bound**2)
        print(f"Grid: {yes+no} ordered endpoint pairs; {yes} found factor witnesses; {no} rejected")
