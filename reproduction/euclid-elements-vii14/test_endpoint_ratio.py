from fractions import Fraction
from itertools import combinations
import unittest

from endpoint_ratio import Trace, ex_aequali


class TestExAequali(unittest.TestCase):
    def test_three_terms(self):
        self.assertEqual(ex_aequali((4,6,10),(10,15,25)),
                         Trace(((2,3),(3,5)), ((2,5),)*3, (2,5), (2,5)))

    def test_independent_grid(self):
        count = 0
        for n in (3,4,5):
            for bases in combinations(range(2,9), n):
                for u,v in combinations(range(1,6), 2):
                    x, y = tuple(u*k for k in bases), tuple(v*k for k in bases)
                    t = ex_aequali(x,y)
                    xs = tuple(Fraction(a,b) for a,b in zip(x,x[1:]))
                    ys = tuple(Fraction(a,b) for a,b in zip(y,y[1:]))
                    self.assertEqual(xs,ys)
                    self.assertEqual(tuple(Fraction(*r) for r in t.adjacent),xs)
                    self.assertEqual(tuple(Fraction(*r) for r in t.vertical),
                                     tuple(Fraction(a,b) for a,b in zip(x,y)))
                    self.assertEqual(Fraction(*t.shared),Fraction(u,v))
                    self.assertEqual(Fraction(*t.endpoints),Fraction(x[0],x[-1]))
                    self.assertEqual(Fraction(x[0],x[-1]),Fraction(y[0],y[-1]))
                    count += 1
        self.assertEqual(count,910)
        print("Exact grid:", count)

    def test_endpoint_only(self):
        x, y = (4,6,10),(10,16,25)
        self.assertEqual(Fraction(x[0],x[-1]),Fraction(y[0],y[-1]))
        self.assertNotEqual(Fraction(x[0],x[1]),Fraction(y[0],y[1]))
        with self.assertRaisesRegex(ValueError,"step 1"):
            ex_aequali(x,y)

    def test_localized_mismatch(self):
        with self.assertRaisesRegex(ValueError,"step 3"):
            ex_aequali((4,6,10,14),(10,15,25,36))
        with self.assertRaises(ValueError):
            ex_aequali((4,6,10),(10,15,25,35))
        with self.assertRaises(ValueError):
            ex_aequali((4,6),(10,15))
        with self.assertRaises(ValueError):
            ex_aequali((1,2,3),(2,4,6))

    def test_modern_direction_boundary(self):
        for x,y in (((10,6,4),(25,15,10)), ((4,4,10),(10,10,25)), ((4,6,10),(4,6,10))):
            self.assertEqual(Fraction(x[0],x[-1]),Fraction(y[0],y[-1]))
            with self.assertRaises(ValueError):
                ex_aequali(x,y)


if __name__ == "__main__":
    unittest.main()
