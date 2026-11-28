from fractions import Fraction as F
from itertools import product
from unittest import TestCase
from ratio_witness import Witness,construct


class TestX30(TestCase):
    def test_examples(self):
        self.assertEqual(construct(1,1,2),Witness(F(1,5),F(4,5),F(1,5),F(4,5)))
        self.assertEqual(construct(F(3,2),1,1),Witness(F(3,4),F(3,4),F(1,2),F(1,2)))
        self.assertEqual(construct(2,2,1),Witness(F(8,5),F(2,5),F(4,5),F(1,5)))

    def test_invalid(self):
        for args in [(1,3,4),(1,4,3),(1,0,2),(1,-1,1),(0,1,1),
                     (-1,1,1),(1.0,1,1),(1,True,1),(1,1,F(1))]:
            with self.assertRaises(ValueError):
                construct(*args)

    def test_grid(self):
        # The reduced ratio-square numerator and denominator never exceed 8192.
        squares={j*j for j in range(1,91)}
        h=F(7,5)
        accepted=rejected=0
        for m,n in product(range(1,65),repeat=2):
            if m*m+n*n in squares:
                with self.assertRaises(ValueError):
                    construct(h,m,n)
                rejected+=1
                continue
            w=construct(h,m,n)
            self.assertEqual(w.l_squared+w.g_squared,h)
            self.assertEqual(w.l_squared*n*n,w.g_squared*m*m)
            for term,square_ratio in ((w.l_squared,w.l_over_h_squared),(w.g_squared,w.g_over_h_squared)):
                self.assertEqual(term,h*square_ratio)
                self.assertFalse(square_ratio.numerator in squares and square_ratio.denominator in squares)
            accepted+=1
        self.assertEqual((accepted,rejected),(4022,74))
        print(f"Grid: {accepted+rejected} ordered leg pairs; accepted={accepted}; square controls={rejected}")
