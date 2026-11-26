import unittest
from fractions import Fraction
from itertools import product
from math import gcd
from chain_extension import continuation,coprime_endpoint_obstruction


class TestContinuation(unittest.TestCase):
    def test_worked_directions(self):
        self.assertEqual(coprime_endpoint_obstruction((8,12,18,27)),Fraction(81,2))
        self.assertEqual(coprime_endpoint_obstruction((27,18,12,8)),Fraction(16,3))
        self.assertEqual(coprime_endpoint_obstruction((2,3)),Fraction(9,2))

    def test_scaled_counterexample(self):
        self.assertEqual(continuation((16,24,36,54)),81)
        with self.assertRaises(ValueError):
            coprime_endpoint_obstruction((16,24,36,54))

    def test_modern_boundaries(self):
        for chain,value in [((1,2,4),8),((4,2,1),Fraction(1,2)),((7,7,7),7),((1,1),1)]:
            self.assertEqual(continuation(chain),value)
            with self.assertRaises(ValueError):
                coprime_endpoint_obstruction(chain)

    def test_invalid_and_exact(self):
        for chain in ((),(1,),(2,3,5),(0,2),(-1,2),(1.0,2),(True,2)):
            with self.subTest(chain=chain), self.assertRaises(ValueError):
                continuation(chain)
        p=10**40+1
        self.assertEqual(coprime_endpoint_obstruction((p*p,p*(p+1),(p+1)**2)),
                         Fraction((p+1)**3,p))

    def test_bounded_integer_oracle(self):
        accepted=obstructed=integer_witnesses=probes=0
        bound=20
        for length in (2,3,4):
            for chain in product(range(1,bound+1),repeat=length):
                ratios={Fraction(y,x) for x,y in zip(chain,chain[1:])}
                if len(ratios)!=1:
                    with self.assertRaises(ValueError):
                        continuation(chain)
                    continue
                accepted+=1
                a,b=chain[0],chain[1]
                numerator=b*chain[-1]
                found=[k for k in range(1,numerator+1) if a*k==numerator]
                probes+=numerator
                expected=chain[-1]*ratios.pop()
                self.assertEqual(continuation(chain),expected)
                self.assertEqual(found,[int(expected)] if expected.denominator==1 else [])
                integer_witnesses+=bool(found)
                if min(a,chain[-1])>=2 and gcd(a,chain[-1])==1:
                    self.assertEqual(found,[])
                    self.assertEqual(coprime_endpoint_obstruction(chain),expected)
                    obstructed+=1
        print(f"Grid: {sum(bound**k for k in (2,3,4))} input chains; {accepted} geometric; {probes} integer probes; {integer_witnesses} witnesses; {obstructed} coprime nonunit chains obstructed")
