from fractions import Fraction
from itertools import product
from math import gcd, prod
import unittest
from cube_ratio import CubeRatio, cube_ratio


class TestCubeRatio(unittest.TestCase):
    def test_worked_and_reversed(self):
        r = cube_ratio((2,4,6),(3,6,9))
        self.assertEqual(r,CubeRatio((48,72,108,162),(8,12,18,27),6,(2,3)))
        self.assertEqual(cube_ratio((3,6,9),(2,4,6)),
                         CubeRatio(r.chain[::-1],r.primitive[::-1],6,(3,2)))

    def test_equal_volume_is_not_witness(self):
        self.assertEqual(prod((2,4,6)),prod((2,3,8)))
        with self.assertRaises(ValueError):
            cube_ratio((2,4,6),(2,3,8))

    def test_modern_boundaries(self):
        self.assertEqual(cube_ratio((2,4,6),(2,4,6)).primitive,(1,1,1,1))
        self.assertEqual(cube_ratio((1,2,3),(2,4,6)).roots,(1,2))

    def test_invalid(self):
        for side in ((1,2),(True,2,3),(0,2,3),(-1,2,3),(1.0,2,3)):
            with self.subTest(side=side), self.assertRaises(ValueError):
                cube_ratio(side,(2,4,6))

    def test_grid(self):
        accepted = rejected = 0
        for sides in product(range(1,7),repeat=6):
            left,right = sides[:3],sides[3:]
            steps = {Fraction(y,x) for x,y in zip(left,right)}
            if len(steps) != 1:
                with self.assertRaises(ValueError):
                    cube_ratio(left,right)
                rejected += 1
                continue
            step = steps.pop()
            r = cube_ratio(left,right)
            a,b = prod(left),prod(right)
            self.assertEqual(r.chain,tuple(a*step**i for i in range(4)))
            t = gcd(a,b)
            self.assertEqual(r.scale,t)
            self.assertEqual((a//t,b//t),tuple(x**3 for x in r.roots))
            self.assertEqual(Fraction(b,a),step**3)
            accepted += 1
        self.assertEqual(accepted+rejected,6**6)
        print(f'Grid: {accepted+rejected} ordered sextuples; {accepted} proportional; {rejected} rejected')
