from fractions import Fraction as F
from unittest import TestCase
from ratio_witness import analyze,Witness


class TestX18(TestCase):
    def test_controls(self):
        self.assertEqual(analyze(5,4),Witness(F(9),(F(4),F(5),F(5,2),F(5,3))))
        self.assertEqual(analyze(3,2),Witness(F(5),None))

    def test_scaling(self):
        for k in (F(3,2),F(1,3),F(19,4)):
            for whole,side in ((5,4),(3,2)):
                base,scaled=analyze(whole,side),analyze(k*whole,k*side)
                self.assertEqual(scaled.gap_squared,k*k*base.gap_squared)
                self.assertEqual(scaled.ratios,base.ratios)

    def test_invalid(self):
        for args in [(1,1),(1,2),(1,0),(0,0),(2,-1),(2,1.),(2,True)]:
            with self.assertRaises(ValueError):
                analyze(*args)

    def test_grid(self):
        # Enumerate doubled smaller part Y; its partner is 2L-Y.
        # If a rational solution exists, d² integer implies d integer,
        # hence the doubled parts are integer too.
        rational=total=0
        for length in range(2,65):
            for side in range(1,length):
                hits = [(2*length-y,y) for y in range(1,length)
                        if (2*length-y)*y==side*side]
                self.assertLessEqual(len(hits),1)
                w=analyze(length,side)
                if not hits:
                    self.assertIsNone(w.ratios)
                    self.assertEqual(w.gap_squared,length**2-side**2)
                else:
                    x,y=hits[0]
                    self.assertEqual(w.gap_squared,F(x-y,2)**2)
                    self.assertEqual(w.ratios,(F(x,y),F(2*length,y),F(length,y),
                                               F(2*length,x-y)))
                    rational+=1
                total+=1
        self.assertEqual((total,rational),(2016,54))
        print(f"Grid: {total} integer inputs; four rational ratios={rational}; none={total-rational}")
