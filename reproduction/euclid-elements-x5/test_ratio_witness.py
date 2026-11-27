from fractions import Fraction as F
from itertools import product
import unittest
from ratio_witness import ratio_witness


class TestWitness(unittest.TestCase):
    def test_three_signs(self):
        r=ratio_witness(F(21,10),F(9,10),F(3,10))
        self.assertEqual(r.counts,(7,3))
        self.assertEqual([r.compare(*p) for p in ((1,3),(3,7),(1,2))],[(-1,-1),(0,0),(1,1)])

    def test_subdivision_and_scale(self):
        a,b,d=F(21,10),F(9,10),F(3,10)
        original=ratio_witness(a,b,d)
        fine=ratio_witness(a,b,d/4)
        scaled=ratio_witness(13*a,13*b,13*d)
        self.assertEqual(fine.counts,(28,12))
        self.assertEqual(scaled.counts,original.counts)
        for u,v in ((1,3),(3,7),(1,2)):
            self.assertEqual(original.compare(u,v),fine.compare(u,v))
            self.assertEqual(original.compare(u,v),scaled.compare(u,v))

    def test_invalid(self):
        for args in ((0,1,1),(1,-1,1),(1,1,0),(1,1,2),(1.0,2,1),(True,2,1),(2,3,F(2,3))):
            with self.subTest(args=args),self.assertRaises(ValueError):
                ratio_witness(*args)
        for args in ((0,1),(1,False),(1,2.0)):
            with self.assertRaises(ValueError):
                ratio_witness(2,3,1).compare(*args)

    def test_grid(self):
        cases=less=equal=greater=0
        for d,k,l in product((F(1,2),F(2,3),F(5,4)),range(1,9),range(1,9)):
            a,b=k*d,l*d
            r=ratio_witness(a,b,d)
            independent=F(a,b)
            self.assertEqual(F(*r.counts),independent)
            for u,v in product(range(1,9),repeat=2):
                # Compare reduced ratio numerator/denominator to v:u.
                x,y=u*independent.numerator,v*independent.denominator
                sign=-1 if x<y else (0 if x==y else 1)
                self.assertEqual(r.compare(u,v),(sign,sign))
                cases+=1
                less+=sign<0
                equal+=sign==0
                greater+=sign>0
        self.assertEqual(cases,12288)
        print(f"Grid: 192 scaled magnitude pairs; {cases} comparisons; less/equal/greater {less}/{equal}/{greater}")
