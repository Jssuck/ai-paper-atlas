from fractions import Fraction
from itertools import product
import unittest
from geometric_prefix_sum import Witness,geometric_prefix_sum


class TestPrefix(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(geometric_prefix_sum((8,12,18,27)),Witness((4,6,9),19,Fraction(19,4),38))
        self.assertEqual(geometric_prefix_sum((2,6,18,54)).prefix_sum,26)

    def test_modern_unit(self):
        self.assertEqual(geometric_prefix_sum((1,2,4,8)).prefix_sum,7)

    def test_rejection(self):
        for values in ((1,2),(8,8,8),(27,18,12,8),(8,12,19),(0,3,9),(True,3,9),(1.0,3,9)):
            with self.subTest(values=values),self.assertRaises(ValueError):
                geometric_prefix_sum(values)

    def test_large_exact(self):
        q=10**100+1
        self.assertEqual(geometric_prefix_sum((q,2*q,4*q)).prefix_sum,3*q)

    def test_grid(self):
        valid=invalid=0
        for size in (3,4):
            for terms in product(range(1,21),repeat=size):
                ratios={Fraction(y,x) for x,y in zip(terms,terms[1:])}
                if len(ratios)!=1 or ratios.pop()<=1:
                    with self.assertRaises(ValueError):
                        geometric_prefix_sum(terms)
                    invalid+=1
                    continue
                row=geometric_prefix_sum(terms)
                self.assertEqual(row.prefix_sum,sum(terms[:-1]))
                self.assertEqual(sum(row.adjacent_differences),row.endpoint_difference)
                self.assertEqual(row.subtraction_ratio,Fraction(sum(terms[:-1]),terms[0]))
                self.assertNotEqual(row.prefix_sum,sum(terms))
                valid+=1
        self.assertEqual(valid+invalid,168000)
        print(f"Grid: {valid+invalid} ordered chains; {valid} certified; {invalid} rejected")
