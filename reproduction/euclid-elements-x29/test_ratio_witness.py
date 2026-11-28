from fractions import Fraction as F
from unittest import TestCase
from ratio_witness import Witness,construct


class TestX29(TestCase):
    def test_examples(self):
        self.assertEqual(construct(1,3,2),Witness(F(5,9),F(4,9),F(2,3)))
        self.assertEqual(construct(2,3,2),Witness(F(10,9),F(8,9),F(2,3)))
        self.assertEqual(construct(F(7,5),2,1),Witness(F(21,20),F(7,20),F(1,2)))

    def test_invalid(self):
        for args in [(1,5,3),(1,2,2),(1,2,3),(1,2,0),(1,2,-1),(0,3,2),
                     (-1,3,2),(1.0,3,2),(1,True,1),(1,3,F(1))]:
            with self.assertRaises(ValueError):
                construct(*args)

    def test_grid(self):
        accepted=rejected=0
        h=F(7,5)
        for n in range(2,65):
            # Independent Pythagorean search without integer square root.
            square_legs={j*j for j in range(1,n)}
            for m in range(1,n):
                if any(j+m*m==n*n for j in square_legs):
                    with self.assertRaises(ValueError):
                        construct(h,n,m)
                    rejected+=1
                    continue
                w=construct(h,n,m)
                self.assertEqual(w.l_squared+w.g_squared,h)
                self.assertEqual(w.g_squared,h*w.g_over_h**2)
                self.assertEqual(w.g_over_h*n,m)
                self.assertEqual(w.l_squared*n*n,h*(n*n-m*m))
                accepted+=1
        self.assertEqual((accepted,rejected),(1962,54))
        print(f"Grid: {accepted+rejected} strict ordered pairs; accepted={accepted}; square controls={rejected}")
