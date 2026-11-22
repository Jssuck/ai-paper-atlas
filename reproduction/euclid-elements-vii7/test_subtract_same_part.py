import unittest
from fractions import Fraction as Q
from subtract_same_part import Witness,ratios,reconstruct


class SubtractionTests(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(reconstruct(8,24,3,9),Witness(3,5,15,24,15,(-15,0,9,24)))

    def test_grid_construct_match_cancel(self):
        count=unit=0
        for ab in range(3,26):
            for ae in range(2,ab):
                for n in range(2,13):
                    cd,cf=n*ab,n*ae
                    w=reconstruct(ab,cd,ae,cf)
                    g,c,f,d=w.coordinates
                    self.assertTrue(g<c<f<d)
                    self.assertEqual((f-g,c-g,d-f),(w.gf,w.cg,w.fd))
                    self.assertEqual(w.gf,cd)
                    self.assertEqual(w.gf-cf,w.cg)
                    self.assertEqual(w.cg,w.fd)
                    self.assertEqual(ratios(ab,cd,ae,cf),(Q(1,n),)*3)
                    count+=1
                    unit+=w.eb==1
        self.assertEqual((count,unit),(3036,253))

    def test_mismatched_unit_fractions(self):
        self.assertEqual(ratios(8,24,3,12),(Q(1,3),Q(1,4),Q(5,12)))
        with self.assertRaises(ValueError):
            reconstruct(8,24,3,12)

    def test_zero_full_and_invalid(self):
        for args in ((8,24,0,0),(8,24,8,24),(8,24,9,27),(8,24,True,3)):
            with self.assertRaises(ValueError):
                reconstruct(*args)

    def test_residue_unit_not_input_unit(self):
        self.assertEqual(reconstruct(3,9,2,6),Witness(3,1,3,9,3,(-3,0,6,9)))
        with self.assertRaises(ValueError):
            reconstruct(3,9,1,3)
        self.assertEqual(reconstruct(3,9,1,3,True).eb,2)


if __name__=='__main__':
    unittest.main()
