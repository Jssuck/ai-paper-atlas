import unittest
from fractions import Fraction as Q
from compound_areas import (SLOPE, area, determinant_area, grid, parallelogram,
                            ratio_chain, three_areas)


class CompoundAreaTests(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(three_areas(6,2,4,5),(Q(48,5),Q(32,5),16))
        self.assertEqual(ratio_chain(6,2,4,5,6),(6,4,10))

    def test_mixed_transfer_and_chain_grid(self):
        cases=chains=0
        for a,b,c,d,direction in grid():
            s,t,u=three_areas(a,b,c,d,direction)
            self.assertEqual(Q(s,t),Q(a,c))
            self.assertEqual(Q(t,u),Q(b,d))
            self.assertEqual(Q(s,u),Q(a,c)*Q(b,d))
            for x,y,expected in ((a,b,s),(c,b,t),(c,d,u)):
                self.assertEqual(determinant_area(parallelogram(x,y,direction,(-2,9))),expected)
            for seed in (1,Q(2,7),3,6,Q(11,2)):
                k,l,m=ratio_chain(a,b,c,d,seed)
                self.assertEqual((Q(k,l),Q(l,m),Q(k,m)),(Q(a,c),Q(b,d),Q(s,u)))
                chains+=1
            cases+=1
        self.assertEqual((cases,chains),(128,640))

    def test_unequal_sine_breaks_side_product(self):
        p=area(parallelogram(6,2,SLOPE))
        q=area(parallelogram(4,5,(Q(5,13),Q(12,13))))
        self.assertEqual(Q(p,q),Q(13,25))
        self.assertNotEqual(Q(p,q),Q(3,5))

    def test_equal_absolute_sine_modern_extension(self):
        p=area(parallelogram(6,2,SLOPE))
        supplementary=(Q(-3,5),Q(4,5))
        for direction in (supplementary,(Q(3,5),Q(-4,5))):
            q=area(parallelogram(4,5,direction))
            self.assertEqual(Q(p,q),Q(3,5))
        # Opposite horizontal component gives a supplementary, not equal, angle.
        self.assertNotEqual(SLOPE[0],supplementary[0])
        self.assertEqual(SLOPE[1],supplementary[1])

    def test_degenerate_rejected(self):
        for args in ((0,4,SLOPE),(6,2,(1,0)),(6,2,(1,1))):
            with self.assertRaises(ValueError):
                parallelogram(*args)
        with self.assertRaises(ValueError):
            ratio_chain(6,2,4,5,0)


if __name__=='__main__':
    unittest.main()
