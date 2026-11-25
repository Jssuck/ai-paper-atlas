from fractions import Fraction
from itertools import product
from math import gcd, isqrt
import unittest

from square_ratio import SquareRatio, square_ratio


class TestSquareRatio(unittest.TestCase):
    def test_nonsquare_areas_and_reverse(self):
        self.assertEqual(square_ratio((2,6),(3,9)),SquareRatio((12,18,27),(4,6,9),3,(2,3)))
        self.assertEqual(square_ratio((3,9),(2,6)),SquareRatio((27,18,12),(9,6,4),3,(3,2)))
        self.assertEqual(square_ratio((6,2),(9,3)),square_ratio((2,6),(3,9)))

    def test_equal_area_is_not_a_witness(self):
        self.assertEqual(2*6,1*12)
        with self.assertRaises(ValueError):
            square_ratio((2,6),(1,12))

    def test_modern_boundaries(self):
        self.assertEqual(square_ratio((2,6),(2,6)).primitive,(1,1,1))
        self.assertEqual(square_ratio((1,2),(3,6)).roots,(1,3))

    def test_invalid_inputs(self):
        for left in ((0,2),(-1,3),(True,1),(1.0,2),(3,)):
            with self.subTest(left=left), self.assertRaises(ValueError):
                square_ratio(left,(3,6))

    def test_bounded_oracle(self):
        accepted = rejected = 0
        for a,b,c,d in product(range(1,13),repeat=4):
            step = Fraction(c,a)
            if step != Fraction(d,b):
                rejected += 1
                with self.assertRaises(ValueError):
                    square_ratio((a,b),(c,d))
                continue
            accepted += 1
            result = square_ratio((a,b),(c,d))
            area1,area2 = a*b,c*d
            t = gcd(area1,area2)
            self.assertEqual(result.scale,t)
            self.assertEqual(result.chain,(area1,isqrt(area1*area2),area2))
            self.assertEqual(result.roots,(step.denominator,step.numerator))
            self.assertEqual((area1//t,area2//t),tuple(n*n for n in result.roots))
        self.assertEqual(accepted+rejected,12**4)
        print(f"Grid: {accepted+rejected} ordered quadruples; {accepted} proportional; {rejected} rejected")
