from itertools import product
import unittest
from missing_powers import Position, positional_certificate, floor_root


def valuations(n):
    factors=[]
    p=2
    while n>1:
        count=0
        while n%p==0:
            n//=p
            count+=1
        if count:
            factors.append(count)
        p+=1
    return factors


class TestMissingPowers(unittest.TestCase):
    def test_two_branches(self):
        self.assertEqual(positional_certificate(8,2,2)[1],Position(2,64,1,8))
        self.assertEqual(positional_certificate(4,3,3)[2],Position(3,64,1,4))
        self.assertEqual(positional_certificate(4,2,3)[1].root,0)
        self.assertEqual(positional_certificate(2,1,2)[0].root,0)

    def test_preconditions(self):
        for args in ((4,3,2),(8,3,3),(64,3,2),(64,3,3),(1,3,2),(2,0,3),
                     (2,3,4),(2,3,2.0),(True,3,2)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                positional_certificate(*args)

    def test_composite_degree_caveat(self):
        self.assertNotEqual(floor_root(4,4)**4,4)
        self.assertEqual(floor_root(4**2,4)**4,4**2)
        self.assertEqual(floor_root(8**2,6)**6,8**2)

    def test_large_exact(self):
        q=(10**40+3)**2+1
        r=positional_certificate(q,4,2)
        self.assertEqual(r[-1].root,q*q)
        self.assertEqual(r[-2].root,0)

    def test_independent_grid(self):
        certified = positive = excluded = 0
        for base,degree in product(range(2,129),(2,3)):
            factors=valuations(base)
            if all(v%degree==0 for v in factors):
                with self.assertRaises(ValueError):
                    positional_certificate(base,12,degree)
                excluded+=1
                continue
            for row in positional_certificate(base,12,degree):
                expected=all((v*row.exponent)%degree==0 for v in factors)
                self.assertEqual(row.value,base**row.exponent)
                self.assertEqual(bool(row.root),expected)
                if expected:
                    self.assertEqual(row.root**degree,row.value)
                certified+=1
                positive+=expected
        print(f"Grid: {certified} positions, {positive} powers, {certified-positive} nonpowers, {excluded} excluded base/degree pairs")
        self.assertEqual(certified+12*excluded,127*2*12)
