from fractions import Fraction
from itertools import product
from math import isqrt
import unittest
from square_product import ProductTrace, square_product


class TestSquareProduct(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(square_product((3,6),(2,4)),
                         ProductTrace((18,12,8),(324,216,144),12))

    def test_reverse_and_joint_side_swap(self):
        self.assertEqual(square_product((2,4),(3,6)),
                         ProductTrace((8,12,18),(64,96,144),12))
        self.assertEqual(square_product((6,3),(4,2)),square_product((3,6),(2,4)))

    def test_bad_witnesses(self):
        for left,right,expected in (((3,6),(1,8),True),((2,3),(2,5),False)):
            n = left[0]*left[1]*right[0]*right[1]
            self.assertEqual(isqrt(n)**2==n,expected)
            with self.assertRaises(ValueError):
                square_product(left,right)

    def test_modern_boundaries_and_invalid_inputs(self):
        self.assertEqual(square_product((1,2),(3,6)).root,6)
        self.assertEqual(square_product((3,6),(3,6)).root,18)
        for left in ((0,1),(-1,2),(2.0,3),(True,2),(2,)):
            with self.subTest(left=left), self.assertRaises(ValueError):
                square_product(left,(3,6))

    def test_grid(self):
        passed = nonsimilar_square = nonsimilar_nonsquare = 0
        for a,b,c,d in product(range(1,13),repeat=4):
            first,last = a*b,c*d
            n = first*last
            root = isqrt(n)
            step = Fraction(c,a)
            if step != Fraction(d,b):
                with self.assertRaises(ValueError):
                    square_product((a,b),(c,d))
                if root**2 == n:
                    nonsimilar_square += 1
                else:
                    nonsimilar_nonsquare += 1
                continue
            self.assertEqual(root**2,n)
            out = square_product((a,b),(c,d))
            self.assertEqual(out.root,root)
            self.assertEqual(out.plane_chain,tuple(first*step**i for i in range(3)))
            self.assertEqual(out.lifted_chain,tuple(first**2*step**i for i in range(3)))
            passed += 1
        self.assertEqual(passed+nonsimilar_square+nonsimilar_nonsquare,12**4)
        print(f"Grid: {passed} certified; {nonsimilar_square} rejected square products; {nonsimilar_nonsquare} rejected nonsquare products")
