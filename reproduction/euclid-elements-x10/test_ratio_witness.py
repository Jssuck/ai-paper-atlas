from fractions import Fraction as F
from unittest import TestCase
from ratio_witness import Construction, construct


class TestX10(TestCase):
    def test_orientations(self):
        self.assertEqual(construct(1,3,6), Construction(F(2),F(2),F(2)))
        self.assertEqual(construct(1,6,3), Construction(F(1,2),F(1,2),F(1,2)))

    def test_scalings(self):
        self.assertEqual(construct(1,3,6), construct(1,9,18))
        self.assertEqual(construct(F(3,2),3,6), Construction(F(2),F(9,2),F(81,8)))

    def test_grid(self):
        bound = 64
        side_bound = 8  # Reduced side counts cannot exceed sqrt(bound).
        square_ratios = {F(m*m,n*n) for m in range(1,side_bound+1)
                         for n in range(1,side_bound+1)}
        accepted = rejected = 0
        a = F(7,3)
        for b in range(1,bound+1):
            for c in range(1,bound+1):
                if F(c,b) in square_ratios:
                    with self.assertRaises(ValueError):
                        construct(a,b,c)
                    rejected += 1
                else:
                    k = construct(a,b,c)
                    self.assertEqual(k.d_squared*b, a*a*c)
                    self.assertEqual(k.e_fourth*b, a**4*c)
                    self.assertEqual(k.e_fourth, a*a*k.d_squared)
                    self.assertEqual(k.squared_ratio*b, c)
                    accepted += 1
        self.assertEqual((accepted,rejected), (3916,180))
        print(f"Grid: {bound**2} ordered pairs; constructed={accepted}, square ratios rejected={rejected}")

    def test_invalid(self):
        for args in [(1,16,9),(1,2,2),(0,1,2),(1,0,2),(1,1,0),
                     (1.0,1,2),(1,True,2),(1,F(1,2),2)]:
            with self.assertRaises(ValueError):
                construct(*args)
