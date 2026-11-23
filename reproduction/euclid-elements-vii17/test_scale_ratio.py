from itertools import product
from fractions import Fraction
import unittest

from scale_ratio import Trace, compare_products, scale


class TestScale(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(scale(3,4,6),Trace((12,18),(3,3),(1,3),(2,3)))

    def test_grid(self):
        count = 0
        for a,b,c in product(range(2,11),repeat=3):
            t = scale(a,b,c)
            d,e = t.products
            self.assertEqual((d,e),(a*b,a*c))
            self.assertEqual((Fraction(d,b),Fraction(e,c)),(a,a))
            self.assertEqual(Fraction(*t.internal_ratio),Fraction(1,a))
            self.assertEqual(Fraction(*t.crossed_ratio),Fraction(b,c))
            self.assertEqual(Fraction(b,c),Fraction(d,e))
            count += 1
        self.assertEqual(count,729)
        print("Exact grid:",count)

    def test_wrong_products(self):
        for args in ((3,4,6,12,24),(3,4,6,16,24),(3,4,6,12,19)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                compare_products(*args)
        self.assertNotEqual(Fraction(4,6),Fraction(12,24))
        self.assertEqual(Fraction(4,6),Fraction(16,24))  # not the specified A

    def test_equal_and_reverse(self):
        self.assertEqual(scale(3,4,4).crossed_ratio,(1,1))
        self.assertEqual(scale(3,6,4).crossed_ratio,(3,2))

    def test_modern_boundary(self):
        for args in ((1,4,6),(3,1,6),(0,4,6),(3,0,6),(3,4,0),(True,4,6),(3.0,4,6)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                scale(*args)
        self.assertEqual(Fraction(4,6),Fraction(1*4,1*6))
        self.assertEqual(Fraction(1,6),Fraction(3,18))
        with self.assertRaises(ZeroDivisionError):
            Fraction(0*4,0*6)


if __name__ == "__main__":
    unittest.main()
