from itertools import product
from math import lcm,prod
import unittest
from prime_lcm import prime_lcm,strip_foreign_prime


class TestPrimeLCM(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(prime_lcm([2,3,5]),30)
        self.assertEqual(prime_lcm([5,2,5,3]),30)
        self.assertEqual(prime_lcm([7]),7)

    def test_removal(self):
        self.assertEqual(strip_foreign_prime([2,3,5],210,7),30)
        self.assertEqual(strip_foreign_prime([2,3,5],1470,7),210)
        for args in (([2,3,5],30,7),([2,3,5],210,2),([2,3],7,7),([2,3],24,4)):
            with self.subTest(args=args),self.assertRaises(ValueError):
                strip_foreign_prime(*args)

    def test_no_foreign_prime_does_not_imply_minimality(self):
        self.assertEqual(prime_lcm([2,3,5]),30)
        self.assertEqual(60%30,0)
        self.assertEqual({p for p in (2,3,5,7) if 60%p==0},{2,3,5})

    def test_invalid_and_composite_boundaries(self):
        for members in ([],[1],[2,4],[True,3],[2.,3]):
            with self.subTest(members=members),self.assertRaises(ValueError):
                prime_lcm(members)
        self.assertEqual(lcm(4,6),12)
        self.assertNotEqual(prod((4,6)),12)
        self.assertEqual(lcm(4,6)%3,0)

    def test_bounded_oracle(self):
        checked=probes=removed=least_rejections=0
        for n in range(1,5):
            for members in product((2,3,5,7),repeat=n):
                reference=next(k for k in range(1,prod(members)+1)
                               if all(k%p==0 for p in members))
                probes+=reference
                self.assertEqual(prime_lcm(members),reference)
                self.assertEqual(lcm(*members),reference)
                for external in set((2,3,5,7,11))-set(members):
                    with self.assertRaises(ValueError):
                        strip_foreign_prime(members,reference,external)
                    least_rejections+=1
                    candidate=reference*external
                    self.assertEqual(strip_foreign_prime(members,candidate,external),reference)
                    removed+=1
                checked+=1
        self.assertEqual(checked,340)
        print(f"Grid: {checked} ordered lists, {probes} scan candidates, {removed} removals, {least_rejections} least-value rejections")
