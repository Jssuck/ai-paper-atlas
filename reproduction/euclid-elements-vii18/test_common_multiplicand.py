from fractions import Fraction
from itertools import product
import unittest

from common_multiplicand import Trace, check_products, transport


class TestTransport(unittest.TestCase):
    def test_example(self):
        self.assertEqual(transport(4,6,3), Trace((12,18),(12,18),(3,3),(1,3),(2,3)))

    def test_grid(self):
        count = 0
        for a,b,c in product(range(2,11),repeat=3):
            t = transport(a,b,c)
            d,e = t.products
            self.assertEqual((d,e),(a*c,b*c))
            self.assertEqual(t.swapped,(c*a,c*b))
            self.assertEqual((Fraction(d,a),Fraction(e,b)),t.measure_counts)
            self.assertEqual(Fraction(a,d),Fraction(b,e))
            self.assertEqual(Fraction(a,d),Fraction(*t.internal))
            self.assertEqual(Fraction(a,b),Fraction(d,e))
            self.assertEqual(Fraction(a,b),Fraction(*t.ratio))
            count += 1
        self.assertEqual(count,729)
        print("Exact grid:",count)

    def test_tampered_products(self):
        for ds in ((12,24),(16,24),(12,19)):
            with self.subTest(ds=ds), self.assertRaises(ValueError):
                check_products(4,6,3,*ds)
        self.assertNotEqual(Fraction(4,6),Fraction(12,24))
        self.assertEqual(Fraction(4,6),Fraction(16,24))

    def test_equal_and_reverse(self):
        self.assertEqual(transport(4,4,3).ratio,(1,1))
        self.assertEqual(transport(6,4,3).ratio,(3,2))

    def test_modern_boundaries(self):
        for args in ((4,6,1),(4,6,0),(1,6,3),(4,True,3),(4,6,3.0),(0,6,3)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                transport(*args)
        self.assertEqual(Fraction(4*1,6*1),Fraction(4,6))
        self.assertEqual(Fraction(1*3,6*3),Fraction(1,6))
        self.assertEqual(Fraction(0*3,6*3),Fraction(0,6))
        with self.assertRaises(ZeroDivisionError):
            Fraction(4*0,6*0)


if __name__ == "__main__":
    unittest.main()
