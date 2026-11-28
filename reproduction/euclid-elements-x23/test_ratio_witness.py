from fractions import Fraction as F
from itertools import product
from unittest import TestCase
from ratio_witness import Witness,transfer


def signature(q):
    remaining=q.numerator*q.denominator
    factor=2
    while factor*factor<=remaining:
        while remaining%(factor*factor)==0:
            remaining//=factor*factor
        factor+=1
    return remaining


class TestX23(TestCase):
    def test_examples(self):
        self.assertEqual(transfer(6,4,2),Witness(True,F(96),F(3),F(48),F(1,4)))
        self.assertEqual(transfer(6,2,2),Witness(False,F(24),F(3),F(12),F(1,2)))
        self.assertEqual(transfer(F(16,15),F(9,4),F(2,3)),
                         Witness(True,F(27,5),F(8,5),F(81,10),F(4,9)))

    def test_invalid(self):
        for args in [(1,2,3),(F(9,16),2,3),(0,1,1),(2,0,1),
                     (2,1,-1),(2,2.0,1),(True,1,1)]:
            with self.assertRaises(ValueError):
                transfer(*args)

    def test_grid(self):
        data=[F(p,d) for p,d in product(range(1,7),repeat=2)]
        # Direct trial division on a complete finite grid of representatives.
        length=square_only=rejected=0
        for q,k,b in product(data,repeat=3):
            s=signature(q)
            if s==1:
                with self.assertRaises(ValueError):
                    transfer(q,k,b)
                rejected+=1
                continue
            w=transfer(q,k,b)
            self.assertEqual(w.length_premise,signature(k)==1)
            self.assertEqual(signature(w.b_side_fourth),s)
            self.assertEqual(w.ed_squared*b,q)
            self.assertEqual(w.df_squared*b,w.b_side_fourth)
            self.assertEqual(w.ed_over_df**2*w.df_squared,w.ed_squared)
            self.assertEqual(w.ed_over_df*k,1)
            length+=w.length_premise
            square_only+=not w.length_premise
        self.assertEqual(length+square_only+rejected,len(data)**3)
        self.assertEqual((length,square_only,rejected),(8064,28224,10368))
        print(f"Grid: {len(data)**3}; length premise={length}; porism-only={square_only}; rejected={rejected}")
