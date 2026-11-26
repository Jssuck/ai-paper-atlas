from itertools import product
from math import isqrt
import unittest

from prime_power_divisors import extraction_trace, proper_nonunit_divisors


class TestPrimePowerDivisors(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(proper_nonunit_divisors(3,4),(3,9,27))
        self.assertEqual(extraction_trace(3,4,27),(3,(27,9,3,1)))

    def test_endpoints_and_invalid(self):
        self.assertEqual(proper_nonunit_divisors(7,1),())
        for divisor in (1,81,12,243,False,9.0):
            with self.subTest(divisor=divisor),self.assertRaises(ValueError):
                extraction_trace(3,4,divisor)
        for args in ((1,3),(9,2),(3,0),(3,3.0),(True,3)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                proper_nonunit_divisors(*args)

    def test_composite_base_control(self):
        self.assertEqual(6**2%4,0)
        self.assertNotIn(4,(6,))
        with self.assertRaises(ValueError):
            proper_nonunit_divisors(6,2)

    def test_large_exact_trace(self):
        self.assertEqual(extraction_trace(2,200,2**199),(199,tuple(2**e for e in range(199,-1,-1))))

    def test_paired_search_oracle(self):
        targets=certificates=probes=0
        for p,n in product((2,3,5,7,11,13,17,19),range(1,7)):
            value=p**n
            found=set()
            for divisor in range(2,isqrt(value)+1):
                probes+=1
                quotient,remainder=divmod(value,divisor)
                if not remainder:
                    found.update((divisor,quotient))
            predicted=proper_nonunit_divisors(p,n)
            self.assertEqual(predicted,tuple(sorted(found)))
            for divisor in found:
                e,trace=extraction_trace(p,n,divisor)
                self.assertEqual(divisor,p**e)
                self.assertEqual(trace,tuple(p**i for i in range(e,-1,-1)))
                certificates+=1
            targets+=1
        self.assertEqual((targets,certificates),(48,120))
        print(f"Grid: {targets} prime powers; {probes} paired divisor probes; {certificates} extraction certificates")
