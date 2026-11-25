from fractions import Fraction
import unittest

from square_cube import CubeTrace, cube_from_square


class TestCubeFromSquare(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(cube_from_square(8),CubeTrace((64,128,256,512),(8,16,32,64),2,False))
        self.assertEqual(cube_from_square(27),CubeTrace((729,2187,6561,19683),(27,81,243,729),3,False))

    def test_modern_unit(self):
        self.assertEqual(cube_from_square(1),CubeTrace((1,)*4,(1,)*4,1,True))

    def test_rejects(self):
        for a in (2,4,16,63,65,0,-8,True,8.0):
            with self.subTest(a=a), self.assertRaises(ValueError):
                cube_from_square(a)

    def test_large(self):
        root=10**40+3
        self.assertEqual(cube_from_square(root**3).root,root)

    def test_grid(self):
        bound=10_000
        cubes={n**3:n for n in range(1,22)}
        square_cube_table={r**3 for r in range(1,465)}
        good=bad=0
        for a in range(1,bound+1):
            self.assertEqual(a in cubes, a*a in square_cube_table)
            if a*a not in square_cube_table:
                with self.assertRaises(ValueError):
                    cube_from_square(a)
                bad+=1
                continue
            out=cube_from_square(a)
            self.assertEqual(out.root,cubes[a])
            k=Fraction(cubes[a])
            self.assertEqual(out.source,tuple(a*a*k**i for i in range(4)))
            self.assertEqual(out.target,tuple(a*k**i for i in range(4)))
            good+=1
        self.assertEqual(good+bad,bound)
        print(f'Grid: {good} cube-square inputs accepted; {bad} rejected')
