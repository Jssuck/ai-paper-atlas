import unittest
from fractions import Fraction
from itertools import product

from transfer_square import SquareTrace, transfer_square


class TestTransferSquare(unittest.TestCase):
    def test_fractional_naive_scale_and_reverse(self):
        self.assertEqual(Fraction(4,16), Fraction(1,4))
        self.assertEqual(Fraction(1,4)*24,6)
        self.assertEqual(transfer_square(4,9,16,36), SquareTrace((4,6,9),1,6,(2,3)))
        self.assertEqual(transfer_square(9,4,36,16), SquareTrace((9,6,4),1,6,(3,2)))

    def test_wrong_ratio_and_missing_square(self):
        for terms in ((4,9,36,16),(8,18,16,36),(4,6,8,12),(4,9,8,18)):
            with self.subTest(terms=terms), self.assertRaises(ValueError):
                transfer_square(*terms)

    def test_modern_boundaries_and_invalid_inputs(self):
        self.assertEqual(transfer_square(1,4,9,36).roots,(1,2))
        self.assertEqual(transfer_square(9,9,4,4),SquareTrace((1,1,1),9,9,(3,3)))
        for terms in ((0,0,4,9),(-4,-9,4,9),(True,4,9,36),(4.0,9,16,36)):
            with self.subTest(terms=terms), self.assertRaises(ValueError):
                transfer_square(*terms)

    def test_large_exact(self):
        s,t = 10**40+1,10**40+3
        result = transfer_square(s*s,t*t,4*s*s,4*t*t)
        self.assertEqual(result.roots,(s,t))
        self.assertEqual(result.middle,s*t)

    def test_bounded_grid(self):
        square_root = {i*i:i for i in range(1,11)}
        accepted = wrong = nonsquare = 0
        for u,v in product(range(1,9),repeat=2):
            # Independent oracle: express B from the fraction rather than
            # using the implementation's cross-multiplication or bridge.
            ratio = Fraction(v*v,u*u)
            for a,b in product(range(1,101),repeat=2):
                if a*ratio != b:
                    wrong += 1
                elif a not in square_root:
                    nonsquare += 1
                else:
                    self.assertIn(b,square_root)
                    result = transfer_square(a,b,u*u,v*v)
                    self.assertEqual(result.roots,(square_root[a],square_root[b]))
                    self.assertEqual(result.middle,square_root[a]*square_root[b])
                    accepted += 1
                    continue
                with self.assertRaises(ValueError):
                    transfer_square(a,b,u*u,v*v)
        self.assertEqual(accepted+wrong+nonsquare,640000)
        print(f"Grid: {accepted} accepted, {nonsquare} ratio matches without square A, {wrong} ratio mismatches")
