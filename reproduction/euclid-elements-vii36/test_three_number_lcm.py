from itertools import permutations, product
from math import gcd
import unittest

from three_number_lcm import Trace, construct, transfer


def direct(*xs):
    upper = 1
    for x in xs:
        upper *= x
    return next(m for m in range(max(xs),upper+1) if all(m%x == 0 for x in xs))


class TestThree(unittest.TestCase):
    def test_branches(self):
        self.assertEqual(construct(12,18,9),Trace(36,36,"already measured"))
        self.assertEqual(construct(6,10,14),Trace(30,210,"second construction"))
        self.assertEqual(transfer(6,10,14,420),(14,2))

    def test_grid(self):
        branches = {}
        checked = 0
        for a,b,c in product(range(2,13),repeat=3):
            t = construct(a,b,c)
            self.assertEqual(t.result,direct(a,b,c))
            self.assertEqual(t.pair_multiple,direct(a,b))
            branch = "already measured" if t.pair_multiple%c == 0 else "second construction"
            self.assertEqual(t.branch,branch)
            branches[branch] = branches.get(branch,0)+1
            for m in range(max(a,b,c),a*b*c+1):
                if m%a == m%b == m%c == 0:
                    self.assertEqual(transfer(a,b,c,m),(m//t.pair_multiple,m//t.result))
                    checked += 1
        self.assertEqual(sum(branches.values()),1331)
        print("Exact grid:",branches,"common multiple transfers:",checked)

    def test_permutations_and_nesting(self):
        for xs in permutations((6,10,14)):
            self.assertEqual(construct(*xs).result,210)
        for xs in permutations((3,6,18)):
            self.assertEqual(construct(*xs).result,18)
        self.assertEqual(construct(12,12,12).result,12)

    def test_bad_shortcuts(self):
        a,b,c = 6,10,14
        goal = construct(a,b,c).result
        self.assertEqual(max(direct(a,b),direct(a,c),direct(b,c)),70)
        self.assertEqual(a*b*c//gcd(gcd(a,b),c),420)
        self.assertEqual(goal,210)

    def test_scope(self):
        self.assertEqual(construct(1,4,6,modern=True).result,12)
        for xs in ((1,4,6),(0,4,6),(-2,4,6),(True,4,6),(2,4,6.0)):
            with self.subTest(xs=xs),self.assertRaises(ValueError):
                construct(*xs)
        with self.assertRaises(ValueError):
            transfer(6,10,14,70)
