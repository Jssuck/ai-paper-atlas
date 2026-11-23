from fractions import Fraction
from itertools import product
from math import gcd
import unittest

from paired_sum import Trace, pool


class TestPool(unittest.TestCase):
    def test_one_part(self):
        self.assertEqual(pool(((4,12),(5,15),(7,21))),
                         Trace((1,3), "VII.5", ((4,12),(9,27),(16,48)), (16,48)))

    def test_parts(self):
        self.assertEqual(pool(((2,3),(6,9),(8,12))),
                         Trace((2,3), "VII.6", ((2,3),(8,12),(16,24)), (16,24)))

    def test_exact_grid(self):
        counts = {"VII.5": 0, "VII.6": 0}
        for n in range(2,9):
            for m in range(1,n):
                if gcd(m,n) != 1:
                    continue
                for k in (2,3):
                    for weights in product(range(2,6), repeat=k):
                        pairs = [(m*w,n*w) for w in weights]
                        trace = pool(pairs)
                        expected = Fraction(*pairs[0])
                        self.assertEqual(trace.ratio_counts, (expected.numerator, expected.denominator))
                        self.assertEqual(trace.branch, "VII.5" if pairs[0][1] % pairs[0][0] == 0 else "VII.6")
                        self.assertTrue(all(Fraction(a,b) == expected for a,b in pairs))
                        for i, (a,b) in enumerate(trace.prefixes, 1):
                            self.assertEqual((a,b), tuple(map(sum, zip(*pairs[:i]))))
                            self.assertEqual(Fraction(a,b), expected)
                        self.assertEqual(trace.total, tuple(map(sum, zip(*pairs))))
                        counts[trace.branch] += 1
        self.assertEqual(counts, {"VII.5": 560, "VII.6": 1120})
        print("Exact grid:", counts)

    def test_pairing(self):
        pairs = ((4,6),(8,12))
        self.assertEqual(pool(pairs).total, pool(reversed(pairs)).total)
        crossed = ((4,12),(8,6))
        crossed_both_proper = ((4,12),(6,8))
        for specimen in (crossed, crossed_both_proper, ((4,6),(8,13))):
            with self.subTest(specimen=specimen), self.assertRaises(ValueError):
                pool(specimen)
        self.assertEqual(tuple(map(sum, zip(*crossed))), pool(pairs).total)
        self.assertEqual(tuple(map(sum, zip(*crossed_both_proper))), pool(((4,8),(6,12))).total)

    def test_scope(self):
        for specimen in (((2,3),), (), ((2,2),(3,3)), ((3,2),(6,4)),
                         ((1,2),(2,4)), ((0,2),(3,6)), ((2,3),(4,6.0))):
            with self.subTest(specimen=specimen), self.assertRaises(ValueError):
                pool(specimen)
        self.assertEqual(Fraction(3+6,2+4), Fraction(3,2))
        self.assertEqual(Fraction(2+3,2+3), Fraction(2,2))


if __name__ == "__main__":
    unittest.main()
