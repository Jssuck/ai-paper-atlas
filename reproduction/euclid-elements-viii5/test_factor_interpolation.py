from fractions import Fraction
from itertools import product
import unittest

from factor_interpolation import Trace, interpolate


def search(a,b,c,d):
    for first in range(1,a*b+1):
        terms = (Fraction(first),first*Fraction(c,a),first*Fraction(c,a)*Fraction(d,b))
        if all(t.denominator == 1 for t in terms):
            return tuple(t.numerator for t in terms)
    raise ArithmeticError("raw product would be a witness")


class TestInterpolate(unittest.TestCase):
    def test_example(self):
        self.assertEqual(interpolate(6,10,9,14),Trace((60,90,126),(10,15,21),6,-1))

    def test_swapped_matching(self):
        self.assertEqual(interpolate(6,10,14,9).raw,(60,140,126))
        # Simultaneously swap both factor positions: reverse the order of the
        # same two replacement ratios. Endpoints stay fixed; middle changes.
        self.assertEqual(interpolate(10,6,14,9).primitive,(10,14,21))
        self.assertEqual(Fraction(10,21),Fraction(60,126))
        self.assertNotEqual(interpolate(6,10,14,9).primitive,(10,15,21))

    def test_grid(self):
        counts = {-1:0,0:0,1:0}
        for a,b,c,d in product(range(2,8),repeat=4):
            t = interpolate(a,b,c,d)
            x,y,z = t.raw
            self.assertEqual((Fraction(x,y),Fraction(y,z)),(Fraction(a,c),Fraction(b,d)))
            self.assertEqual(t.primitive,search(a,b,c,d))
            self.assertEqual(t.endpoint_order,(Fraction(a,c)*Fraction(b,d)>1)
                                               -(Fraction(a,c)*Fraction(b,d)<1))
            counts[t.endpoint_order] += 1
        self.assertEqual(sum(counts.values()),1296)
        print("Exact grid: 1296 factor quadruples, endpoint orders:",counts)

    def test_equal_and_reverse(self):
        self.assertEqual(interpolate(2,6,3,4).primitive,(2,3,2))
        self.assertEqual(interpolate(2,6,3,4).endpoint_order,0)
        self.assertEqual(interpolate(9,14,6,10).endpoint_order,1)

    def test_scope(self):
        self.assertEqual(interpolate(1,3,2,4,modern=True).primitive,(3,6,8))
        for values in ((1,3,2,4),(0,3,2,4),(-1,3,2,4),(True,3,2,4),(1.0,3,2,4)):
            with self.subTest(values=values),self.assertRaises(ValueError):
                interpolate(*values)
