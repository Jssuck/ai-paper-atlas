from itertools import product
from math import isqrt
import unittest

from square_endpoints import square_endpoint_roots


class TestSquareEndpoints(unittest.TestCase):
    def test_middle_need_not_be_square(self):
        self.assertEqual(square_endpoint_roots(4, 6, 9), (2, 3))
        self.assertEqual(square_endpoint_roots(9, 6, 4), (3, 2))

    def test_missing_premise(self):
        for args in ((8,12,18),(18,12,8),(4,5,9),(4,6,16)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                square_endpoint_roots(*args)

    def test_modern_boundaries(self):
        self.assertEqual(square_endpoint_roots(1, 3, 9), (1, 3))
        self.assertEqual(square_endpoint_roots(16, 16, 16), (4, 4))

    def test_invalid(self):
        for args in ((0,0,0),(-1,2,4),(True,1,1),(4.0,6,9)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                square_endpoint_roots(*args)

    def test_bounded_oracle(self):
        bound = 100
        squares = {n*n:n for n in range(1,isqrt(bound)+1)}
        valid = nonsquare_first = nongp = 0
        for a,c in product(range(1,bound+1),repeat=2):
            b = isqrt(a*c)
            if b*b != a*c:
                nongp += 1
            elif a not in squares:
                nonsquare_first += 1
            else:
                self.assertIn(c,squares)
                expected = (squares[a],squares[c])
                self.assertEqual(square_endpoint_roots(a,b,c),expected)
                self.assertEqual(expected[0]*expected[1],b)
                valid += 1
                continue
            with self.assertRaises(ValueError):
                square_endpoint_roots(a,b,c)
        self.assertEqual(valid+nonsquare_first+nongp,10000)
        print(f"Endpoint grid: {valid} accepted, {nonsquare_first} nonsquare starts with integer means, {nongp} non-integer means")
