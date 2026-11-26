from itertools import product
import unittest
from half_measure import Witness,half_measure


class TestMeasure(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(half_measure(3,24),Witness(8,12,4))
        self.assertEqual(half_measure(5,10),Witness(2,5,1))

    def test_even_divisor_counterexample(self):
        self.assertEqual(12%4,0)
        self.assertNotEqual((12//2)%4,0)
        with self.assertRaises(ValueError):
            half_measure(4,12)

    def test_domain(self):
        for args in ((3,10),(9,6),(3,9),(1,8),(3,0),(-3,6),(True,6),(3.0,6)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                half_measure(*args)

    def test_large_small_quotient(self):
        a=10**100+1
        self.assertEqual(half_measure(a,6*a),Witness(6,3*a,3))

    def test_grid(self):
        accepted=out_of_scope=fail_measure=steps=unit=0
        for a,b in product(range(1,65),repeat=2):
            if a<3 or a%2!=1 or b%2:
                out_of_scope+=1
            elif b%a:
                fail_measure+=1
            else:
                half=b//2
                self.assertEqual(half%a,0)
                self.assertEqual(half_measure(a,b),Witness(b//a,half,half//a))
                accepted+=1
                steps+=b//a
                unit+=half==a
                continue
            with self.assertRaises(ValueError):
                half_measure(a,b)
        self.assertEqual(accepted+out_of_scope+fail_measure,4096)
        print(f"Grid: {accepted} witnesses ({unit} unit half-quotients); {out_of_scope} domain exclusions; {fail_measure} nondivisible; {steps} accepted subtraction steps")
