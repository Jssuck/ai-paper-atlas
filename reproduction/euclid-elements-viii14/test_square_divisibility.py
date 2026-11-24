from fractions import Fraction
from itertools import product
import unittest

from square_divisibility import Trace, from_squares, inspect


class TestSquares(unittest.TestCase):
    def test_positive_and_reverse(self):
        self.assertEqual(inspect(4,12),Trace((16,48,144),(3,1),3,3,9))
        self.assertEqual(from_squares(4,12),3)
        self.assertIsNone(from_squares(12,4))

    def test_grid(self):
        yes=no=0
        for c,d in product(range(1,41),repeat=2):
            t = inspect(c,d,modern=True)
            a,e,b = t.bridge
            self.assertEqual(Fraction(e,a),Fraction(b,e))
            self.assertEqual(Fraction(b,a).denominator,Fraction(d,c).denominator**2)
            self.assertEqual(t.side_count,d//c if d%c == 0 else None)
            self.assertEqual(t.bridge_count,b//e if b%e == 0 else None)
            self.assertEqual(t.square_count,b//a if b%a == 0 else None)
            self.assertEqual(from_squares(c,d,modern=True),t.side_count)
            yes += t.side_count is not None
            no += t.side_count is None
        self.assertEqual(yes+no,1600)
        print(f"Exact grid: {yes+no} side pairs, {yes} measure, {no} do not")

    def test_noninteger(self):
        for c,d,p,q in ((6,9,3,2),(4,10,5,2),(2,3,3,2)):
            with self.subTest(c=c,d=d):
                t=inspect(c,d)
                self.assertEqual(t.reduced_growth,(p,q))
                self.assertEqual((t.side_count,t.bridge_count,t.square_count),(None,None,None))
                self.assertIsNone(from_squares(c,d))

    def test_scope(self):
        self.assertEqual(from_squares(1,3,modern=True),3)
        self.assertEqual(from_squares(7,7,modern=True),1)
        for sides in ((0,2),(-2,3),(True,4),(2.0,4),(1,3),(7,7)):
            with self.subTest(sides=sides),self.assertRaises(ValueError):
                inspect(*sides)

    def test_big(self):
        c=10**60+1
        self.assertEqual(from_squares(c,11*c),11)
        self.assertIsNone(from_squares(c,11*c+1))
