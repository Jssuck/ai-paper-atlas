from fractions import Fraction
from itertools import product
import unittest
from cube_quotient import QuotientTrace, cube_quotient


class TestCubeQuotient(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(cube_quotient(8,216),
                         QuotientTrace((64,96,144,216),(8,12,18,27),3,False))
        self.assertEqual(cube_quotient(27,216),
                         QuotientTrace((729,486,324,216),(27,18,12,8),2,False))
        self.assertEqual(cube_quotient(8,64).target,(8,8,8,8))

    def test_modern_boundary(self):
        for a,c in ((1,8),(8,8),(1,1)):
            self.assertTrue(cube_quotient(a,c).modern_unit)

    def test_rejected(self):
        for args in ((8,27),(27,8),(8,16),(2,8),(True,8),(0,8),(-1,8),(1.,8)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                cube_quotient(*args)

    def test_large(self):
        x,z = 10**40+1, 10**40+3
        self.assertEqual(cube_quotient(x**3,(x*z)**3).root,z)

    def test_grid(self):
        bound=216
        cubes={k**3:k for k in range(1,7)}
        good=noninteger=noncube=0
        for a,c in product(range(1,bound+1),repeat=2):
            if a not in cubes or c not in cubes:
                noncube+=1
            else:
                step = Fraction(cubes[c],cubes[a]**2)
                b = Fraction(c,a)
                if b.denominator!=1:
                    noninteger+=1
                else:
                    out=cube_quotient(a,c)
                    self.assertEqual(out.root,cubes[b])
                    self.assertEqual(out.source,tuple(a*a*step**j for j in range(4)))
                    self.assertEqual(out.target,tuple(a*step**j for j in range(4)))
                    good+=1
                    continue
            with self.assertRaises(ValueError):
                cube_quotient(a,c)
        self.assertEqual(good+noninteger+noncube,bound**2)
        print(f"Grid: {good} accepted; {noninteger} cube pairs with noninteger quotient; {noncube} noncube pairs")
