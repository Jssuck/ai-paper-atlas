from fractions import Fraction
from itertools import product
from math import gcd
import unittest
from unit_endpoint_chains import Trace, inspect


def root_search(x,k):
    for b in range(1,x+1):
        v = Fraction(b)**k
        if v >= x:
            return b if v==x else None


class TestUnitEndpoint(unittest.TestCase):
    def test_example(self):
        self.assertEqual(inspect((8,12,18,27)),
            Trace(Fraction(3,2),1,((1,2,4,8),(1,3,9,27))))
        self.assertEqual(inspect((27,18,12,8)).unit_chains,((1,3,9,27),(1,2,4,8)))

    def test_non_coprime(self):
        self.assertIsNone(inspect((16,24,36,54)).unit_chains)
        self.assertIsNone(root_search(16,3))
        self.assertIsNone(root_search(54,3))
        self.assertEqual(root_search(64,3),4)  # noncoprime can also succeed
        self.assertEqual(root_search(216,3),6)
        self.assertIsNone(inspect((64,96,144,216)).unit_chains)

    def test_grid(self):
        yes = no = 0
        for p,q,k,h in product(range(1,6),range(1,6),range(2,5),range(1,4)):
            if gcd(p,q)>1:
                continue
            xs = tuple(h*q**(k-i)*p**i for i in range(k+1))
            t = inspect(xs,modern=True)
            self.assertEqual(t.growth,Fraction(xs[-1],xs[-2]))
            self.assertEqual(t.scale,max(d for d in range(1,min(xs[0],xs[-1])+1)
                                           if xs[0]%d == xs[-1]%d == 0))
            if t.unit_chains:
                for goal,row in zip((xs[0],xs[-1]),t.unit_chains):
                    b = root_search(goal,k)
                    self.assertIsNotNone(b)
                    self.assertEqual(len(row),len(xs))
                    self.assertEqual(row[0],1)
                    self.assertEqual(row[-1],goal)
                    self.assertTrue(all(Fraction(y,x)==b for x,y in zip(row,row[1:])))
                yes += 1
            else:
                no += 1
        self.assertEqual((yes,no),(57,114))
        print(f"Exact grid: {yes+no} chains, {yes} with coprime endpoints, {no} excluded")

    def test_scope(self):
        self.assertEqual(inspect((1,3,9),modern=True).unit_chains,((1,1,1),(1,3,9)))
        self.assertEqual(inspect((1,1,1),modern=True).scale,1)
        for xs in ((1,3,9),(5,5,5),(2,3),(0,0,0),(True,2,4),(2.0,4,8)):
            with self.subTest(xs=xs),self.assertRaises(ValueError):
                inspect(xs)

    def test_not_geometric(self):
        with self.assertRaisesRegex(ValueError,"adjacent"):
            inspect((8,12,19,27))
