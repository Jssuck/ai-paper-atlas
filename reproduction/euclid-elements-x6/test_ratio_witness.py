from fractions import Fraction as F
from itertools import product
import unittest
from ratio_witness import Witness,construct,ratio_witness


class TestWitness(unittest.TestCase):
    def test_worked(self):
        a,b=F(21,10),F(9,5)
        self.assertEqual(ratio_witness(a,b,14,12),Witness(F(3,20),b,F(189,50)))
        self.assertEqual(ratio_witness(a,b,7,6).part,F(3,10))
        with self.assertRaises(ValueError):
            ratio_witness(a,b,7,5)

    def test_porism_and_scale(self):
        self.assertEqual(construct(2,2,1),Witness(F(1),F(1),F(2)))
        self.assertEqual(construct(2,1,1),Witness(F(2),F(2),F(4)))
        w=ratio_witness(6,4,3,2)
        z=ratio_witness(42,28,3,2)
        self.assertEqual(z,Witness(w.part*7,w.constructed*7,w.mean_squared*49))

    def test_invalid(self):
        for args in ((0,1,1,1),(1,0,1,1),(1,1,0,1),(1,1,1,-1),(1.,1,1,1),(1,1,1,True)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                ratio_witness(*args)

    def test_grid(self):
        values=[F(i,3) for i in range(1,9)]
        yes=no=0
        for a,b,m,n in product(values,values,range(1,9),range(1,9)):
            t=construct(a,m,n)
            self.assertEqual(F(a,t.constructed),F(m,n))
            self.assertEqual(t.mean_squared,t.constructed*a)
            if a*n==b*m:
                self.assertEqual(ratio_witness(a,b,m,n),t)
                self.assertEqual((a/t.part,b/t.part),(m,n))
                yes+=1
            else:
                with self.assertRaises(ValueError):
                    ratio_witness(a,b,m,n)
                no+=1
        self.assertEqual(yes+no,4096)
        print(f"Grid: {yes+no} ordered claims; {yes} accepted; {no} rejected")
