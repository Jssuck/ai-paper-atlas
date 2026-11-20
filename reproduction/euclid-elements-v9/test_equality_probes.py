from fractions import Fraction
from itertools import product
import unittest

from equality_probes import Magnitude as M, bounded_mismatch, distinguish, probe


class V9(unittest.TestCase):
    def test_identical_three_signs(self):
        for m, n, s in ((1,2,-1),(2,2,0),(3,2,1)):
            self.assertEqual(probe(M(1), M(1), M(1), m, n), ((s,s),(-s,-s)))

    def test_equal_returns_none(self):
        self.assertIsNone(distinguish(M(Fraction(1,2)), M(Fraction(2,4)), M(7)))

    def test_a_larger(self):
        k = distinguish(M(7), M(4), M(4))
        self.assertEqual((k.larger,k.m,k.n,k.forward,k.reverse), ("a",2,3,(1,-1),(-1,1)))

    def test_b_larger(self):
        k = distinguish(M(4), M(7), M(4))
        self.assertEqual((k.larger,k.m,k.n,k.forward,k.reverse), ("b",2,3,(-1,1),(1,-1)))

    def test_weak_witness_also_refutes_v5(self):
        self.assertEqual(probe(M(3), M(2), M(2), 1, 1), ((1,0),(-1,0)))

    def test_finite_false_positive(self):
        a,b,c = map(M, (102,101,100))
        self.assertIsNone(bounded_mismatch(a,b,c,20))
        self.assertEqual(bounded_mismatch(a,b,c,51), (50,51))
        k = distinguish(a,b,c)
        self.assertEqual((k.m,k.n,k.forward,k.reverse), (101,103,(1,-1),(-1,1)))

    def test_rational_mesh(self):
        vals = sorted({Fraction(i,j) for i,j in product(range(1,6),repeat=2)})
        self.assertEqual(len(vals), 19)
        count = 0
        for a,b,c in product(vals, repeat=3):
            k = distinguish(M(a),M(b),M(c))
            count += 1
            if a == b:
                self.assertIsNone(k)
            else:
                sign = 1 if a>b else -1
                self.assertLess(k.m*min(a,b), k.n*c)
                self.assertLess(k.n*c, k.m*max(a,b))
                self.assertEqual((k.forward,k.reverse), ((sign,-sign),(-sign,sign)))
        self.assertEqual(count, 6859)

    def test_nonlength_homogeneous(self):
        k = distinguish(M(2,"area"), M(1,"area"), M(9,"area"))
        self.assertEqual(k.forward, (1,-1))

    def test_mixed_kind_rejected_even_when_equal(self):
        a,b,c = M(1), M(1), M(1,"area")
        for fn,args in ((distinguish,()), (probe,(1,1)), (bounded_mismatch,(2,))):
            with self.assertRaises(ValueError):
                fn(a,b,c,*args)

    def test_nonpositive_or_inexact_magnitude(self):
        for bad in (0,-1,True,1.5):
            with self.assertRaises(ValueError):
                M(bad)

    def test_invalid_multiplier_or_bound(self):
        a = M(1)
        for bad in (0,-1,True,Fraction(2,1)):
            with self.assertRaises(ValueError):
                probe(a,a,a,1,bad)
            with self.assertRaises(ValueError):
                bounded_mismatch(a,a,a,bad)


if __name__ == "__main__":
    unittest.main()
