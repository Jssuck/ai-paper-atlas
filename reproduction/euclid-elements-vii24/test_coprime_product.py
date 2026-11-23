from fractions import Fraction
from itertools import product
import unittest

from coprime_product import Trace, certificate, force_divisor


def factors(n):
    return {d for d in range(2,n+1) if n%d == 0}


class TestProduct(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(certificate(8,9,35),72)
        self.assertEqual(factors(72)&factors(35),set())

    def test_remove_premises(self):
        self.assertEqual(force_divisor(8,10,35,5),Trace(80,5,16,(5,8),2))
        self.assertEqual(factors(80)&factors(35),{5})
        self.assertEqual(factors(72)&factors(14),{2})
        for args in ((8,10,35),(8,9,14)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                certificate(*args)
        with self.assertRaises(ValueError):
            force_divisor(8,9,14,2)

    def test_grid(self):
        theorem = witnesses = 0
        fs = {n:factors(n) for n in range(2,13)}
        for a,b,c in product(range(2,13),repeat=3):
            d = a*b
            common = fs[c]&factors(d)
            if not (fs[a]&fs[c]):
                for e in common:
                    t = force_divisor(a,b,c,e)
                    self.assertIn(e,fs[b])
                    self.assertEqual(Fraction(e,a),Fraction(b,t.f))
                    self.assertEqual((e*t.scale,a*t.scale),(b,t.f))
                    self.assertGreater(t.f,1)
                    witnesses += 1
                if not (fs[b]&fs[c]):
                    self.assertEqual(certificate(a,b,c),d)
                    self.assertFalse(common)
                    theorem += 1
        self.assertGreater(theorem,0)
        self.assertGreater(witnesses,0)
        print(f"Exact grid: 1331 triples, {theorem} theorem cases, {witnesses} witnesses")

    def test_unit_edges(self):
        # Under the retained premise, F=1 would force E=AB; hence A|E|C.
        with self.assertRaisesRegex(ValueError,"coprime"):
            force_divisor(2,3,6,6)
        self.assertEqual(force_divisor(8,5,35,5),Trace(40,5,8,(5,8),1))
        with self.assertRaises(ValueError):
            certificate(1,9,35)

    def test_invalid(self):
        for args in ((8,9,35,5),(8,10,35,2),(8,10,35,1),(8,10,35,5.0)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                force_divisor(*args)
