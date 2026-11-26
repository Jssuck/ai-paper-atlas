from itertools import product
from math import gcd
import unittest
from doubling_coprime import common_divisors,doubled_coprime,transfer_double_measure


class TestDoubling(unittest.TestCase):
    def test_coprime(self):
        self.assertEqual(doubled_coprime(15,8),16)
        self.assertEqual(common_divisors(15,16),())

    def test_common_divisor_transport_outside_original_premise(self):
        self.assertEqual(common_divisors(45,30),(3,5,15))
        self.assertEqual(common_divisors(45,60),(3,5,15))
        self.assertEqual(transfer_double_measure(45,30,15),2)
        with self.assertRaises(ValueError):
            doubled_coprime(45,30)

    def test_even_counterexample(self):
        self.assertEqual(common_divisors(4,3),())
        self.assertEqual(common_divisors(4,6),(2,))
        with self.assertRaises(ValueError):
            doubled_coprime(4,3)

    def test_invalid(self):
        for args in ((1,3),(3,1),(3,0),(3,-1),(True,3),(3.,4)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                doubled_coprime(*args)
        for args in ((45,30,7),(45,30,1),(45,30,9),(4,3,2)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                transfer_double_measure(*args)

    def test_grid(self):
        pairs=coprime=noncoprime=transfers=0
        for a,b in product(range(3,65,2),range(2,65)):
            g,gd=gcd(a,b),gcd(a,2*b)
            self.assertEqual(g,gd)
            before=common_divisors(a,b)
            after=common_divisors(a,2*b)
            self.assertEqual(before,after)
            self.assertEqual(max(before,default=1),g)
            for d in after:
                self.assertEqual(transfer_double_measure(a,b,d),b//d)
                transfers+=1
            if g==1:
                self.assertEqual(doubled_coprime(a,b),2*b)
                coprime+=1
            else:
                with self.assertRaises(ValueError):
                    doubled_coprime(a,b)
                noncoprime+=1
            pairs+=1
        self.assertEqual(pairs,1953)
        print(f"Grid: {pairs} odd/nonunit pairs; {coprime} coprime; {noncoprime} noncoprime; {transfers} transported divisors")
