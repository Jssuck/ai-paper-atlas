import itertools
import unittest
from fractions import Fraction
from math import prod

from similar_solid import solid_chain


class TestSolid(unittest.TestCase):
    def test_worked(self):
        r = solid_chain((2, 4, 6), (3, 6, 9))
        self.assertEqual(r.kml, (8, 12, 18))
        self.assertEqual(r.anob, (48, 72, 108, 162))
        self.assertEqual(r.step, Fraction(3, 2))

    def test_reversed(self):
        r = solid_chain((3, 6, 9), (2, 4, 6))
        self.assertEqual(r.kml, (18, 12, 8))
        self.assertEqual(r.anob, (162, 108, 72, 48))
        self.assertEqual(r.step, Fraction(2, 3))

    def test_modern_boundaries(self):
        self.assertEqual(solid_chain((2, 3, 4), (2, 3, 4)).anob, (24,)*4)
        self.assertEqual(solid_chain((1, 2, 3), (2, 4, 6)).anob, (6, 12, 24, 48))

    def test_alternative_factorization_and_bad_input(self):
        with self.assertRaises(ValueError):
            solid_chain((2, 4, 6), (2, 9, 9))
        self.assertEqual(prod((2, 9, 9)), 162)
        self.assertEqual([Fraction(y,x) for x,y in ((48,72),(72,108),(108,162))],
                         [Fraction(3,2)]*3)
        for left in ((1,2), (0,2,3), (-1,2,3), (True,2,3), (1.0,2,3)):
            with self.subTest(left=left), self.assertRaises(ValueError):
                solid_chain(left, (2,4,6))

    def test_exact_grid(self):
        similar = other = 0
        for factors in itertools.product(range(1,7), repeat=6):
            left, right = factors[:3], factors[3:]
            ratios = {Fraction(y,x) for x,y in zip(left,right)}
            if len(ratios) != 1:
                with self.assertRaises(ValueError):
                    solid_chain(left,right)
                other += 1
                continue
            r = solid_chain(left,right)
            step = ratios.pop()
            self.assertEqual(r.step, step)
            self.assertEqual(r.kml, tuple(Fraction(prod(left[:2]))*step**i for i in range(3)))
            self.assertEqual(r.anob, tuple(Fraction(prod(left))*step**i for i in range(4)))
            self.assertEqual(r.anob[-1], prod(right))
            self.assertEqual(Fraction(prod(right),prod(left)), step**3)
            similar += 1
        self.assertEqual(similar+other, 6**6)
        print(f"Exact grid: {similar+other} ordered sextuples; {similar} similar, {other} nonsimilar")
