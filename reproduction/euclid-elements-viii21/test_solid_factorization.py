import unittest
from fractions import Fraction
from itertools import product
from math import prod

from solid_factorization import SolidTrace, factor_solids


class TestSolids(unittest.TestCase):
    def test_original_witness(self):
        self.assertEqual(factor_solids(48,72,108,162),
                         SolidTrace((4,6,9),(12,18),(2,2,12),(3,3,18)))

    def test_reversed_and_primitive(self):
        self.assertEqual(factor_solids(162,108,72,48),
                         SolidTrace((9,6,4),(18,12),(3,3,18),(2,2,12)))
        self.assertEqual(factor_solids(24,36,54,81).no,(6,9))

    def test_modern_boundaries(self):
        self.assertEqual(factor_solids(1,2,4,8).right,(2,2,2))
        self.assertEqual(factor_solids(9,9,9,9).left,(1,1,9))

    def test_invalid(self):
        for args in ((48,72,108,161),(48,73,108,162),
                     (0,0,0,0),(-1,2,4,8),(True,2,4,8),(1.0,2,4,8)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                factor_solids(*args)

    def test_exact_cubed_ratio_grid(self):
        bound = 100
        roots = {Fraction(i**3,j**3):Fraction(i,j)
                 for i,j in product(range(1,5),repeat=2)}
        accepted = absent = 0
        for a,b in product(range(1,bound+1),repeat=2):
            ratio = Fraction(b,a)
            # The reduced numerator and denominator cannot exceed bound,
            # so any corresponding positive cube roots are at most 4.
            step = roots.get(ratio)
            if step is None:
                with self.assertRaises(ValueError):
                    factor_solids(a,a,b,b)
                absent += 1
                continue
            chain = [a*step**i for i in range(4)]
            self.assertTrue(all(x.denominator==1 for x in chain))
            original = [int(x) for x in chain]
            r = factor_solids(*original)
            self.assertEqual((prod(r.left),prod(r.right)),(a,b))
            self.assertEqual([Fraction(y,x) for x,y in zip(r.left,r.right)], [step]*3)
            self.assertEqual(r.efg, (step.denominator**2,
                                     step.numerator*step.denominator,step.numerator**2))
            self.assertEqual(Fraction(r.no[1],r.no[0]),step)
            accepted += 1
        self.assertEqual(accepted+absent,10000)
        print(f"Endpoint cube-ratio grid: {accepted+absent} ordered pairs, {accepted} with two means, {absent} without")
