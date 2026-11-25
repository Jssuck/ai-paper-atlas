from itertools import product
from math import prod
import unittest
from solid_product import SolidTrace, solid_product


class TestSolidProduct(unittest.TestCase):
    def test_fixtures(self):
        self.assertEqual(solid_product(4,3),SolidTrace((2,2,3),12,False))
        self.assertEqual(solid_product(4,2),SolidTrace((2,2,2),8,True))
        self.assertEqual(solid_product(25,7),SolidTrace((5,5,7),175,False))

    def test_sufficient_not_necessary(self):
        with self.assertRaises(ValueError):
            solid_product(3,4)
        self.assertEqual(prod((3,2,2)),3*4)

    def test_two_primes_cannot_produce_three_nonunit_factors(self):
        with self.assertRaises(ValueError):
            solid_product(2,3)
        self.assertLess(2*3,2**3)

    def test_invalid(self):
        for args in ((4,1),(1,4),(0,4),(-1,4),(True,4),(4,2.0)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                solid_product(*args)

    def test_exhaustive_oracle(self):
        from collections import defaultdict
        side = range(2,33)
        triples = defaultdict(set)
        for i in range(2,257):
            for j in range(2,1024//(2*i)+1):
                for k in range(2,1024//(i*j)+1):
                    triples[i*j*k].add((i,j,k))
        accepted = solid_other = nonsolid = 0
        for a,b in product(side, repeat=2):
            c = a*b
            possible = triples[c]
            tagged = {t for t in possible if t[2] == b}
            if not tagged:
                with self.assertRaises(ValueError):
                    solid_product(a,b)
                if possible:
                    solid_other += 1
                else:
                    nonsolid += 1
                continue
            out = solid_product(a,b)
            self.assertIn(out.factors,tagged)
            self.assertEqual(out.product,c)
            self.assertEqual(out.cube,any(i*i*i==c for i in side))
            accepted += 1
        self.assertEqual(accepted+solid_other+nonsolid,31**2)
        print(f'Grid: {accepted} certified; {solid_other} solid outside hypothesis; {nonsolid} nonsolid')
