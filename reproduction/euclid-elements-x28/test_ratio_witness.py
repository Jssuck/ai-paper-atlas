from fractions import Fraction as F
from itertools import product
from unittest import TestCase
from ratio_witness import Witness,construct


class TestX28(TestCase):
    def test_examples(self):
        self.assertEqual(construct(1,2,3),Witness(F(2),F(9,2),F(3,2),F(3)))
        self.assertEqual(construct(1,3,2),Witness(F(3),F(4,3),F(2,3),F(2)))
        self.assertEqual(construct(F(1,3),F(2,3),F(1)),Witness(F(2,9),F(1,2),F(3,2),F(1,3)))

    def test_each_premise(self):
        # Each omitted premise leaves the other two intact; show which output fails.
        cases=[((1,4,2),"A:B",F(4)), ((1,2,4),"A:C",F(4)), ((2,1,4),"B:C",F(4))]
        for (a,b,c),pair,expected_square in cases:
            with self.assertRaisesRegex(ValueError,pair):
                construct(a,b,c)
            d4,e4,k,area2=F(a*b),F(a*c*c,b),F(c,b),F(a*c)
            quantities={"A:B":d4,"A:C":area2,"B:C":k}
            self.assertEqual(quantities[pair],expected_square)
        for args in [(0,2,3),(1,2,-3),(1,2,3.0),(True,2,3)]:
            with self.assertRaises(ValueError):
                construct(*args)

    def test_grid(self):
        data=[F(p,q) for p,q in product(range(1,5),repeat=2)]
        # Any numerator/denominator tested below is at most 4^4 before reduction.
        squares={F(m*m,n*n) for m,n in product(range(1,17),repeat=2)}
        valid=0
        for a,b,c in product(data,repeat=3):
            if any(v in squares for v in (a/b,a/c,b/c)):
                with self.assertRaises(ValueError):
                    construct(a,b,c)
                continue
            w=construct(a,b,c)
            self.assertTrue(all(q not in squares for q in (w.d_fourth,w.e_fourth,
                            w.e_over_d_squared,w.rectangle_area_squared)))
            self.assertEqual(w.d_fourth,a*b)
            self.assertEqual(w.e_over_d_squared*b,c)
            self.assertEqual(w.d_fourth*w.e_over_d_squared**2,w.e_fourth)
            self.assertEqual(w.d_fourth*w.e_fourth,w.rectangle_area_squared**2)
            self.assertEqual(w.rectangle_area_squared,a*c)
            valid+=1
        self.assertEqual(valid,1344)
        print(f"Grid: {len(data)**3} ordered representatives; constructed={valid}; excluded={len(data)**3-valid}")
