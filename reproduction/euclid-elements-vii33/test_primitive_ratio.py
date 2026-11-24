from fractions import Fraction
from itertools import product
import unittest

from primitive_ratio import Trace, matching_scale, primitive


def oracle(xs):
    for first in range(1,xs[0]+1):
        candidate = tuple(Fraction(first,xs[0])*x for x in xs)
        if all(x.denominator == 1 for x in candidate):
            return tuple(x.numerator for x in candidate)
    raise RuntimeError("input itself would be a witness")


class TestPrimitive(unittest.TestCase):
    def test_main(self):
        self.assertEqual(primitive((18,30,45)),Trace((6,10,15),3,(18,6,3)))
        self.assertEqual(primitive((6,10,15)).scale,1)
        self.assertTrue(all(any(x%d == y%d == 0 for d in range(2,min(x,y)+1))
                            for x,y in ((6,10),(6,15),(10,15))))

    def test_grid(self):
        branches = [0,0]
        for length in (2,3,4):
            for xs in product(range(2,8),repeat=length):
                t = primitive(xs)
                self.assertEqual(t.least,oracle(xs))
                self.assertEqual(t.scale,matching_scale(xs,xs))
                self.assertEqual(matching_scale(xs,tuple(x*2 for x in t.least)),2)
                self.assertEqual(matching_scale(xs,t.least),1)
                self.assertEqual(tuple(Fraction(y,xs[0]) for y in xs),
                                 tuple(Fraction(y,t.least[0]) for y in t.least))
                for i,g in enumerate(t.prefix_measures,1):
                    self.assertEqual(g,max(d for d in range(1,min(xs[:i])+1)
                                           if all(x%d == 0 for x in xs[:i])))
                branches[t.scale>1] += 1
        self.assertEqual(sum(branches),1548)
        print("Exact grid: 1548 tuples; scale 1 / scaled:",branches)

    def test_arbitrary_length_and_order(self):
        self.assertEqual(primitive((45,18,30,12,33)).least,(15,6,10,4,11))
        self.assertEqual(matching_scale((45,18,30,12,33),(30,12,20,8,22)),2)
        with self.assertRaises(ValueError):
            matching_scale((18,30,45),(15,10,6))

    def test_boundaries(self):
        self.assertEqual(primitive((9,9,9)).least,(1,1,1))
        self.assertEqual(primitive((3,6)).least,(1,2))
        for xs in ((),(4,),(1,2),(0,2),(2,-3),(True,2),(2,3.0)):
            with self.subTest(xs=xs),self.assertRaises(ValueError):
                primitive(xs)

    def test_wrong_candidate(self):
        for candidate in ((6,10),(0,10,15),(6,10,16),(9,15,22)):
            with self.subTest(candidate=candidate),self.assertRaises(ValueError):
                matching_scale((18,30,45),candidate)
