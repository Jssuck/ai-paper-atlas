from itertools import product
from fractions import Fraction
from math import gcd
import unittest
from coprime_sums import coprime_sums,normalize_chain


class TestCoprimeSums(unittest.TestCase):
    def test_worked_and_reverse(self):
        r=coprime_sums(2,3)
        self.assertEqual((r.chain,r.sums,r.common_divisors),((4,6,9),(15,13,10),(1,1,1)))
        self.assertEqual(coprime_sums(3,2).chain,r.chain[::-1])

    def test_nonminimal_and_nongeometric(self):
        self.assertEqual(normalize_chain(8,12,18)[0],2)
        self.assertEqual([gcd(x,38-x) for x in (8,12,18)],[2]*3)
        self.assertEqual(gcd(3,4+5),3)
        with self.assertRaises(ValueError):
            normalize_chain(3,4,5)

    def test_modern_units_and_bad_inputs(self):
        self.assertTrue(coprime_sums(1,1).modern_unit)
        self.assertTrue(coprime_sums(1,3).modern_unit)
        self.assertEqual(normalize_chain(7,7,7)[0],7)
        for args in ((2,4),(0,1),(True,3),(1,1.0)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                coprime_sums(*args)

    def test_large_exact(self):
        a=10**40+1
        self.assertEqual(coprime_sums(a,a+1).common_divisors,(1,1,1))

    def test_grid(self):
        bound=36
        geometric=nonminimal=checks=0
        for x,y,z in product(range(1,bound+1),repeat=3):
            if Fraction(y,x)!=Fraction(z,y):
                with self.assertRaises(ValueError):
                    normalize_chain(x,y,z)
                continue
            geometric+=1
            scale=gcd(gcd(x,y),z)
            nonminimal+=scale>1
            primitive=(x//scale,y//scale,z//scale)
            got_scale,r=normalize_chain(x,y,z)
            self.assertEqual((got_scale,r.chain),(scale,primitive))
            for i in range(3):
                subtotal=sum(primitive[j] for j in range(3) if j!=i)
                self.assertEqual(r.sums[i],subtotal)
                self.assertFalse(any(primitive[i]%d==subtotal%d==0
                                     for d in range(2,min(primitive[i],subtotal)+1)))
                checks+=1
        print(f"Grid: {bound**3} ordered triples; {geometric} geometric ({nonminimal} nonminimal); {checks} primitive sum checks")
