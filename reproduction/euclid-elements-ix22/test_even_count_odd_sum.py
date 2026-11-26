from itertools import product
import unittest

from even_count_odd_sum import Witness, even_count_odd_sum


class TestOddSum(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(even_count_odd_sum((3,5,7,9)), Witness((1,2,3,4),2,12,24))
        self.assertEqual(even_count_odd_sum((3,3)), Witness((1,1),1,3,6))

    def test_odd_count(self):
        for terms in ((3,),(3,5,7),(3,3,3,3,3)):
            with self.subTest(terms=terms), self.assertRaises(ValueError):
                even_count_odd_sum(terms)

    def test_other_domains(self):
        for terms in ((),(1,3),(0,3),(-3,7),(3.0,5),(True,3),(2,4),(3,4)):
            with self.subTest(terms=terms), self.assertRaises(ValueError):
                even_count_odd_sum(terms)
        self.assertEqual(sum((1,3)),4)
        self.assertEqual(sum((-3,7)),4)

    def test_large(self):
        a=10**100+1
        self.assertEqual(even_count_odd_sum((a,a+2)).total_half,a+1)

    def test_independent_grid(self):
        odds={i+i+1 for i in (1,2,3)}
        even_totals={i+i:i for i in range(1,15)}
        yes=no=0
        for length in range(1,5):
            for terms in product(range(1,8),repeat=length):
                if length not in (2,4) or any(n not in odds for n in terms):
                    with self.assertRaises(ValueError):
                        even_count_odd_sum(terms)
                    no+=1
                    continue
                out=even_count_odd_sum(terms)
                pair_halves=tuple(even_totals[a+b] for a,b in zip(terms[::2],terms[1::2]))
                self.assertEqual(sum(pair_halves),out.total_half)
                self.assertEqual(out.total,sum(terms))
                yes+=1
        self.assertEqual((yes,no),(90,2710))
        print(f"Grid: {yes+no} lists, {yes} witnesses, {no} excluded")
