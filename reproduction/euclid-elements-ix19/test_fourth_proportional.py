from fractions import Fraction
from itertools import product
from collections import Counter
from math import gcd
import unittest
from fourth_proportional import fourth_proportional,nonunit_inputs


class TestFourth(unittest.TestCase):
    def test_four_cases(self):
        for triple,flags,witness in (
            ((4,6,9),(True,True),None),((8,12,18),(True,False),27),
            ((2,4,3),(False,True),6),((6,4,9),(False,False),6),
            ((6,5,9),(False,False),None),
            ((12,18,27),(True,False),None)):
            row=nonunit_inputs(*triple)
            self.assertEqual((row.continued,row.coprime_endpoints),flags)
            self.assertEqual(row.witness,witness)

    def test_auxiliary_need_not_be_integer(self):
        row=nonunit_inputs(2,4,3)
        self.assertEqual((row.witness,row.auxiliary),(6,Fraction(9,2)))
        self.assertEqual(Fraction(4,3),Fraction(6,row.auxiliary))

    def test_unit_and_invalid(self):
        self.assertEqual(fourth_proportional(1,4,3).witness,12)
        self.assertEqual(nonunit_inputs(6,2,3).witness,1)
        with self.assertRaises(ValueError):
            nonunit_inputs(1,4,3)
        for triple in ((0,4,3),(-1,4,3),(True,4,3),(2.,4,3)):
            with self.subTest(triple=triple),self.assertRaises(ValueError):
                fourth_proportional(*triple)

    def test_order_and_large(self):
        self.assertEqual(nonunit_inputs(6,4,9).witness,6)
        self.assertIsNone(nonunit_inputs(9,4,6).witness)
        m=10**40+3
        self.assertEqual(nonunit_inputs(4*m,6*m,8*m).witness,12*m)

    def test_bounded_additive_oracle(self):
        cases=Counter()
        probes=0
        for a,b,c in product(range(2,19),repeat=3):
            target=b*c
            subtotal=0
            found=None
            for k in range(1,target+1):
                subtotal+=a
                probes+=1
                if subtotal>=target:
                    if subtotal==target:
                        found=k
                    break
            row=nonunit_inputs(a,b,c)
            self.assertEqual(row.witness,found)
            self.assertEqual(a*row.quotient+row.remainder,target)
            self.assertTrue(0<=row.remainder<a)
            flags=(Fraction(a,b)==Fraction(b,c),gcd(a,c)==1)
            self.assertEqual((row.continued,row.coprime_endpoints),flags)
            cases[flags+(found is not None,)]+=1
        self.assertEqual(sum(cases.values()),17**3)
        print(f"Grid: {17**3} triples, {probes} additive probes")
        for geometric,coprime in product((True,False),repeat=2):
            print(f"continued={geometric}, coprime={coprime}: {cases[geometric,coprime,True]} found, {cases[geometric,coprime,False]} absent")
