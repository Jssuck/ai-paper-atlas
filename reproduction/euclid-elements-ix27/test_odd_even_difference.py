from itertools import product
import unittest
from odd_even_difference import OddDifference,odd_even_difference


class TestOddEvenDifference(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(odd_even_difference(19,8),OddDifference(18,10,11,5,False))

    def test_unit_boundary(self):
        self.assertEqual(odd_even_difference(3,2),OddDifference(2,0,1,0,True))

    def test_invalid(self):
        for args in ((3,1),(3,0),(3,4),(7,7),(4,3),(False,2),(7.,4),(7,-2)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                odd_even_difference(*args)

    def test_large(self):
        a=10**100+1
        self.assertEqual(odd_even_difference(a,a-3).half_without_unit,1)

    def test_independent_grid(self):
        evens={k+k for k in range(1,33)}
        odds={k+k+1 for k in range(1,32)}
        good=unit=steps=bad=0
        for a,b in product(range(1,65),repeat=2):
            if a<=b or a not in odds or b not in evens:
                with self.assertRaises(ValueError):
                    odd_even_difference(a,b)
                bad+=1
                continue
            cursor=b+1
            half=0
            while cursor<a:
                cursor+=2
                half+=1
                steps+=1
            self.assertEqual(cursor,a)
            self.assertEqual(odd_even_difference(a,b),OddDifference(a-1,half+half,half+half+1,half,half==0))
            good+=1
            unit+=half==0
        self.assertEqual((good,unit,bad,steps),(496,31,3600,4960))
        print(f"Grid: {good+bad} pairs; {good} witnesses ({unit} unit outputs); {bad} rejected; {steps} pair increments")
