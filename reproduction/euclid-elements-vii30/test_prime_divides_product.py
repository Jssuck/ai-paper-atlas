from fractions import Fraction
from itertools import product
import unittest

from prime_divides_product import Trace, Witness, least_transfer, prove


class TestPrimeProduct(unittest.TestCase):
    def test_fixtures(self):
        w = Witness((7,15),(14,30),2)
        self.assertEqual(prove(7,15,14),Trace(210,30,(False,True),w))
        self.assertEqual(prove(7,14,15),Trace(210,30,(True,False),w))
        self.assertEqual(prove(7,14,21),Trace(294,42,(True,True),None))

    def test_grid(self):
        counts = {(False,True):0,(True,False):0,(True,True):0}
        scanned = 0
        for p,a,b in product(range(2,16),repeat=3):
            ds = [j for j in range(1,p+1) if p%j == 0]
            c = sum([a]*b)
            if ds != [1,p] or c%p:
                with self.assertRaises(ValueError):
                    prove(p,a,b)
            else:
                t = prove(p,a,b)
                expected = (a%p == 0,b%p == 0)
                self.assertEqual(t.divides,expected)
                self.assertTrue(any(expected))
                self.assertEqual(t.product,c)
                self.assertEqual(p*t.product_quotient,c)
                if t.witness:
                    w = t.witness
                    self.assertEqual(Fraction(*w.ratio),Fraction(*w.compared))
                    self.assertEqual(tuple(w.scale*x for x in w.ratio),w.compared)
                counts[expected] += 1
            scanned += 1
        self.assertEqual(scanned,2744)
        self.assertTrue(all(counts.values()))
        print(f"Exact grid: {scanned} triples; branches {counts}")

    def test_composite_failure(self):
        self.assertEqual(4*9%6,0)
        self.assertTrue(4%6 and 9%6)
        with self.assertRaisesRegex(ValueError,"prime"):
            prove(6,4,9)

    def test_reject_wrong_premise(self):
        for args in ((7,8,9),(1,8,9),(7,1,14),(7,0,14),(7,14,15.0)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                prove(*args)
        for args in ((7,15,14,31),(6,4,9,6)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                least_transfer(*args)

    def test_single_count(self):
        self.assertEqual(prove(7,15,7).witness,Witness((7,15),(7,15),1))
