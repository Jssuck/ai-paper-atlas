from itertools import product
import unittest
from even_sum import EvenSum,even_sum


class TestEvenSum(unittest.TestCase):
    def test_partition(self):
        self.assertEqual(even_sum([2,4,6]),EvenSum((1,2,3),6,12))
        self.assertEqual(even_sum([2]),EvenSum((1,),1,2))

    def test_mixed_and_false_converse(self):
        for terms,total in (((2,3),5),((3,5),8),((2,3,5),10)):
            self.assertEqual(sum(terms),total)
            with self.assertRaises(ValueError):
                even_sum(terms)

    def test_modern_boundaries(self):
        for terms in ((),(0,2),(-2,6),(2.0,4),(True,4)):
            with self.subTest(terms=terms), self.assertRaises(ValueError):
                even_sum(terms)
        self.assertEqual(sum((-2,0,6)),4)

    def test_large_exact(self):
        a=10**100+1
        self.assertEqual(even_sum([2*a,2*a+2]),EvenSum((a,a+1),2*a+1,4*a+2))

    def test_bounded_oracle(self):
        accepts=rejected=even_rejected=0
        # Generate reference witnesses by adding two equal positive counts.
        even_table={k+k:k for k in range(1,5)}
        for length in range(1,5):
            for terms in product(range(1,9),repeat=length):
                if any(n not in even_table for n in terms):
                    with self.assertRaises(ValueError):
                        even_sum(terms)
                    rejected+=1
                    even_rejected+=sum(terms) in range(2,33,2)
                    continue
                out=even_sum(terms)
                self.assertEqual(out.term_halves,tuple(even_table[n] for n in terms))
                self.assertEqual(out.half_total+out.half_total,sum(terms))
                self.assertEqual(out.total,sum(terms))
                accepts+=1
        self.assertEqual((accepts,rejected),(340,4340))
        print(f"Grid: {accepts+rejected} lists; {accepts} certified; {rejected} rejected ({even_rejected} with even totals)")
