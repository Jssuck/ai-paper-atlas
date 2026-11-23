from fractions import Fraction
from math import gcd
import unittest

from alternate_same_parts import Proof, compare


class TestCompare(unittest.TestCase):
    def test_unit_branch(self):
        self.assertEqual(compare(8,12,16,24), Proof(2,3,4,8,(1,2),"VII.5"))

    def test_parts_branch(self):
        self.assertEqual(compare(8,12,20,30), Proof(2,3,4,10,(2,5),"VII.6"))

    def test_exact_grid(self):
        counts = {"VII.5": 0, "VII.6": 0}
        for n in range(3,11):
            for m in range(2,n):
                if gcd(m,n) != 1:
                    continue
                for h in range(2,11):
                    for g in range(1,h):
                        ab,c,de,f = m*g,n*g,m*h,n*h
                        traced = compare(ab,c,de,f)
                        baseline = Fraction(ab,de)
                        self.assertEqual(Fraction(ab,c), Fraction(de,f))
                        self.assertEqual(Fraction(c,f), baseline)
                        self.assertEqual(traced.comparison, (baseline.numerator, baseline.denominator))
                        self.assertEqual((traced.m,traced.n,traced.g,traced.h), (m,n,g,h))
                        self.assertEqual(traced.aggregation, "VII.5" if h%g == 0 else "VII.6")
                        counts[traced.aggregation] += 1
        self.assertEqual(counts, {"VII.5": 374, "VII.6": 616})
        print("Exact grid:", counts)

    def test_invalid_premises(self):
        for args in ((8,12,20,32), (4,12,8,24), (8,8,16,16), (False,12,20,30)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                compare(*args)
        self.assertNotEqual(Fraction(8,20), Fraction(12,32))

    def test_scope(self):
        self.assertEqual(compare(2,3,4,6).g, 1)
        for args in ((8,12,8,12), (20,30,8,12), (1,3,2,6)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                compare(*args)
        self.assertEqual(Fraction(20,8), Fraction(30,12))
        self.assertEqual(Fraction(8,8), Fraction(12,12))


if __name__ == "__main__":
    unittest.main()
