from itertools import product
import unittest
from even_product import Witness,odd_times_even


class TestProduct(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(odd_times_even(3,8),Witness(3,8,12,24))
        self.assertEqual(odd_times_even(3,2),Witness(3,2,3,6))

    def test_even_count_and_swapped(self):
        for args in ((4,8),(8,3),(3,7)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                odd_times_even(*args)
        self.assertEqual(4*8,32)
        self.assertEqual(8*3,24)

    def test_units_and_zero(self):
        for args in ((1,8),(0,8),(3,0),(3,1),(3,-2),(3,True),(3,8.0)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                odd_times_even(*args)

    def test_large_summand(self):
        b=10**100+2
        self.assertEqual(odd_times_even(7,b).half_total,7*(b//2))

    def test_grid(self):
        counts={n+n+1 for n in range(1,32)}
        halves={n+n:n for n in range(1,33)}
        accepted=rejected=added=0
        for a,b in product(range(1,65),repeat=2):
            if a not in counts or b not in halves:
                with self.assertRaises(ValueError):
                    odd_times_even(a,b)
                rejected+=1
                continue
            self.assertEqual(odd_times_even(a,b),Witness(a,b,a*halves[b],a*b))
            accepted+=1
            added+=a
        self.assertEqual((accepted,rejected,added),(992,3104,32736))
        print(f"Grid: {accepted+rejected} ordered pairs; {accepted} accepted; {rejected} rejected; {added} copy steps")
