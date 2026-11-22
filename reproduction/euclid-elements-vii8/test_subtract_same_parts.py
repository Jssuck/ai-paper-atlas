import unittest
from fractions import Fraction as Q
from math import gcd
from subtract_same_parts import Witness,construct,ratios


class PairedSubtractionTests(unittest.TestCase):
    def test_worked(self):
        w=construct(10,15,6,9)
        self.assertEqual(w,Witness(2,3,5,3,(0,5,10),(3,8),(2,2)))
        self.assertEqual(w.gh(),10)
        self.assertEqual(ratios(10,15,6,9),(Q(2,3),)*3)

    def test_grid_and_local_ratios(self):
        count=v_unit=gap_unit=0
        for n in range(3,15):
            for m in range(2,n):
                if gcd(m,n)!=1:
                    continue
                for u in range(2,13):
                    for v in range(1,u):
                        ab,cd,ae,cf=m*u,n*u,m*v,n*v
                        w=construct(ab,cd,ae,cf)
                        self.assertEqual(w.gh(),ab)
                        self.assertEqual(len(w.cuts),m)
                        for start,cut,end,leftover in zip(w.endpoints,w.cuts,w.endpoints[1:],w.leftovers):
                            self.assertTrue(start<cut<end)
                            self.assertEqual((end-start,cut-start,end-cut),(u,v,u-v))
                            self.assertEqual((Q(end-start,cd),Q(cut-start,cf),Q(leftover,cd-cf)),
                                             (Q(1,n),)*3)
                        self.assertEqual(sum(w.leftovers),ab-ae)
                        self.assertEqual(ratios(ab,cd,ae,cf),(Q(m,n),)*3)
                        count+=1
                        v_unit+=v==1
                        gap_unit+=u-v==1
        self.assertEqual((count,v_unit,gap_unit),(3300,550,550))

    def test_unit_in_intermediate_not_given_terms(self):
        w=construct(4,6,2,3)
        self.assertEqual((w.v,w.leftovers),(1,(1,1)))
        with self.assertRaises(ValueError):
            construct(4,6,1,3)

    def test_mismatch_and_same_unit_fraction(self):
        self.assertEqual(ratios(10,15,6,12),(Q(2,3),Q(1,2),Q(4,3)))
        for args in ((10,15,6,12),(12,48,4,16)):
            with self.assertRaises(ValueError):
                construct(*args)

    def test_zero_full_and_invalid(self):
        for args in ((10,15,0,0),(10,15,10,15),(10,15,12,18),(10,15,2.0,3)):
            with self.assertRaises(ValueError):
                construct(*args)


if __name__=='__main__':
    unittest.main()
