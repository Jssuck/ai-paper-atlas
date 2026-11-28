from fractions import Fraction as F
from math import gcd
from itertools import product
from unittest import TestCase
from ratio_witness import Witness,apply_area


class TestX20(TestCase):
    def test_examples(self):
        self.assertEqual(apply_area(4,6),Witness(F(3,2),F(9),(3,2),F(1,2)))
        self.assertEqual(apply_area(2,F(3,2)),Witness(F(3,4),F(9,8),(3,4),F(1,4)))
        self.assertEqual(apply_area(2,3),Witness(F(3,2),F(9,2),(3,2),F(1,2)))

    def test_scaling(self):
        for k in (F(2),F(1,7),F(7,3)):
            old,new=apply_area(2,3),apply_area(2*k,3*k)
            self.assertEqual(old.breadth_per_base,new.breadth_per_base)
            self.assertEqual(old.measure_per_base,new.measure_per_base)
            self.assertEqual(new.breadth_squared,k*old.breadth_squared)

    def test_grid(self):
        total = integral = 0
        for p,q,m,n in product(range(1,9),repeat=4):
            a = F(p,q)
            # Start from an independently tiled rectangle: a square of side
            # base is n*n tiles, while a rectangle of breadth m tiles is m*n.
            tile = a/(n*n)
            area = m*n*tile
            result = apply_area(a,area)
            self.assertEqual(result.breadth_squared,m*m*tile)
            self.assertEqual(result.breadth_per_base*n,m)
            i,j=result.counts
            self.assertEqual(i*n,j*m)
            self.assertEqual(gcd(i,j),1)
            self.assertEqual(i*result.measure_per_base,result.breadth_per_base)
            self.assertEqual(j*result.measure_per_base,1)
            integral += j==1
            total += 1
        self.assertEqual((total,integral),(4096,1280))
        print(f"Grid: {total} constructed rectangles; integral breadth/base={integral}; other rational={total-integral}")

    def test_invalid(self):
        for pair in [(0,1),(1,0),(-1,2),(2,-1),(1.0,1),(True,1),(1,1.0)]:
            with self.assertRaises(ValueError):
                apply_area(*pair)
