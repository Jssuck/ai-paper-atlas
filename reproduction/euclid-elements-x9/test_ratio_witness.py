from fractions import Fraction as F
from unittest import TestCase

from ratio_witness import Certificate, classify


class TestX9(TestCase):
    def test_examples(self):
        self.assertEqual(classify(2, 1), Certificate(F(2), None, None))
        self.assertEqual(classify(50, 72), Certificate(F(25,36), F(5,6), F(2)))
        self.assertEqual(classify(72, 50), Certificate(F(36,25), F(6,5), F(2)))
        self.assertEqual(classify(4, 9), Certificate(F(4,9), F(2,3), F(1)))
        self.assertEqual(classify(2, 2), Certificate(F(1), F(1), F(2)))

    def test_scaling(self):
        self.assertEqual(classify(F(4,7), F(9,7)), Certificate(F(4,9), F(2,3), F(1,7)))
        self.assertIsNone(classify(F(2,7), F(1,7)).length_ratio)

    def test_grid(self):
        # Construct all squared candidate ratios independently of the isqrt path.
        bound = 80
        max_side = 9  # 9² exceeds bound, hence includes every possible reduced side count.
        roots = {F(m*m, n*n): F(m, n)
                 for m in range(1,max_side+1) for n in range(1,max_side+1)}
        count = 0
        for a in range(1,bound+1):
            for b in range(1,bound+1):
                c = classify(a,b)
                expected = roots.get(F(a,b))
                self.assertEqual(c.length_ratio, expected, (a,b))
                if expected is None:
                    self.assertIsNone(c.common_side_squared)
                else:
                    count += 1
                    self.assertEqual(c.common_side_squared * expected.numerator**2, a)
                    self.assertEqual(c.common_side_squared * expected.denominator**2, b)
        self.assertEqual(count, 224)
        print(f"Grid: {bound**2} ordered pairs; length commensurable={count}, square-only={bound**2-count}")

    def test_invalid_and_large(self):
        for pair in [(0,1), (1,-1), (1,0.5), (True,1)]:
            with self.assertRaises(ValueError):
                classify(*pair)
        n=10**72+1
        self.assertEqual(classify(2*n*n,2*(n-1)**2).length_ratio, F(n,n-1))
        self.assertIsNone(classify(n*n+1,1).length_ratio)
