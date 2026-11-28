from fractions import Fraction as F
from itertools import product
from unittest import TestCase
from ratio_witness import Witness,form_rectangle


def square_class(q):
    n=q.numerator*q.denominator
    k=2
    while k*k<=n:
        while n%(k*k)==0:
            n//=k*k
        k+=1
    return n


class TestX24(TestCase):
    def test_examples(self):
        self.assertEqual(form_rectangle(6,2),Witness(F(24),F(1,2),F(24)))
        self.assertEqual(form_rectangle(6,F(1,2)),Witness(F(3,2),F(2),F(3,2)))
        self.assertEqual(form_rectangle(F(16,15),F(9,4)),Witness(F(27,5),F(4,9),F(27,5)))
        self.assertEqual(form_rectangle(6,1),Witness(F(6),F(1),F(6)))

    def test_invalid(self):
        for args in [(F(9,16),1),(1,2),(0,1),(2,0),(-1,1),(2,1.5),(True,1)]:
            with self.assertRaises(ValueError):
                form_rectangle(*args)

    def test_grid(self):
        data=[F(p,d) for p,d in product(range(1,9),repeat=2)]
        accepted=0
        for q,h in product(data,repeat=2):
            tag=square_class(q)
            if tag==1:
                with self.assertRaises(ValueError):
                    form_rectangle(q,h)
                continue
            w=form_rectangle(q,h)
            self.assertEqual(square_class(w.rectangle_area_squared),tag)
            self.assertEqual(w.rectangle_area_squared*w.square_over_rectangle**2,q)
            self.assertEqual(w.equivalent_side_fourth,w.rectangle_area_squared)
            self.assertEqual(form_rectangle(q*h**4,1/h).rectangle_area_squared,w.rectangle_area_squared)
            accepted+=1
        self.assertEqual(accepted,3328)
        print(f"Grid: {len(data)**2} ordered inputs; accepted={accepted}; square controls={len(data)**2-accepted}")
