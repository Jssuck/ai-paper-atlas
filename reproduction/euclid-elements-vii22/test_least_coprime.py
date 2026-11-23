from fractions import Fraction
from itertools import product
import unittest

from least_coprime import Witness, diagnostic, shrink


class TestLeast(unittest.TestCase):
    def test_any_measure(self):
        self.assertEqual(shrink(18,30,2), Witness(2,(9,15)))
        self.assertEqual(shrink(18,30,6), Witness(6,(3,5)))

    def test_coprime_composites(self):
        self.assertEqual(diagnostic(8,15),((8,15),True))
        with self.assertRaises(ValueError):
            shrink(8,15,2)

    def test_grid(self):
        pairs = supported = units = 0
        for a,b in product(range(2,19),repeat=2):
            ratio = Fraction(a,b)
            brute = next((x,y) for x in range(1,a+1) for y in range(1,b+1)
                         if Fraction(x,y) == ratio)
            divisors = [c for c in range(2,min(a,b)+1) if a%c == b%c == 0]
            self.assertEqual(diagnostic(a,b),(brute,not divisors))
            for c in divisors:
                if c in (a,b):
                    with self.assertRaisesRegex(ValueError,"unit quotient"):
                        shrink(a,b,c)
                    units += 1
                else:
                    d,e = shrink(a,b,c).smaller
                    self.assertLess(d,a)
                    self.assertLess(e,b)
                    self.assertEqual((c*d,c*e),(a,b))
                    self.assertEqual(Fraction(d,e),ratio)
                    supported += 1
            pairs += 1
        self.assertEqual(pairs,289)
        print(f"Exact grid: {pairs} pairs, {supported} nonunit certificates, {units} unit boundaries")

    def test_invalid(self):
        for args in ((18,30,4),(18,30,1),(18,30,0),(18,30,2.0),(False,30,2)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                shrink(*args)

    def test_unit_boundary(self):
        self.assertEqual(diagnostic(3,6),((1,2),False))
        self.assertEqual(Fraction(3,6),Fraction(1,2))
        with self.assertRaisesRegex(ValueError,"unit quotient"):
            shrink(3,6,3)
        with self.assertRaises(ValueError):
            diagnostic(1,2)
