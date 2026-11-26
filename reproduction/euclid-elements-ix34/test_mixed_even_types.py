from itertools import product
import unittest

from mixed_even_types import Witness,mixed_even_types


class TestMixedEvenTypes(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(mixed_even_types(12),Witness((12,6,3),(6,2),(3,4),(4,3)))
        self.assertEqual(mixed_even_types(24),Witness((24,12,6,3),(12,2),(3,8),(8,3)))

    def test_outside(self):
        for n in (2,4,16,18,9,1,0,-12,True,12.0):
            with self.subTest(n=n),self.assertRaises(ValueError):
                mixed_even_types(n)

    def test_large_exact(self):
        n=7*2**200
        self.assertEqual(mixed_even_types(n).odd_divisor_pair,(7,2**200))

    def test_independent_grouping(self):
        cap=256
        factors={n:set() for n in range(2,cap+1)}
        for a,b in product(range(2,cap//2+1),repeat=2):
            if a*b<=cap:
                factors[a*b].add((a,b))
        both=pairs=even=0
        for n,group in factors.items():
            ep={(a,b) for a,b in group if a%2==0 and b%2==0}
            op={(a,b) for a,b in group if a%2 and b%2==0}
            pairs+=len(group)
            even+=n%2==0
            if not (ep and op):
                with self.assertRaises(ValueError):
                    mixed_even_types(n)
                continue
            w=mixed_even_types(n)
            self.assertIn(w.even_pair,ep)
            self.assertIn(w.odd_divisor_pair,op)
            self.assertIn(w.reversed_mixed_pair,group)
            self.assertEqual(w.reversed_mixed_pair,w.odd_divisor_pair[::-1])
            self.assertTrue(all(a==b+b for a,b in zip(w.halving_chain,w.halving_chain[1:])))
            both+=1
        self.assertEqual((len(factors),even,both),(255,128,57))
        print(f"Grid: {len(factors)} values ({even} even); {pairs} ordered nonunit pairs; {both} both categories")
