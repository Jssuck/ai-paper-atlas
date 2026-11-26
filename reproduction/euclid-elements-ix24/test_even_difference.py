from itertools import product
import unittest
from even_difference import Difference,even_difference


class TestEvenDifference(unittest.TestCase):
    def test_worked_and_minimal(self):
        self.assertEqual(even_difference(18,8),Difference(9,4,5,10))
        self.assertEqual(even_difference(4,2),Difference(2,1,1,2))

    def test_modern_contrasts(self):
        for a,b in ((8,8),(8,18),(8,0),(8,-2)):
            with self.subTest(a=a,b=b),self.assertRaises(ValueError):
                even_difference(a,b)
            self.assertEqual(a-b,2*(a//2-b//2))

    def test_invalid(self):
        for a,b in ((10,3),(9,4),(9,3),(8,False),(8,2.0),(True,0)):
            with self.subTest(a=a,b=b),self.assertRaises(ValueError):
                even_difference(a,b)
        self.assertEqual(9-3,6)  # odd-minus-odd is not an IX.24 premise

    def test_large_exact(self):
        a=10**100+2
        self.assertEqual(even_difference(a,a-2).remainder_half,1)

    def test_bounded_oracle(self):
        certified=rejected=probes=0
        paired={k+k:k for k in range(1,33)}
        for a,b in product(range(1,65),repeat=2):
            if a<=b or a not in paired or b not in paired:
                with self.assertRaises(ValueError):
                    even_difference(a,b)
                rejected+=1
                continue
            # Count whole pairs until the smaller number reaches the larger.
            cursor,k=b,0
            while cursor<a:
                cursor+=2
                k+=1
                probes+=1
            self.assertEqual(cursor,a)
            out=even_difference(a,b)
            self.assertEqual(out,Difference(paired[a],paired[b],k,a-b))
            certified+=1
        self.assertEqual((certified,rejected,probes),(496,3600,5456))
        print(f"Grid: {certified+rejected} ordered pairs; {certified} certified; {rejected} rejected; {probes} pair increments")
