from fractions import Fraction
from math import gcd
import unittest

from alternate_ratio import Alternation, alternate


class TestAlternate(unittest.TestCase):
    def test_fixtures(self):
        for args, expected in (
            ((4,8,12,24), Alternation((1,2),(1,3),"VII.9","part")),
            ((6,12,10,20), Alternation((1,2),(3,5),"VII.9","parts")),
            ((4,6,12,18), Alternation((2,3),(1,3),"VII.10","part")),
            ((8,12,20,30), Alternation((2,3),(2,5),"VII.10","parts")),
        ):
            self.assertEqual(alternate(*args), expected)

    def test_grid(self):
        tally = {}
        for n in range(2,9):
            for m in range(1,n):
                if gcd(m,n) != 1:
                    continue
                for v in range(3,9):
                    for u in range(2,v):
                        a,b,c,d = m*u,n*u,m*v,n*v
                        result = alternate(a,b,c,d)
                        self.assertEqual(Fraction(a,b), Fraction(c,d))
                        self.assertEqual(Fraction(a,c), Fraction(b,d))
                        self.assertEqual(Fraction(*result.incoming), Fraction(a,b))
                        self.assertEqual(Fraction(*result.crossed), Fraction(a,c))
                        self.assertEqual(result.route, "VII.9" if b%a == 0 else "VII.10")
                        self.assertEqual(result.crossed_kind, "part" if c%a == 0 else "parts")
                        key = result.route, result.crossed_kind
                        tally[key] = tally.get(key,0)+1
        self.assertEqual(sum(tally.values()),441)
        self.assertEqual(len(tally),4)
        print("Exact grid:", sorted(tally.items()))

    def test_mismatch_and_scope(self):
        for xs in ((8,12,20,32),(8,12,8,12),(16,24,8,12),
                   (12,8,24,16),(1,3,4,12),(0,2,3,6),(True,3,4,12)):
            with self.subTest(xs=xs), self.assertRaises(ValueError):
                alternate(*xs)
        self.assertNotEqual(Fraction(8,20), Fraction(12,32))

    def test_modern_direction_changes(self):
        a,b,c,d = (8,12,16,24)
        proper = Fraction(*alternate(a,b,c,d).crossed)
        self.assertEqual(Fraction(c,a), 1/proper)
        self.assertEqual(Fraction(d,b), 1/proper)
        self.assertEqual(Fraction(b,d), proper)  # reversing both input ratios
        self.assertEqual(Fraction(a,c), proper)

    def test_modern_equalities(self):
        self.assertEqual(Fraction(8,8), Fraction(12,12))  # equal crossed terms
        self.assertEqual(Fraction(8,16), Fraction(8,16))  # equal within input pairs
        with self.assertRaises(ValueError):
            alternate(8,8,16,16)
        self.assertEqual(alternate(2,3,4,6).incoming, (2,3))  # unit gcd


if __name__ == "__main__":
    unittest.main()
