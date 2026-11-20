from fractions import Fraction
from itertools import product
import unittest

from order_witness import (
    Magnitude as M, SHARED_DENOMINATOR as D, SHARED_NUMERATOR as N,
    bounded_search, infer_order, scaled_terms,
)


class V10(unittest.TestCase):
    def test_fixed_consequent_equality(self):
        cert = infer_order(M(3),M(2),M(2),1,1,D)
        self.assertEqual((cert.first,cert.second,cert.conclusion), ((3,2),(2,2),"A>B"))

    def test_fixed_antecedent_equality(self):
        cert = infer_order(M(3),M(2),M(2),3,2,N)
        self.assertEqual((cert.first,cert.second,cert.conclusion), ((6,4),(6,6),"A>B"))

    def test_swapping_multipliers_not_invariant_for_weak_witness(self):
        self.assertIsNotNone(infer_order(M(3),M(2),M(2),1,1,D))
        self.assertIsNone(infer_order(M(3),M(2),M(2),1,1,N))
        self.assertIsNotNone(infer_order(M(3),M(2),M(2),3,2,N))
        self.assertIsNone(infer_order(M(3),M(2),M(2),2,3,D))

    def test_strict_sandwich_supports_both(self):
        a,b,c = map(M,(7,4,4))
        self.assertEqual(scaled_terms(a,b,c,2,3,D), ((14,12),(8,12)))
        self.assertEqual(scaled_terms(a,b,c,3,2,N), ((12,8),(12,14)))
        self.assertIsNotNone(infer_order(a,b,c,2,3,D))
        self.assertIsNotNone(infer_order(a,b,c,3,2,N))

    def test_first_greater_alone_not_enough(self):
        for orientation in (D,N):
            self.assertIsNone(infer_order(M(3),M(2),M(1 if orientation==D else 5),1,1,orientation))

    def test_no_witness_for_equal_or_opposite(self):
        for a,b in ((2,2),(2,3)):
            for orientation in (D,N):
                self.assertIsNone(bounded_search(M(a),M(b),M(2),12,orientation))

    def test_finite_no_evidence(self):
        a,b,c = map(M,(102,101,100))
        for orientation,expected in ((D,(51,52)),(N,(51,50))):
            self.assertIsNone(bounded_search(a,b,c,20,orientation))
            cert = bounded_search(a,b,c,52,orientation)
            self.assertEqual((cert.m,cert.n),expected)
            self.assertEqual(cert.conclusion,"A>B")

    def test_rational_mesh_soundness(self):
        vals = sorted({Fraction(i,j) for i,j in product(range(1,5),repeat=2)})
        self.assertEqual(len(vals),11)
        count = accepted = 0
        for a,b,c in product(vals,repeat=3):
            am,bm,cm = map(M,(a,b,c))
            for m,n,orientation in product(range(1,5),range(1,5),(D,N)):
                result = infer_order(am,bm,cm,m,n,orientation)
                expected = (a > n*c/m >= b if orientation==D else a >= m*c/n > b)
                self.assertEqual(result is not None, expected)
                if result is not None:
                    self.assertGreater(a,b)
                    accepted += 1
                count += 1
        self.assertEqual(count,42592)
        self.assertEqual(accepted,6008)

    def test_kind_validation(self):
        for o in (D,N):
            self.assertIsNotNone(infer_order(M(7,"area"),M(4,"area"),M(4,"area"),
                                              2 if o==D else 3, 3 if o==D else 2,o))
            with self.assertRaises(ValueError):
                infer_order(M(3),M(2),M(2,"area"),1,1,o)
            with self.assertRaises(ValueError):
                bounded_search(M(3),M(2),M(2,"area"),2,o)

    def test_illegal_inputs(self):
        for bad in (0,-1,True,1.5):
            with self.assertRaises(ValueError):
                M(bad)
        for bad in (0,-1,True,Fraction(2,1)):
            with self.assertRaises(ValueError):
                infer_order(M(3),M(2),M(2),bad,1,D)
            with self.assertRaises(ValueError):
                bounded_search(M(3),M(2),M(2),bad,D)
        with self.assertRaises(ValueError):
            infer_order(M(3),M(2),M(2),1,1,"unrecognized")


if __name__ == "__main__":
    unittest.main()
