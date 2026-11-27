from fractions import Fraction as F
from itertools import product
from unittest import TestCase

from ratio_witness import ratio, transfer


def kernel(n):
    """Independent squarefree signature by removing repeated prime factors."""
    p = 2
    while p*p <= n:
        while n % (p*p) == 0:
            n //= p*p
        p += 1
    return n


class TestX13(TestCase):
    def test_transfer_and_scaling(self):
        self.assertEqual(ratio(2,8),F(1,2))
        self.assertIsNone(transfer(2,8,3))
        self.assertIsNone(transfer(F(2,49),F(8,49),F(3,49)))
        self.assertIsNone(transfer(1,4,2))
        self.assertIsNone(transfer(2,2,3))

    def test_nontransitivity(self):
        self.assertIsNone(ratio(1,2))
        self.assertIsNone(ratio(2,4))
        self.assertEqual(ratio(1,4),F(1,2))

    def test_invalid(self):
        for args in [(1,2,3),(1,4,9),(0,1,2),(1,1,-1),(1.,4,2),(True,4,2)]:
            with self.assertRaises(ValueError):
                transfer(*args)

    def test_grid(self):
        sig = {i:kernel(i) for i in range(1,25)}
        accepted = 0
        for a,b,c in product(sig,repeat=3):
            local_scale = ratio(a,b)
            self.assertEqual(local_scale is not None,sig[a] == sig[b])
            if local_scale is not None:
                self.assertEqual(local_scale**2,F(a,b))
            if sig[a] == sig[b] and sig[a] != sig[c]:
                self.assertIsNone(transfer(a,b,c))
                accepted += 1
            else:
                with self.assertRaises(ValueError):
                    transfer(a,b,c)
        self.assertEqual(accepted,1026)
        print(f"Grid: {24**3} ordered triples; admissible={accepted}; rejected={24**3-accepted}")
