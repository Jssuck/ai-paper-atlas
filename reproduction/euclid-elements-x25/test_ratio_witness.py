from fractions import Fraction as F
from itertools import product
from unittest import TestCase
from ratio_witness import Witness,construct


class TestX25(TestCase):
    def test_examples(self):
        self.assertEqual(construct(2,2,1),Witness((F(2),F(4),F(8)),F(4),True))
        self.assertEqual(construct(2,3,2),Witness((F(1),F(3),F(9)),F(6),False))
        self.assertEqual(construct(F(2,3),F(3,2),F(4,5)),
                         Witness((F(5,6),F(5,4),F(15,8)),F(1),True))

    def test_invalid(self):
        for args in [(4,2,1),(2,4,1),(F(9,16),2,1),(2,1,1),(0,2,1),
                     (2,0,1),(2,2,0),(2,-1,1),(2,2.0,1),(True,2,1)]:
            with self.assertRaises(ValueError):
                construct(*args)

    def test_grid(self):
        values=[F(p,d) for p,d in product(range(1,5),repeat=2)]
        # q*k has reduced numerator and denominator at most 16;
        # therefore all possible reduced rational roots appear here.
        squares={F(m*m,n*n) for m,n in product(range(1,5),repeat=2)}
        yes=no=outside=0
        for q,k,b in product(values,repeat=3):
            if q in squares or k in squares:
                with self.assertRaises(ValueError):
                    construct(q,k,b)
                outside+=1
                continue
            w=construct(q,k,b)
            f,g,h=w.width_squares
            self.assertEqual(g*g,f*h)
            self.assertEqual(f*b,q)
            self.assertEqual(h*b,q*k*k)
            self.assertEqual(g*b,w.area_squared)
            self.assertEqual(w.area_rational,q*k in squares)
            yes+=w.area_rational
            no+=not w.area_rational
        self.assertEqual((yes,no,outside),(576,1024,2496))
        print(f"Grid: {len(values)**3} ordered inputs; rational area={yes}; irrational area={no}; excluded={outside}")
