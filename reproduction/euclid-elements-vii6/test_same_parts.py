import unittest
from fractions import Fraction as Q
from math import gcd
from same_parts import construct,paired_totals,ratios


class SamePartsTests(unittest.TestCase):
    def test_worked(self):
        result=construct(8,12,10,15)
        self.assertEqual((result.m,result.n,result.first_unit,result.second_unit),(2,3,4,5))
        self.assertEqual(paired_totals(result.partial_pairs),(8,10,18))
        self.assertEqual(paired_totals(result.whole_pairs),(12,15,27))

    def test_exact_grid(self):
        count=0
        for n in range(3,15):
            for m in range(2,n):
                if gcd(m,n)!=1:
                    continue
                for g in range(1,12):
                    for h in range(1,12):
                        a,b,c,d=g*m,g*n,h*m,h*n
                        result=construct(a,b,c,d)
                        self.assertEqual(len(result.partial_pairs),m)
                        self.assertEqual(len(result.whole_pairs),n)
                        self.assertEqual(result.partial_pairs,result.whole_pairs[:m])
                        self.assertEqual(paired_totals(result.partial_pairs),(a,c,a+c))
                        self.assertEqual(paired_totals(result.whole_pairs),(b,d,b+d))
                        self.assertEqual(ratios(a,b,c,d),(Q(m,n),)*3)
                        count+=1
        self.assertEqual(count,6050)

    def test_different_reduced_numerator(self):
        self.assertEqual(ratios(6,15,9,15),(Q(2,5),Q(3,5),Q(1,2)))
        with self.assertRaises(ValueError):
            construct(6,15,9,15)

    def test_different_reduced_denominator(self):
        self.assertEqual(ratios(8,12,6,15),(Q(2,3),Q(2,5),Q(14,27)))
        with self.assertRaises(ValueError):
            construct(8,12,6,15)

    def test_unit_components_and_unit_fraction_distinct(self):
        w=construct(2,3,10,15)
        self.assertEqual((w.first_unit,w.second_unit,paired_totals(w.partial_pairs)),(1,5,(2,10,12)))
        with self.assertRaises(ValueError):
            construct(3,12,5,20)

    def test_invalid_input(self):
        for args in ((0,3,2,3),(3,3,2,3),(4,3,2,3),(True,3,2,3),(2,3,2.0,3)):
            with self.assertRaises(ValueError):
                construct(*args)


if __name__=='__main__':
    unittest.main()
