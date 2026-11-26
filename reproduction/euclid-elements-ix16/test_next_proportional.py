from fractions import Fraction
from itertools import product
from math import gcd
import unittest

from next_proportional import next_proportional,no_integer_continuation


class TestContinuation(unittest.TestCase):
    def test_worked_and_orientation(self):
        self.assertEqual(no_integer_continuation(2,3),Fraction(9,2))
        self.assertEqual(no_integer_continuation(3,2),Fraction(4,3))

    def test_non_coprime_controls(self):
        self.assertEqual(next_proportional(4,6),9)
        self.assertEqual(next_proportional(6,4),Fraction(8,3))
        for args in ((4,6),(6,4),(4,4)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                no_integer_continuation(*args)

    def test_modern_units(self):
        self.assertEqual(next_proportional(1,4),16)
        self.assertEqual(next_proportional(4,1),Fraction(1,4))
        self.assertEqual(next_proportional(1,1),1)
        for args in ((1,4),(4,1),(1,1)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                no_integer_continuation(*args)

    def test_invalid_and_large(self):
        for args in ((0,3),(2,-1),(True,2),(2,3.0)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                next_proportional(*args)
        a=10**40+1
        self.assertEqual(no_integer_continuation(a,a+1).denominator,a)

    def test_bounded_integer_oracle(self):
        coprime_nonunit = witnesses = probes = 0
        for a,b in product(range(1,33),repeat=2):
            found=[]
            for k in range(1,b*b+1):
                probes+=1
                if a*k==b*b:
                    found.append(k)
            value=next_proportional(a,b)
            self.assertEqual(found,[int(value)] if value.denominator==1 else [])
            witnesses+=bool(found)
            if min(a,b)>=2 and gcd(a,b)==1:
                self.assertEqual(found,[])
                self.assertEqual(no_integer_continuation(a,b).denominator,a)
                coprime_nonunit+=1
        print(f"Grid: 1024 ordered pairs; {probes} integer candidates; {witnesses} with witness; {coprime_nonunit} coprime nonunit pairs")
        self.assertEqual(probes,366080)
