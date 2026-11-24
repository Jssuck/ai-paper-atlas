import unittest
from itertools import product
from common_multiple_remainder import Trace, close_difference, verify_least_divides


class TestRemainder(unittest.TestCase):
    def test_exact(self):
        self.assertEqual(verify_least_divides(12,18,108),Trace(3,0,(0,0)))
        self.assertEqual(verify_least_divides(12,18,36),Trace(1,0,(0,0)))

    def test_nonleast(self):
        self.assertEqual(close_difference(12,18,72,108),Trace(1,36,(3,2)))
        self.assertEqual(close_difference(12,18,72,36),Trace(0,36,(3,2)))

    def test_invalid(self):
        for args in ((12,18,36,50),(12,18,18,108),(12,18,36,0),(True,18,36,108)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                close_difference(*args)
        with self.assertRaises(ValueError):
            verify_least_divides(12,18,50)

    def test_grid(self):
        exact = positive = 0
        for a,b in product(range(2,16),repeat=2):
            common = [c for c in range(1,2*a*b+1) if c%a == c%b == 0]
            least = common[0]
            for target in common:
                t = verify_least_divides(a,b,target)
                self.assertEqual(t,Trace(target//least,0,(0,0)))
                exact += 1
                for step in common:
                    q,r = divmod(target,step)
                    self.assertEqual(close_difference(a,b,step,target),Trace(q,r,(r//a,r//b)))
                    if r:
                        self.assertIn(r,common)
                        positive += 1
        print(f"Exact grid: 196 pairs, {exact} least-step checks, {positive} positive nonleast-step remainders")

    def test_modern_unit(self):
        self.assertEqual(verify_least_divides(1,6,12),Trace(2,0,(0,0)))
        self.assertEqual(verify_least_divides(5,5,15),Trace(3,0,(0,0)))
