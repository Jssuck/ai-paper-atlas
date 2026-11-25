import unittest
from itertools import product
from fractions import Fraction
from cube_product import CubeProduct, cube_product


class TestCubeProduct(unittest.TestCase):
    def test_worked_and_descending(self):
        self.assertEqual(cube_product(8,27),
                         CubeProduct((8,12,18,27),(64,96,144,216),6,False))
        self.assertEqual(cube_product(27,8),
                         CubeProduct((27,18,12,8),(729,486,324,216),6,False))

    def test_equality_and_modern_unit(self):
        self.assertEqual(cube_product(8,8).root,4)
        self.assertTrue(cube_product(1,27).modern_unit)
        self.assertTrue(cube_product(27,1).modern_unit)
        self.assertEqual(cube_product(1,1).root,1)

    def test_rejects_noncube_even_if_product_is_cube(self):
        self.assertEqual(2*4,2**3)
        for pair in ((2,4),(8,4),(4,8),(0,1),(-1,8),(True,8),(8.0,27)):
            with self.subTest(pair=pair), self.assertRaises(ValueError):
                cube_product(*pair)

    def test_large_exact(self):
        x,y=10**40+1,10**40+3
        self.assertEqual(cube_product(x**3,y**3).root,x*y)

    def test_grid(self):
        bound=216
        endpoint_cubes={n**3:n for n in range(1,7)}
        product_cubes={n**3:n for n in range(1,37)}
        accepted = rejected_cube = rejected_noncube = 0
        for a,b in product(range(1,bound+1),repeat=2):
            if a in endpoint_cubes and b in endpoint_cubes:
                r=cube_product(a,b)
                q=Fraction(endpoint_cubes[b],endpoint_cubes[a])
                self.assertEqual(r.root,product_cubes[a*b])
                self.assertEqual(r.chain,tuple(a*q**i for i in range(4)))
                self.assertEqual(r.lifted,tuple(a*a*q**i for i in range(4)))
                accepted+=1
            else:
                with self.assertRaises(ValueError):
                    cube_product(a,b)
                if a*b in product_cubes:
                    rejected_cube+=1
                else:
                    rejected_noncube+=1
        self.assertEqual(accepted+rejected_cube+rejected_noncube,bound**2)
        print(f"Grid: {accepted} accepted; {rejected_cube} rejected despite cube product; {rejected_noncube} rejected with noncube product")
