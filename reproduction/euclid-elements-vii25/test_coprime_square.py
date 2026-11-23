from itertools import product
import unittest

from coprime_square import Trace, product_lemma, square


def common(a,b):
    return [i for i in range(2,min(a,b)+1) if a%i == b%i == 0]


class TestSquare(unittest.TestCase):
    def test_worked(self):
        self.assertEqual(square(8,15),Trace((8,8),15,64))
        self.assertEqual(common(64,15),[])
        self.assertEqual(common(8,8),[2,4,8])

    def test_grid(self):
        accepted = rejected = 0
        for a,b in product(range(2,31),repeat=2):
            if common(a,b):
                with self.assertRaises(ValueError):
                    square(a,b)
                self.assertTrue(common(a*a,b))
                rejected += 1
            else:
                t = square(a,b)
                self.assertEqual(t,Trace((a,a),b,a*a))
                self.assertEqual(common(t.square,b),[])
                accepted += 1
        self.assertEqual(accepted+rejected,841)
        print(f"Exact grid: 841 pairs, {accepted} coprime, {rejected} noncoprime")

    def test_bad_premise(self):
        self.assertEqual(common(6,15),[3])
        self.assertEqual(common(36,15),[3])
        with self.assertRaisesRegex(ValueError,"coprime"):
            square(6,15)

    def test_two_distinct_slots(self):
        self.assertEqual(product_lemma(8,8,15),64)
        self.assertEqual(product_lemma(8,2,15),16)
        for args in ((8,3,15),(3,8,15)):
            with self.assertRaisesRegex(ValueError,"coprime"):
                product_lemma(*args)

    def test_modern_boundaries(self):
        self.assertEqual(common(1,15),[])
        for args in ((1,15),(8,1),(0,15),(-8,15),(8.0,15),(True,15)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                square(*args)
