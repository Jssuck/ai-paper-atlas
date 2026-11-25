from fractions import Fraction
from itertools import product
from math import isqrt
import unittest
from similar_plane import Trace, construct


class TestPlane(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(construct(4,6,6,9),Trace((24,36,54),36,Fraction(3,2)))
        self.assertEqual(construct(6,9,4,6).chain,(54,36,24))

    def test_grid(self):
        accepted = rejected = 0
        for c,d,e,f in product(range(1,9),repeat=4):
            a,b = c*d,e*f
            candidate = isqrt(a*b)
            if Fraction(c,d) != Fraction(e,f):
                with self.assertRaises(ValueError):
                    construct(c,d,e,f,modern=True)
                rejected += 1
                continue
            t = construct(c,d,e,f,modern=True)
            self.assertEqual(t.chain,(a,candidate,b))
            self.assertEqual(candidate*candidate,a*b)
            self.assertEqual(t.alternate_middle,candidate)
            self.assertEqual((Fraction(candidate,a),Fraction(b,candidate)),(t.growth,)*2)
            self.assertEqual(Fraction(b,a),t.growth**2)
            accepted += 1
        print(f"Exact grid: {accepted+rejected} quadruples; {accepted} similar, {rejected} nonsimilar")

    def test_integer_mean_does_not_fix_factor_pairs(self):
        self.assertEqual(isqrt((2*8)*(4*9)),24)
        self.assertNotEqual(8*4,24)
        self.assertNotEqual(2*9,8*4)
        with self.assertRaisesRegex(ValueError,"similar"):
            construct(2,8,4,9)
        self.assertEqual(construct(4,4,6,6).chain,(16,24,36))

    def test_boundaries(self):
        self.assertEqual(construct(1,2,2,4,modern=True).chain,(2,4,8))
        self.assertEqual(construct(3,4,3,4,modern=True).chain,(12,12,12))
        for xs in ((1,2,2,4),(3,4,3,4)):
            with self.subTest(xs=xs), self.assertRaises(ValueError):
                construct(*xs)

    def test_invalid(self):
        for xs in ((0,4,2,4),(-1,2,1,2),(True,2,3,6),(2.0,4,3,6)):
            with self.subTest(xs=xs),self.assertRaises(ValueError):
                construct(*xs,modern=True)
