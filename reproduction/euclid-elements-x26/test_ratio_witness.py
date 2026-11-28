from fractions import Fraction as F
from itertools import product
from unittest import TestCase
from ratio_witness import WidthSquare,contradiction,difference_squared


class TestX26(TestCase):
    def test_examples(self):
        self.assertEqual(contradiction(2,1,1),WidthSquare(F(3),F(2),F(2)))
        self.assertEqual(contradiction(F(3,2),F(1,3),F(2,3)),
                         WidthSquare(F(29,12),F(1),F(3,2)))
        self.assertEqual(difference_squared(8,2),F(2))
        self.assertEqual(difference_squared(3,2),WidthSquare(F(5),F(-2),F(6)))

    def test_rejection(self):
        for args in [(4,1,1),(2,0,1),(2,-1,1),(2,1,0),(2,1.0,1),(True,1,1)]:
            with self.assertRaises(ValueError):
                contradiction(*args)
        for args in [(2,2),(2,3),(4,2),(3,1)]:
            with self.assertRaises(ValueError):
                difference_squared(*args)

    def test_grid(self):
        # Independent square-ratio oracle: q,p terms <=16, p*q terms <=256.
        data=sorted({F(p,n) for p,n in product(range(1,17),repeat=2)})
        sq={F(m*m,n*n) for m,n in product(range(1,17),repeat=2)}
        med=[q for q in data if q not in sq]
        pairs=rational_d2=0
        for i,p in enumerate(med):
            for q in med[:i]:
                d2=difference_squared(p,q)
                if p*q in sq:
                    self.assertIsInstance(d2,F)
                    self.assertGreater(d2,0)
                    self.assertEqual((p+q-d2)**2,4*p*q)
                    # Actual d² terms can exceed 256. Generate candidate
                    # integer roots without using the source square test.
                    self.assertNotIn(d2.numerator,{m*m for m in range(1,d2.numerator+1)}
                                     if d2.denominator in {n*n for n in range(1,d2.denominator+1)} else set())
                    rational_d2+=1
                else:
                    self.assertEqual(d2,WidthSquare(p+q,F(-2),p*q))
                pairs+=1
        self.assertEqual((len(med),pairs,rational_d2),(148,10878,370))
        print(f"Pair grid: {len(med)} nonsquares; {pairs} ordered strict pairs; rational nonsquare d²={rational_d2}; radical d²={pairs-rational_d2}")

    def test_certificate_grid(self):
        squares={1,4,9,16}
        count=0
        for q,r,b in product(range(1,17),range(1,5),range(1,5)):
            if q in squares:
                continue
            w=contradiction(q,F(r,3),F(b,5))
            self.assertEqual(w.constant*F(b,5),q+F(r,3)**2)
            self.assertEqual(w.radical_coefficient*F(b,5),F(2*r,3))
            self.assertGreater(w.radical_coefficient,0)
            count+=1
        self.assertEqual(count,192)
        print(f"Certificate grid: {count} positive nonzero radical coefficients")
