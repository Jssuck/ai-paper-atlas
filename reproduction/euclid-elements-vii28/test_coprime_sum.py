from itertools import product
import unittest

from coprime_sum import check, from_sum, to_sum


def common(a,b):
    return {d for d in range(2,min(a,b)+1) if a%d == b%d == 0}


class TestSum(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(check(8,15),(1,1,1))
        self.assertEqual(check(5,7),(1,1,1))
        self.assertEqual(check(6,9),(3,3,3))

    def test_transport(self):
        self.assertEqual(to_sum(6,9,3),5)
        self.assertEqual(from_sum(6,9,3),3)
        self.assertEqual(from_sum(9,6,3),2)
        self.assertEqual(from_sum(6,6,6),1)

    def test_grid(self):
        nonunit = 0
        for a,b in product(range(2,21),repeat=2):
            observed = common(a,b)
            self.assertEqual(observed,common(a,a+b))
            self.assertEqual(observed,common(b,a+b))
            self.assertEqual(check(a,b),(max(observed,default=1),)*3)
            for d in observed:
                self.assertEqual(to_sum(a,b,d),(a+b)//d)
                self.assertEqual(from_sum(a,b,d),b//d)
                self.assertEqual(from_sum(b,a,d),a//d)
                nonunit += 1
        print(f"Exact grid: 361 pairs, {nonunit} nonunit common-measure witnesses")

    def test_invalid_witness(self):
        for fn in (to_sum,from_sum):
            for args in ((8,15,2),(8,15,5),(8,15,7)):
                with self.subTest(fn=fn,args=args), self.assertRaises(ValueError):
                    fn(*args)

    def test_scope(self):
        for args in ((1,2),(0,5),(-2,5),(True,5),(2,5.0)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                check(*args)
        self.assertEqual(common(1,5),common(1,6))
