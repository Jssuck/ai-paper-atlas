from fractions import Fraction as F
from math import gcd,lcm
from unittest import TestCase
from ratio_witness import Witness,from_parts,from_whole


def maximum_measure(a,b):
    denominator = lcm(a.denominator,b.denominator)
    return F(gcd(int(a*denominator),int(b*denominator)),denominator)


class TestX15(TestCase):
    def test_nonmaximal_witness(self):
        expected = Witness(F(3,10),(4,6,10))
        self.assertEqual(from_parts(F(3,10),4,6),expected)
        self.assertEqual(from_whole(F(3,10),10,4),expected)
        self.assertEqual(expected.lengths,(F(6,5),F(9,5),F(3)))
        self.assertEqual(maximum_measure(*expected.lengths[:2]), F(3,5))

    def test_grid(self):
        largest = smaller = 0
        for unit in (F(1),F(2,3),F(5,14)):
            for p in range(1,33):
                for r in range(1,33):
                    left = from_parts(unit,p,r)
                    right = from_whole(unit,p+r,p)
                    self.assertEqual(left,right)
                    a,b,c = left.lengths
                    self.assertEqual(c-a,b)
                    maxima = [maximum_measure(x,y) for x,y in [(a,b),(a,c),(b,c)]]
                    self.assertEqual(maxima,[maxima[0]]*3)
                    k = maxima[0]/unit
                    self.assertTrue(k.denominator==1 and k>=1)
                    largest += (k==1)
                    smaller += (k>1)
        self.assertEqual((largest,smaller),(1941,1131))
        print(f"Grid: {largest+smaller} witness triples; maximal={largest}; nonmaximal={smaller}")

    def test_invalid(self):
        for fn, args in [(from_parts,(1,2,0)),(from_parts,(1,-1,2)),
                         (from_whole,(1,2,2)),(from_whole,(1,1,2)),
                         (from_whole,(1,2,0)), (from_whole,(0,2,1)),
                         (from_whole,(1.0,2,1)),(from_parts,(1,True,2))]:
            with self.assertRaises(ValueError):
                fn(*args)

    def test_orientation(self):
        self.assertEqual(from_whole(1,10,6),from_parts(1,6,4))
        self.assertEqual(from_whole(1,10,4),from_parts(1,4,6))
