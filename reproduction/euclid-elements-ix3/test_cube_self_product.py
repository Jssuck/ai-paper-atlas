from fractions import Fraction
from math import isqrt
import unittest

from cube_self_product import CubeSquareTrace, cube_self_product


class TestCubeSelfProduct(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(cube_self_product(8),
                         CubeSquareTrace((1,2,4,8),(8,16,32,64),4,False))
        self.assertEqual(cube_self_product(27).root,9)

    def test_modern_unit(self):
        self.assertEqual(cube_self_product(1),
                         CubeSquareTrace((1,1,1,1),(1,1,1,1),1,True))

    def test_invalid(self):
        for a in (2,4,63,65,0,-8,True,8.0):
            with self.subTest(a=a), self.assertRaises(ValueError):
                cube_self_product(a)

    def test_large_exact(self):
        c=10**40+3
        self.assertEqual(cube_self_product(c**3).root,c*c)

    def test_bounded_grid(self):
        roots={r**3:r for r in range(1,101)}
        # Independently find cubes that are squares by checking a square root.
        cube_squares={}
        for r in range(1,10001):
            n=r**3
            a=isqrt(n)
            if a*a==n and a<=10000:
                cube_squares[a]=r
        accepted=rejected=0
        for a in range(1,10001):
            if a not in roots:
                self.assertNotIn(a,cube_squares)
                with self.assertRaises(ValueError):
                    cube_self_product(a)
                rejected+=1
                continue
            r=cube_self_product(a)
            self.assertEqual(r.root,cube_squares[a])
            for chain in (r.unit_chain,r.scaled_chain):
                self.assertEqual([Fraction(y,x) for x,y in zip(chain,chain[1:])],[roots[a]]*3)
            accepted+=1
        self.assertEqual(accepted+rejected,10000)
        print(f"Grid: {accepted} cubes with cube-square witness; {rejected} noncubes rejected")
