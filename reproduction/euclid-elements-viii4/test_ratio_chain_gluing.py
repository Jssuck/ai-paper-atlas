from fractions import Fraction
from itertools import product
from math import gcd,prod
import unittest

from ratio_chain_gluing import Step, Trace, construct


def direct(ratios):
    cumulative = [Fraction(1)]
    for a,b in ratios:
        cumulative.append(cumulative[-1]*Fraction(b,a))
    for first in range(1,prod(a for a,_ in ratios)+1):
        xs = tuple(first*x for x in cumulative)
        if all(x.denominator == 1 for x in xs):
            return tuple(x.numerator for x in xs)
    raise ArithmeticError("product of all antecedents should give a candidate")


class TestGluing(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(construct(((2,3),(5,7),(3,4))),
                         Trace((10,15,21,28),(Step(15,5,3,(10,15,21)),Step(21,1,7,(10,15,21,28)))))
        self.assertEqual(construct(((2,3),(5,7),(4,5))).terms,(40,60,84,105))

    def test_grid(self):
        counts = [0,0]
        pairs = tuple(product(range(1,4),repeat=2))
        for ds in product(pairs,repeat=3):
            t = construct(ds,modern=True)
            self.assertEqual(t.terms,direct(ds))
            for i,s in enumerate(t.steps,2):
                self.assertEqual(s.prefix,direct(ds[:i]))
                counts[s.prefix_scale>1] += 1
        self.assertEqual(sum(counts),1458)
        print("Exact grid: 729 chains; bridge steps with/without resizing:",counts[1],counts[0])

    def test_endpoint_control(self):
        t = construct(((3,5),(2,3)))
        self.assertEqual(t.terms,(6,10,15))
        self.assertEqual(gcd(t.terms[0],t.terms[-1]),3)

    def test_reverse_unreduced(self):
        ds = ((6,4),(14,10),(4,3))
        self.assertEqual(construct(ds).terms,direct(ds))
        forward = ((2,3),(5,7),(3,4))
        self.assertEqual(construct(tuple((b,a) for a,b in reversed(forward))).terms,
                         tuple(reversed(construct(forward).terms)))

    def test_scope(self):
        self.assertEqual(construct(((1,1),(2,4)),modern=True).terms,(1,1,2))
        self.assertEqual(construct(((2,3),)).terms,(2,3))
        for ds in ((),((1,2),),((3,3),),((2,4),),((True,3),),((2.0,3),),((0,3),)):
            with self.subTest(ds=ds),self.assertRaises(ValueError):
                construct(ds)
