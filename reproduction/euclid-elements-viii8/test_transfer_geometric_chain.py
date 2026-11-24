from fractions import Fraction
from itertools import product
from math import gcd
import unittest

from transfer_geometric_chain import Trace, transfer


class TestTransfer(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(transfer((16,24,36,54),24,81),
            Trace((8,12,18,27),2,3,Fraction(3,2),(24,36,54,81)))

    def test_grid(self):
        count=0
        for a,b,n,s,t in product(range(1,6),range(1,6),range(3,6),range(1,5),range(1,5)):
            if gcd(a,b)>1:
                continue
            row = tuple(a**(n-i-1)*b**i for i in range(n))
            source = tuple(s*x for x in row)
            first,last = t*row[0],t*row[-1]
            trace = transfer(source,first,last,modern=True)
            oracle = tuple(Fraction(x*first,source[0]) for x in source)
            self.assertEqual(trace.chain,oracle)
            self.assertEqual(trace.relative_scale,Fraction(first,source[0]))
            self.assertEqual((trace.old_count,trace.new_count),(s,t))
            self.assertEqual(trace.chain[-1],last)
            count += 1
        self.assertEqual(count,912)
        print("Exact grid:",count)

    def test_endpoints_do_not_determine_length(self):
        self.assertEqual(transfer((4,16,64),4,64).chain,(4,16,64))
        self.assertEqual(transfer((4,8,16,32,64),4,64).chain,(4,8,16,32,64))

    def test_wrong_endpoint_data(self):
        for first,last in ((81,24),(24,62),(24,82)):
            with self.subTest(first=first,last=last),self.assertRaisesRegex(ValueError,"ordered"):
                transfer((16,24,36,54),first,last)

    def test_scope(self):
        self.assertEqual(transfer((1,3,9),2,18,modern=True).chain,(2,6,18))
        self.assertEqual(transfer((5,5,5),7,7,modern=True).chain,(7,7,7))
        for source,first,last in (((1,3,9),2,18),((5,5,5),7,7),((4,8),8,16),
                                  ((4,8,17),8,34),((4,8,16),True,4),((4,8,16),0,0)):
            with self.assertRaises(ValueError):
                transfer(source,first,last)
