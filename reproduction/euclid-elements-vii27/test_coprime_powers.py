from itertools import product
import unittest

from coprime_powers import Trace, binary_gcd, prove


def common(a,b):
    return [d for d in range(2,min(a,b)+1) if a%d == b%d == 0]


class TestPowers(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(prove(8,15),Trace(((64,15),(64,225),(8,225)),
            ((8,15),(8,225),(64,15),(64,225)),(512,3375)))

    def test_grid(self):
        yes = no = 0
        for a,b in product(range(2,21),repeat=2):
            divisors = common(a,b)
            expected = max(divisors,default=1)
            self.assertEqual(binary_gcd(a,b),expected)
            if divisors:
                with self.assertRaises(ValueError):
                    prove(a,b)
                self.assertEqual(binary_gcd(a**3,b**3),expected**3)
                no += 1
            else:
                t = prove(a,b)
                self.assertEqual(t.cubes,(a**3,b**3))
                for p in (*t.square_steps,*t.cross_pairs,t.cubes):
                    self.assertFalse(common(*p))
                    self.assertEqual(binary_gcd(*p),1)
                yes += 1
        self.assertEqual(yes+no,361)
        print(f"Exact grid: 361 pairs, {yes} accepted, {no} rejected")

    def test_bad_premise(self):
        self.assertEqual(common(6,15),[3])
        self.assertEqual(binary_gcd(6**3,15**3),27)
        with self.assertRaises(ValueError):
            prove(6,15)

    def test_reverse(self):
        self.assertEqual(prove(15,8).cubes,(3375,512))

    def test_scope(self):
        for inputs in ((1,15),(8,0),(-8,15),(True,15),(8.0,15)):
            with self.subTest(inputs=inputs), self.assertRaises(ValueError):
                prove(*inputs)
