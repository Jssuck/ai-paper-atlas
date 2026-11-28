from fractions import Fraction as F
from itertools import product
from unittest import TestCase
from ratio_witness import Witness,classify


def signature(n):
    """Strip square factors using exact integer division, not root extraction."""
    k=2
    while k*k<=n:
        while not n%(k*k):
            n//=k*k
        k+=1
    return n


class TestX19(TestCase):
    def test_examples(self):
        self.assertEqual(classify(2,8),Witness(F(1,2),F(4),(4,1),F(1)))
        self.assertEqual(classify(2,3),Witness(None,None,None,None))
        self.assertEqual(classify(8,2),Witness(F(2),F(4),(4,1),F(1)))

    def test_fractional_and_reference(self):
        self.assertEqual(classify(F(2,3),F(6)),Witness(F(1,3),F(2),(2,1),F(1)))
        self.assertEqual(classify(F(2,9),F(8,9)),Witness(F(1,2),F(4,9),(4,9),F(1,9)))
        # Replace u by 2u, keeping the physical sides and rectangle fixed.
        self.assertEqual(classify(F(2,4),F(8,4)),Witness(F(1,2),F(1),(1,1),F(1)))

    def test_invalid(self):
        for args in [(0,1),(1,0),(-1,1),(1.0,1),(True,1)]:
            with self.assertRaises(ValueError):
                classify(*args)

    def test_grid(self):
        inputs = [F(n,d) for n,d in product(range(1,13),repeat=2)]
        tags = [signature(x.numerator*x.denominator) for x in inputs]
        yes=0
        for i,j in product(range(len(inputs)),repeat=2):
            a,b=inputs[i],inputs[j]
            result = classify(a,b)
            expected = tags[i]==tags[j]
            self.assertEqual(result.length_ratio is not None,expected)
            self.assertEqual(result.area_ratio is not None,expected)
            if expected:
                yes+=1
                self.assertEqual(result.length_ratio**2*b,a)
                self.assertEqual(result.area_ratio**2,a*b)
                m,n=result.area_counts
                self.assertEqual(m*result.measure_in_reference_squares,result.area_ratio)
                self.assertEqual(n*result.measure_in_reference_squares,1)
        self.assertEqual(yes,1696)
        print(f"Grid: {len(inputs)**2} ordered input pairs; both rational={yes}; neither={len(inputs)**2-yes}")
