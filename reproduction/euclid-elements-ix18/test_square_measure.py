from fractions import Fraction
from itertools import product
import unittest
from square_measure import Measure,square_measure,extend_nonunit


class TestSquareMeasure(unittest.TestCase):
    def test_forward_and_reverse(self):
        self.assertEqual(square_measure(4,6),Measure(36,9,0,9,False))
        self.assertEqual(extend_nonunit(4,6),9)
        self.assertEqual(square_measure(6,4),Measure(16,2,4,None,False))
        with self.assertRaises(ValueError):
            extend_nonunit(6,4)

    def test_non_coprime_fail_and_equal(self):
        self.assertIsNone(square_measure(6,10).witness)
        self.assertEqual(extend_nonunit(7,7),7)

    def test_modern_units(self):
        self.assertEqual(square_measure(1,4),Measure(16,16,0,16,True))
        self.assertEqual(square_measure(4,1),Measure(1,0,1,None,True))
        self.assertEqual(square_measure(1,1).witness,1)
        self.assertEqual(square_measure(4,2),Measure(4,1,0,1,False))
        self.assertEqual(extend_nonunit(4,2),1)
        for args in ((1,4),(4,1),(1,1)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                extend_nonunit(*args)

    def test_invalid_and_large(self):
        for args in ((0,4),(-4,6),(4,6.0),(True,6)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                square_measure(*args)
        z=10**40+3
        self.assertEqual(extend_nonunit(4*z,6*z),9*z)

    def test_bounded_oracle(self):
        count=success=nonunit=unit_outputs=probes=0
        for a,b in product(range(1,41),repeat=2):
            # Find witnesses solely by counting upward in arithmetic progression.
            subtotal=0
            found=None
            for k in range(1,b*b+1):
                subtotal+=a
                probes+=1
                if subtotal>=b*b:
                    if subtotal==b*b:
                        found=k
                    break
            result=square_measure(a,b)
            self.assertEqual(result.witness,found)
            self.assertEqual(result.quotient*a+result.remainder,b*b)
            self.assertTrue(0<=result.remainder<a)
            if found is not None:
                self.assertEqual(Fraction(a,b),Fraction(b,found))
                success+=1
                if min(a,b)>1:
                    self.assertEqual(extend_nonunit(a,b),found)
                    nonunit+=1
                    unit_outputs+=found==1
            count+=1
        self.assertEqual(count,1600)
        self.assertEqual((nonunit-unit_outputs,unit_outputs),(177,5))
        print(f"Grid: {count} ordered pairs; {probes} additive probes; {success} witnesses ({nonunit} nonunit-input pairs: {nonunit-unit_outputs} nonunit outputs, {unit_outputs} unit outputs)")
