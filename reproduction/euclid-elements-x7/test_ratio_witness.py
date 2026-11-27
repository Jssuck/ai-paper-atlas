from fractions import Fraction as F
from itertools import product
from math import isqrt
import unittest
from ratio_witness import Comparison,compare_ratio


class TestComparison(unittest.TestCase):
    def test_sign_controls(self):
        self.assertEqual(compare_ratio(2,1,1,1),Comparison(F(1),1))
        self.assertEqual(compare_ratio(2,1,3,2),Comparison(F(-1),-1))
        self.assertEqual(compare_ratio(2,1,99,70),Comparison(F(-1),-1))
        self.assertEqual(compare_ratio(F(9,4),1,3,2),Comparison(F(0),0))

    def test_rescaled(self):
        original=compare_ratio(2,1,99,70)
        z=F(7,11)
        self.assertEqual(compare_ratio(2*z*z,z,99,70),Comparison(z*z*original.gap,-1))
        self.assertEqual(compare_ratio(2,1,198,140),Comparison(F(-4),-1))

    def test_invalid(self):
        for args in ((0,1,1,1),(1,-1,1,1),(1,1,0,1),(1,1,1,-1),(2.,1,1,1),(2,True,1,1),(2,1,1,True)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                compare_ratio(*args)

    def test_grid(self):
        signs={-1:0,0:0,1:0}
        control_hits=0
        for m,n in product(range(1,129),repeat=2):
            # Independent sign criterion uses floor(sqrt(2*n*n)).
            floor=isqrt(2*n*n)
            exact=floor*floor==2*n*n
            sign=0 if exact and m==floor else (1 if m<=floor else -1)
            self.assertEqual(compare_ratio(2,1,m,n).sign,sign)
            signs[sign]+=1
            r=F(m,n)
            control=0 if r==F(3,2) else (1 if r<F(3,2) else -1)
            self.assertEqual(compare_ratio(F(9,4),1,m,n).sign,control)
            control_hits+=control==0
        self.assertEqual((signs[0],control_hits),(0,42))
        print(f"Grid: 16384 pairs per case; sqrt2 relative to m/n below/equal/above = {signs[-1]}/{signs[0]}/{signs[1]}; positive-control equalities = {control_hits}")
