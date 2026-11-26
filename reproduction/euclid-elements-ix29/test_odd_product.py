from itertools import product
import unittest
from odd_product import Witness,odd_times_odd


class TestOddProduct(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(odd_times_odd(3,5),Witness(3,6,1,7,15))
        self.assertEqual(odd_times_odd(5,3),Witness(5,5,2,7,15))

    def test_even_substitutions(self):
        for a,b,result in ((4,5,20),(3,6,18),(4,6,24)):
            self.assertEqual(a*b,result)
            with self.assertRaises(ValueError):
                odd_times_odd(a,b)

    def test_boundaries(self):
        for args in ((1,5),(3,1),(0,5),(3,0),(-3,5),(3,True),(3,5.0)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                odd_times_odd(*args)

    def test_large_exact(self):
        b=10**100+1
        self.assertEqual(odd_times_odd(3,b).total,3*b)

    def test_independent_grid(self):
        odd_halves={h+h+1:h for h in range(1,32)}
        yes=no=steps=0
        for a,b in product(range(1,65),repeat=2):
            if a not in odd_halves or b not in odd_halves:
                with self.assertRaises(ValueError):
                    odd_times_odd(a,b)
                no+=1
                continue
            out=odd_times_odd(a,b)
            self.assertEqual(out,Witness(a,a*odd_halves[b],odd_halves[a],(a*b-1)//2,a*b))
            yes+=1
            steps+=a
        self.assertEqual((yes,no,steps),(961,3135,31713))
        print(f"Grid: {yes+no} pairs; {yes} accepted; {no} rejected; {steps} copy steps")
