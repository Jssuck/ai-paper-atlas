from fractions import Fraction
from itertools import product
import unittest

from cube_endpoints import cube_endpoint_roots, floor_cuberoot


class TestCubeEndpoints(unittest.TestCase):
    def test_middle_terms_need_not_be_cubes(self):
        self.assertEqual(cube_endpoint_roots(8,12,18,27),(2,3))
        self.assertEqual(cube_endpoint_roots(27,18,12,8),(3,2))

    def test_missing_premise(self):
        for terms in ((24,36,54,81),(8,12,18,28),(8,13,18,27),(8,13,19,27)):
            with self.subTest(terms=terms), self.assertRaises(ValueError):
                cube_endpoint_roots(*terms)

    def test_modern_boundaries_and_invalid_input(self):
        self.assertEqual(cube_endpoint_roots(1,2,4,8),(1,2))
        self.assertEqual(cube_endpoint_roots(27,27,27,27),(3,3))
        for terms in ((0,0,0,0),(-1,2,4,8),(True,2,4,8),(1.0,2,4,8)):
            with self.subTest(terms=terms), self.assertRaises(ValueError):
                cube_endpoint_roots(*terms)

    def test_large_exact(self):
        s,t = 10**40+1,10**40+3
        self.assertEqual(cube_endpoint_roots(s**3,s*s*t,s*t*t,t**3),(s,t))
        self.assertEqual(floor_cuberoot(s**3-1),s-1)
        self.assertEqual(floor_cuberoot(0),0)

    def test_bounded_oracle(self):
        roots = {n**3:n for n in range(1,7)}
        # 216 is the endpoint bound, so reduced cube ratios have roots at most 6.
        steps = {Fraction(y,x):Fraction(roots[y],roots[x]) for x,y in product(roots,repeat=2)}
        accepted = noncube = absent = 0
        for a,d in product(range(1,217),repeat=2):
            step = steps.get(Fraction(d,a))
            if step is None:
                absent += 1
                with self.assertRaises(ValueError):
                    cube_endpoint_roots(a,a,d,d)
                continue
            middle = (a*step,a*step**2)
            self.assertTrue(all(x.denominator == 1 for x in middle))
            args = (a,int(middle[0]),int(middle[1]),d)
            if a not in roots:
                noncube += 1
                with self.assertRaises(ValueError):
                    cube_endpoint_roots(*args)
            else:
                self.assertIn(d,roots)
                self.assertEqual(cube_endpoint_roots(*args),(roots[a],roots[d]))
                accepted += 1
        self.assertEqual(accepted+noncube+absent,216**2)
        print(f"Endpoint grid: {accepted} cube starts, {noncube} noncube starts with integer means, {absent} without two integer means")
