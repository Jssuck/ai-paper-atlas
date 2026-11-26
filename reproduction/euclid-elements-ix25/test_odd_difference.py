from itertools import product
import unittest
from odd_difference import OddDifference,odd_difference


class TestOddDifference(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(odd_difference(18,7),OddDifference(6,12,11,5,False))

    def test_unit_output(self):
        self.assertEqual(odd_difference(4,3),OddDifference(2,2,1,0,True))
        self.assertEqual(odd_difference(18,17).half_without_unit,0)

    def test_domain(self):
        for args in ((8,1),(8,9),(8,8),(9,4),(0,-3),(True,3),(8.0,3)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                odd_difference(*args)
        self.assertEqual(8-1,7)
        self.assertEqual(8-9,-1)

    def test_large(self):
        a=10**100+2
        self.assertEqual(odd_difference(a,a-3).difference,3)

    def test_grid(self):
        pairs=unit=probes=0
        evens={k+k for k in range(1,33)}
        odds={k+k+1 for k in range(1,32)}
        for a,b in product(range(1,65),repeat=2):
            if a<=b or a not in evens or b not in odds:
                with self.assertRaises(ValueError):
                    odd_difference(a,b)
                continue
            cursor=b+1
            half=0
            while cursor<a:
                cursor+=2
                half+=1
                probes+=1
            self.assertEqual(cursor,a)
            self.assertEqual(odd_difference(a,b),OddDifference(b-1,2*half+2,half+half+1,half,half==0))
            pairs+=1
            unit+=half==0
        self.assertEqual((pairs,unit,probes),(496,31,4960))
        print(f"Grid: 4096 ordered pairs, {pairs} witnesses ({unit} unit outputs), 3600 excluded, {probes} pair increments")
