from fractions import Fraction
from math import gcd
import unittest

from alternate_remainders import Trace, subtract


class TestSubtract(unittest.TestCase):
    def test_vii7(self):
        self.assertEqual(subtract(12,36,4,12), Trace((1,3),(1,3),(8,24),(1,3),"VII.7"))

    def test_vii8(self):
        self.assertEqual(subtract(12,18,4,6).subtraction, "VII.8")
        self.assertEqual(subtract(12,18,8,12).subtraction, "VII.8")
        self.assertEqual(subtract(18,30,6,10), Trace((3,5),(1,3),(12,20),(3,5),"VII.8"))

    def test_grid(self):
        counts = {"VII.7": 0, "VII.8": 0}
        for n in range(2,11):
            for m in range(1,n):
                if gcd(m,n) != 1:
                    continue
                for u in range(3,11):
                    for v in range(2,u):
                        a,b,c,d = m*u,n*u,m*v,n*v
                        got = subtract(a,b,c,d)
                        ab = Fraction(a,b)
                        self.assertEqual(ab, Fraction(c,d))
                        self.assertEqual(ab, Fraction(a-c,b-d))
                        self.assertEqual(Fraction(*got.counts), ab)
                        self.assertEqual(got.remainder_counts, got.counts)
                        self.assertEqual(Fraction(*got.removal), Fraction(c,a))
                        self.assertEqual(got.subtraction, "VII.7" if b%a == 0 else "VII.8")
                        counts[got.subtraction] += 1
        self.assertEqual(counts, {"VII.7": 324, "VII.8": 792})
        print("Exact grid:", counts)

    def test_invalid(self):
        for args in ((12,18,4,8), (12,12,4,4), (18,12,6,4),
                     (12,18,0,0), (12,18,12,18), (12,18,14,21),
                     (False,18,4,6), (3,6,1,2)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                subtract(*args)
        self.assertNotEqual(Fraction(12,18), Fraction(8,10))

    def test_units(self):
        self.assertEqual(subtract(3,6,2,4).remainders, (1,2))
        self.assertEqual(subtract(6,9,2,3).removal, (1,3))
        self.assertEqual(subtract(6,9,2,3).counts, (2,3))


if __name__ == "__main__":
    unittest.main()
