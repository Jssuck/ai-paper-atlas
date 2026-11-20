from fractions import Fraction as F
from itertools import product
import unittest

from ratio_chains import Ratio, bounded_mismatch, exact_chain, probe_chain, same_exact


class V11(unittest.TestCase):
    equal = Ratio(2,3), Ratio(4,6,"area"), Ratio(6,9,"mass")
    near = Ratio(101,100), Ratio(102,100), Ratio(103,100)

    def test_all_three_signs(self):
        for m,n,s in ((1,1,-1),(3,2,0),(2,1,1)):
            self.assertEqual(probe_chain(*self.equal,m,n),(s,s,s))

    def test_cross_kind_ratios_allowed(self):
        self.assertTrue(exact_chain(*self.equal))
        self.assertTrue(same_exact(self.equal[0],self.equal[2]))

    def test_within_pair_kind_rejected(self):
        with self.assertRaises(ValueError):
            Ratio.from_typed(1,"area",1,"length")

    def test_false_left_or_right_premise(self):
        a,b,c = Ratio(2,3), Ratio(4,6), Ratio(1,1)
        self.assertFalse(exact_chain(c,a,b))
        self.assertFalse(exact_chain(a,b,c))

    def test_equal_endpoints_not_all_equal(self):
        a,b,c = Ratio(2,3), Ratio(1,1), Ratio(4,6)
        self.assertTrue(same_exact(a,c))
        self.assertFalse(exact_chain(a,b,c))
        self.assertEqual(probe_chain(a,b,c,1,1),(-1,0,-1))

    def test_bounded_false_agreement(self):
        self.assertIsNone(bounded_mismatch(*self.near,20))
        self.assertFalse(exact_chain(*self.near))
        self.assertEqual(bounded_mismatch(*self.near,40),(34,35,(-1,-1,1)))

    def test_mismatch_at_equality_boundary(self):
        self.assertEqual(probe_chain(*self.near,50,51),(-1,0,1))

    def test_multiplier_must_be_common(self):
        a,b,c = Ratio(1,2),Ratio(1,3),Ratio(1,4)
        self.assertEqual((a.sign(2,1),b.sign(3,1),c.sign(4,1)),(0,0,0))
        self.assertEqual(probe_chain(a,b,c,2,1),(0,-1,-1))

    def test_positive_exact_inputs(self):
        self.assertTrue(same_exact(Ratio(F(1,2),F(3,4)),Ratio(2,3)))
        for bad in (0,-1,True,0.5):
            with self.assertRaises(ValueError):
                Ratio(bad,1)

    def test_positive_integral_probes(self):
        for bad in (False,0,1.5,F(1),-2):
            with self.assertRaises(ValueError):
                probe_chain(*self.equal,bad,1)
            with self.assertRaises(ValueError):
                bounded_mismatch(*self.equal,bad)

    def test_rational_grid_against_division_oracle(self):
        ratios=[Ratio(i,j) for i,j in product(range(1,5),repeat=2)]
        cases=accepted=0
        for a,b,c in product(ratios,repeat=3):
            qa,qb,qc=(r.first/r.second for r in (a,b,c))
            result=exact_chain(a,b,c)
            self.assertEqual(result,qa==qb==qc)
            accepted += result
            for m,n in product(range(1,4),repeat=2):
                signs=probe_chain(a,b,c,m,n)
                target=F(n,m)
                self.assertEqual(signs,tuple((q>target)-(q<target) for q in (qa,qb,qc)))
                if result:
                    self.assertEqual(len(set(signs)),1)
                cases += 1
        self.assertEqual(cases,36864)
        self.assertEqual(accepted,88)


if __name__ == "__main__":
    unittest.main()
