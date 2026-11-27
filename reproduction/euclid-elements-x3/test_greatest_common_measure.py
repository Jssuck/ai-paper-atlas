import unittest
from fractions import Fraction as F
from math import lcm
from itertools import product
from greatest_common_measure import greatest_common_measure,common_measure_at,is_common_measure


class TestGreatestMeasure(unittest.TestCase):
    def test_delayed(self):
        r=greatest_common_measure(F(21,10),F(9,10))
        self.assertEqual(r.measure,F(3,10))
        self.assertEqual(r.backward_counts,(7,3,1,0))
        self.assertEqual(tuple(row[-1] for row in r.divisions),(F(3,10),0))

    def test_direct_and_equal(self):
        self.assertEqual(greatest_common_measure(12,3).backward_counts,(4,1,0))
        self.assertEqual(greatest_common_measure(3,3).backward_counts,(1,1,0))

    def test_candidates(self):
        r=greatest_common_measure(F(21,10),F(9,10))
        for n in range(1,10):
            c=common_measure_at(r,n)
            self.assertTrue(is_common_measure(r,c))
            self.assertEqual((F(21,10)/c,F(9,10)/c),(7*n,3*n))
        self.assertFalse(is_common_measure(r,F(1,5)))

    def test_invalid(self):
        for a,b in ((0,0),(1,2),(2,0),(2.,1),(True,1)):
            with self.assertRaises(ValueError):
                greatest_common_measure(a,b)

    def test_grid(self):
        values=sorted({F(i,j) for i,j in product(range(1,13),range(1,5))})
        pairs=direct=delayed=probes=0
        for a,b in product(values,repeat=2):
            if a<b:
                continue
            scale=lcm(a.denominator,b.denominator)
            A,B=int(a*scale),int(b*scale)
            r=greatest_common_measure(a,b)
            self.assertEqual(r.measure,F(max(d for d in range(1,B+1) if A%d==B%d==0),scale))
            for k in range(1,2*B+1):
                c=F(k,2*scale)
                self.assertEqual(is_common_measure(r,c),(a/c).denominator==(b/c).denominator==1)
                probes+=1
            pairs+=1
            direct+=len(r.divisions)==1
            delayed+=len(r.divisions)>1
        print(f"Grid: {pairs} pairs; {direct} direct; {delayed} delayed; {probes} candidate checks")
