from collections import Counter
import unittest
from mutual_primes import Step,coprime,divisor_oracle,trace


class MutualPrimesTests(unittest.TestCase):
    def test_worked_trace(self):
        state,steps=trace(35,22)
        self.assertEqual(state,"unit-remainder")
        self.assertEqual(steps,(Step(35,22,1,13),Step(22,13,1,9),
                                Step(13,9,1,4),Step(9,4,2,1)))
        self.assertTrue(coprime(35,22))

    def test_grid_and_divisor_oracle(self):
        counts=Counter()
        for a in range(1,65):
            for b in range(1,65):
                state,steps=trace(a,b)
                self.assertEqual(trace(a,b,True),(state,steps))
                self.assertEqual(coprime(a,b),divisor_oracle(a,b)==(1,))
                for row in steps:
                    A,B,q,r=row.larger,row.smaller,row.quotient,row.remainder
                    self.assertEqual(A,q*B+r)
                    self.assertTrue(q>=1 and 0<=r<B<A)
                    if r:
                        self.assertEqual(divisor_oracle(A,B),divisor_oracle(B,r))
                    else:
                        self.assertIn(B,divisor_oracle(A,B))
                counts[state]+=1
        self.assertEqual(sum(counts.values()),4096)
        self.assertEqual(counts["input-unit"],127)
        self.assertEqual(counts["input-equal"],63)

    def test_exact_division_examples(self):
        self.assertEqual(trace(21,7),("exact-division",(Step(21,7,3,0),)))
        state,steps=trace(42,18)
        self.assertEqual((state,steps[-1]),("exact-division",Step(18,6,3,0)))
        self.assertFalse(coprime(42,18))

    def test_units_and_equal_inputs_are_modern_extension(self):
        self.assertEqual(trace(1,1),("input-unit",()))
        self.assertEqual(trace(9,1),("input-unit",()))
        self.assertEqual(trace(9,9),("input-equal",()))
        self.assertTrue(coprime(9,1))
        self.assertFalse(coprime(9,9))

    def test_cost_separates_subtractions_from_batches(self):
        _,steps=trace(10001,2)
        self.assertEqual((sum(row.quotient for row in steps),len(steps)),(5000,1))
        self.assertEqual(trace(10001,2,True),("unit-remainder",steps))

    def test_invalid(self):
        for args in ((0,1),(-1,5),(2.0,3),(True,6)):
            with self.assertRaises(ValueError):
                trace(*args)


if __name__=='__main__':
    unittest.main()
