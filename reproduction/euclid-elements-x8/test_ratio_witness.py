from fractions import Fraction as F
from unittest import TestCase

from ratio_witness import classify


class TestClassification(TestCase):
    def test_examples(self):
        self.assertIsNone(classify(F(3, 2)).ratio)
        self.assertEqual(classify(F(50, 72), 6), classify(F(25, 36), 6))
        self.assertEqual(classify(F(25, 36), 6).a, 5)
        self.assertEqual(classify(F(4, 9), 3).ratio, F(2, 3))
        self.assertEqual(classify(1, F(11, 7)).a, F(11, 7))

    def test_nonsquare_bounds(self):
        for p, d in [(2, 9), (4, 7), (3, 2)]:
            cert = classify(F(p, d))
            for t, r in zip((p, d), cert.floors):
                self.assertLessEqual(r*r, t)
                self.assertLess(t, (r+1)**2)
            self.assertTrue(any(r*r < t for t, r in zip((p, d), cert.floors)))
            self.assertIsNone(cert.a)

    def test_grid(self):
        # Independent generation of squared candidate ratios; no isqrt.
        # Reduced root of a reduced p/d in this range must have terms <= 64.
        bound = 64
        roots = {F(m*m, n*n): F(m, n)
                 for m in range(1, bound+1) for n in range(1, bound+1)}
        yes = 0
        for p in range(1, bound+1):
            for d in range(1, bound+1):
                q = F(p, d)
                result = classify(q, F(5, 7))
                expected = roots.get(q)
                self.assertEqual(result.ratio, expected, (p, d))
                if expected is not None:
                    yes += 1
                    self.assertEqual(result.a, F(5, 7)*expected)
                else:
                    self.assertIsNone(result.a)
        self.assertEqual(yes, 180)
        print(f"Grid: {bound**2} ordered pairs; rational={yes}, irrational={bound**2-yes}")

    def test_invalid_and_large(self):
        for args in [(0,),(-1,),(1.5,),(True,),(2,0),(2,1.0)]:
            with self.assertRaises(ValueError):
                classify(*args)
        n = 10**60+3
        self.assertEqual(classify(F(n*n, (n+1)**2)).ratio, F(n,n+1))
        self.assertIsNone(classify(n*n+1).ratio)
