from fractions import Fraction
from itertools import product
import unittest

from transfer_cube import CubeTrace, transfer_cube


class TestCubeRatioTransfer(unittest.TestCase):
    def test_fractional_naive_scale_and_reverse(self):
        self.assertEqual(Fraction(8,64),Fraction(1,8))
        self.assertEqual(transfer_cube(8,27,64,216),
                         CubeTrace((8,12,18,27),1,(12,18),(2,3)))
        self.assertEqual(transfer_cube(27,8,216,64),
                         CubeTrace((27,18,12,8),1,(18,12),(3,2)))

    def test_missing_cube_and_wrong_ratio(self):
        self.assertEqual(Fraction(24,81),Fraction(64,216))
        for args in ((24,81,64,216),(8,27,216,64),(8,27,16,54),(8,36,8,27)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                transfer_cube(*args)

    def test_modern_boundaries_and_invalid_input(self):
        self.assertEqual(transfer_cube(1,8,27,216).roots,(1,2))
        self.assertEqual(transfer_cube(8,8,27,27).primitive,(1,1,1,1))
        for args in ((0,0,8,27),(-8,-27,8,27),(True,8,27,216),(1.0,8,27,216)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                transfer_cube(*args)

    def test_large_exact(self):
        s,t = 10**40+1,10**40+3
        result = transfer_cube(s**3,t**3,8*s**3,8*t**3)
        self.assertEqual(result.roots,(s,t))
        self.assertEqual(result.means,(s*s*t,s*t*t))

    def test_bounded_grid(self):
        cubes = {i**3:i for i in range(1,7)}
        accepted = matching_without_cube = mismatch = 0
        for c,d in product(cubes,repeat=2):
            ratio = Fraction(d,c)
            step = Fraction(cubes[d],cubes[c])
            for a,b in product(range(1,101),repeat=2):
                if ratio != Fraction(b,a):
                    mismatch += 1
                elif a not in cubes:
                    matching_without_cube += 1
                else:
                    self.assertIn(b,cubes)
                    out = transfer_cube(a,b,c,d)
                    self.assertEqual(out.roots,(cubes[a],cubes[b]))
                    self.assertEqual(out.means,(a*step,a*step**2))
                    accepted += 1
                    continue
                with self.assertRaises(ValueError):
                    transfer_cube(a,b,c,d)
        self.assertEqual(accepted+matching_without_cube+mismatch,360000)
        print(f"Grid: {accepted} accepted; {matching_without_cube} matching ratio without cube A; {mismatch} ratio mismatches")
