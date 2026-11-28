from fractions import Fraction as F
from itertools import product
from unittest import TestCase
from ratio_witness import Witness,construct


class TestX32(TestCase):
    def test_examples(self):
        self.assertEqual(construct(25,3,21),Witness(F(75),F(1323,25),F(63),F(21,25),F(4,25),True))
        self.assertEqual(construct(2,3,1),Witness(F(6),F(3,2),F(3),F(1,2),F(1,2),False))
        self.assertEqual(construct(F(2,7),F(3,7),F(1,7)),Witness(F(6,49),F(3,98),F(3,49),F(1,2),F(1,2),False))

    def test_invalid(self):
        for args in [(4,1,2),(4,2,1),(3,4,1),(1,2,3),(2,3,2),
                     (2,3,0),(2,-3,1),(2,3.0,1),(True,3,1)]:
            with self.assertRaises(ValueError):
                construct(*args)

    def test_grid(self):
        data=range(1,17)
        squares={i*i for i in range(1,17)}
        yes=no=excluded=0
        for a,b,c in product(data,repeat=3):
            if a<=c or any(v in squares for v in (a*b,a*c,b*c)):
                with self.assertRaises(ValueError):
                    construct(a,b,c)
                excluded+=1
                continue
            w=construct(a,b,c)
            self.assertEqual(w.gap_commensurable,a*(a-c) in squares)
            self.assertEqual(w.d_fourth,a*b)
            self.assertEqual(w.area_squared,b*c)
            self.assertEqual(w.d_fourth*w.e_fourth,(b*c)**2)
            self.assertEqual(w.e_over_d_squared*a,c)
            self.assertEqual(w.e_over_d_squared**2*w.d_fourth,w.e_fourth)
            self.assertEqual(w.gap_ratio_squared,F(a-c,a))
            yes+=w.gap_commensurable
            no+=not w.gap_commensurable
        self.assertEqual((yes,no,excluded),(86,1282,2728))
        print(f"Grid: {yes+no+excluded}; gap commensurable={yes}; gap incommensurable={no}; rejected={excluded}")
