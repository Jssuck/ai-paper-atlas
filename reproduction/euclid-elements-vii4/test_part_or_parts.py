import unittest
from collections import Counter
from fractions import Fraction as Q
from part_or_parts import Parts,classify,divisor_oracle


class PartsTests(unittest.TestCase):
    def test_proof_branches(self):
        self.assertEqual(classify(5,8,True),Parts(1,5,8,"coprime-units"))
        self.assertEqual(classify(4,12,True),Parts(4,1,3,"measures-whole"))
        self.assertEqual(classify(6,15,True),Parts(3,2,5,"common-measure"))

    def test_grid_against_fraction_and_divisors(self):
        counts=Counter()
        for b in range(2,81):
            for a in range(1,b):
                answer=classify(a,b)
                g,k,n=answer.step,answer.count,answer.whole_count
                ratio=Q(a,b)
                self.assertEqual((k,n),(ratio.numerator,ratio.denominator))
                self.assertEqual(g,max(divisor_oracle(a,b)))
                self.assertEqual((g*k,g*n),(a,b))
                self.assertTrue(0<k<n)
                self.assertEqual(answer.is_part(),not b%a)
                for d in divisor_oracle(a,b):
                    self.assertGreaterEqual(a//d,k)
                counts[answer.branch]+=1
        self.assertEqual(sum(counts.values()),3160)
        self.assertEqual(counts,{"coprime-units":1886,"common-measure":986,"measures-whole":209,"initial-unit":79})

    def test_noncanonical_refinements(self):
        design=classify(12,18)
        self.assertEqual((design.step,design.count,design.whole_count),(6,2,3))
        self.assertEqual(divisor_oracle(12,18),(1,2,3,6))
        self.assertEqual([(12//d,18//d) for d in (1,2,3,6)],[(12,18),(6,9),(4,6),(2,3)])

    def test_unit_is_modern_extension(self):
        self.assertEqual(classify(1,8),Parts(1,1,8,"initial-unit"))
        with self.assertRaises(ValueError):
            classify(1,8,True)

    def test_invalid(self):
        for args in ((0,5),(-2,6),(4,4),(8,4),(2.0,3),(True,6)):
            with self.assertRaises(ValueError):
                classify(*args)


if __name__=='__main__':
    unittest.main()
