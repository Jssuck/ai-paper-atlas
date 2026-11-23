from fractions import Fraction
from itertools import product
import unittest

from least_ratio import Trace, candidate, least


def brute(a,b,minimum=1):
    expected = Fraction(a,b)
    for x in range(minimum,a+1):
        for y in range(minimum,b+1):
            if Fraction(x,y)==expected:
                return x,y
    raise ValueError("no candidate in bounded search")


class TestLeast(unittest.TestCase):
    def test_false_least(self):
        self.assertEqual(candidate(16,24,10,15),
            Trace((2,3),(5,8),((2,3),(4,6),(6,9),(8,12),(10,15)),False,(5,8),(2,3)))
        self.assertEqual(Fraction(10,16),Fraction(15,24))

    def test_least_count(self):
        self.assertEqual(candidate(16,24,8,12),
                         Trace((2,3),(4,8),((2,3),(4,6),(6,9),(8,12)),False,(1,2),None))
        shared_scale = candidate(20,30,12,18)
        self.assertEqual((shared_scale.fraction_counts,shared_scale.historical_block),((3,5),(4,6)))
        self.assertEqual(candidate(16,24,2,3),Trace((2,3),(1,8),((2,3),),True,(1,8),None))
        self.assertEqual(least(91,143),((7,11),13))
        self.assertEqual(least(7,11),((7,11),1))

    def test_grid(self):
        count = 0
        for a,b in product(range(1,21),repeat=2):
            pair,k = least(a,b)
            self.assertEqual(pair,brute(a,b))
            self.assertEqual(tuple(x*k for x in pair),(a,b))
            self.assertEqual(Fraction(*pair),Fraction(a,b))
            count += 1
        self.assertEqual(count,400)
        print("Exact grid:",count)

    def test_unit_diagnostic(self):
        self.assertEqual(brute(3,6),(1,2))
        self.assertEqual(brute(3,6,2),(2,4))
        self.assertNotEqual((3%2,6%4),(0,0))
        with self.assertRaises(ValueError):
            candidate(3,6,2,4)

    def test_scope(self):
        for args in ((16,24,10,14),(16,24,16,24),(24,16,15,10),(16,24,1,2)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                candidate(*args)
        for args in ((0,2),(2,-1),(2,3.0),(True,2)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                least(*args)


if __name__ == "__main__":
    unittest.main()
