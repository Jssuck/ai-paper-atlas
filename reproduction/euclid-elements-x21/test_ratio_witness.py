from fractions import Fraction as F
from itertools import product
from unittest import TestCase
from ratio_witness import Witness,classify


class TestX21(TestCase):
    def test_examples(self):
        self.assertEqual(classify(2,3),Witness(False,False,(F(1),6),F(6)))
        self.assertEqual(classify(2,8),Witness(True,True,(F(4),1),F(64,4)))
        self.assertEqual(classify(F(2,3),F(8,5)),Witness(False,False,(F(4,15),15),F(16,15)))
        self.assertEqual(classify(F(8,5),F(2,3)),classify(F(2,3),F(8,5)))

    def test_invalid(self):
        for pair in [(0,1),(1,0),(-1,1),(1,1.0),(True,2)]:
            with self.assertRaises(ValueError):
                classify(*pair)

    def test_grid(self):
        inputs=[F(p,q) for p,q in product(range(1,9),repeat=2)]
        # Both a/b and ab have reduced numerator and denominator <=64.
        squares={F(m*m,n*n) for m,n in product(range(1,9),repeat=2)}
        yes=0
        for a,b in product(inputs,repeat=2):
            w=classify(a,b)
            self.assertEqual(w.sides_commensurable,a/b in squares)
            self.assertEqual(w.area_rational,a*b in squares)
            c,d=w.area_radical
            self.assertGreater(c,0)
            self.assertTrue(all(d%(i*i) for i in range(2,d+1) if i*i<=d))
            self.assertEqual(c*c*d,a*b)
            self.assertEqual(w.equal_square_side_fourth,c*c*d)
            yes+=w.area_rational
        self.assertEqual(yes,456)
        print(f"Grid: {len(inputs)**2} ordered input pairs; commensurable/rational={yes}; square-only/irrational={len(inputs)**2-yes}")
