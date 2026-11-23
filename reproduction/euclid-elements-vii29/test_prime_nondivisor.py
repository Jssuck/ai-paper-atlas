from itertools import product
import unittest

from prime_nondivisor import Trace, common_witness, inspect, prime, prove


def factors(n):
    return {d for d in range(1,n+1) if n%d == 0}


class TestPrime(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(prove(7,15),Trace(1,1,True))
        self.assertEqual(prove(13,6),Trace(1,6,True))

    def test_witness(self):
        self.assertEqual(common_witness(7,14,7),2)
        with self.assertRaisesRegex(ValueError,"must not measure"):
            prove(7,14)
        with self.assertRaisesRegex(ValueError,"does not measure"):
            common_witness(7,15,7)

    def test_composites(self):
        self.assertEqual(inspect(6,9),Trace(3,3,False))
        self.assertEqual(inspect(8,15),Trace(1,7,True))
        for pair in ((6,9),(8,15)):
            with self.assertRaisesRegex(ValueError,"prime"):
                prove(*pair)

    def test_grid(self):
        accepted = witnesses = checked = 0
        for p,n in product(range(2,31), repeat=2):
            oracle = factors(p)
            ds = oracle & factors(n)
            self.assertEqual(inspect(p,n).common_measure,max(ds))
            self.assertEqual(prime(p),oracle == {1,p})
            if oracle != {1,p} or p in ds:
                with self.assertRaises(ValueError):
                    prove(p,n)
                if oracle == {1,p}:
                    self.assertEqual(common_witness(p,n,p)*p,n)
                    witnesses += 1
            else:
                self.assertEqual(ds,{1})
                self.assertTrue(prove(p,n).coprime)
                accepted += 1
            checked += 1
        self.assertEqual(checked,841)
        print(f"Exact grid: {checked} pairs, {accepted} theorem cases, {witnesses} prime-divisor witnesses")

    def test_unit_boundary(self):
        self.assertEqual(factors(1),{1})
        for args in ((1,7),(7,1),(0,7),(True,7),(7,2.0)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                prove(*args)
