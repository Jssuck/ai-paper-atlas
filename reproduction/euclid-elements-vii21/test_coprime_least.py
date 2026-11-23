from fractions import Fraction
from itertools import product
import unittest

from coprime_least import Diagnostic, analyze, divisor_count


class TestLeast(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(analyze(8,15),Diagnostic((8,15),1,True))
        self.assertEqual(analyze(16,30),Diagnostic((8,15),2,False))
        self.assertEqual(divisor_count(16,30,8,15),2)

    def test_grid(self):
        count = 0
        for a,b in product(range(2,21),repeat=2):
            target = Fraction(a,b)
            least = next((x,y) for x in range(1,a+1) for y in range(1,b+1)
                         if Fraction(x,y) == target)
            commons = [k for k in range(1,min(a,b)+1) if a%k == b%k == 0]
            self.assertEqual(analyze(a,b),Diagnostic(least,max(commons),len(commons)==1))
            count += 1
        self.assertEqual(count,361)
        print("Exact grid:",count)

    def test_nonleast_candidate(self):
        self.assertEqual(divisor_count(12,18,6,9),2)
        self.assertEqual(analyze(12,18),Diagnostic((2,3),6,False))
        self.assertEqual(Fraction(6,9),Fraction(2,3))
        self.assertNotEqual(analyze(12,18).least,(6,9))

    def test_invalid_witness(self):
        for args in ((16,30,8,10),(16,30,8,14),(8,15,8,15)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                divisor_count(*args)

    def test_modern_unit_boundary(self):
        self.assertEqual(analyze(4,8),Diagnostic((1,2),4,False))
        for args in ((4,8,1,2),(0,8,1,2),(4,8,1.0,2)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                divisor_count(*args)
        with self.assertRaises(ValueError):
            analyze(True,2)
