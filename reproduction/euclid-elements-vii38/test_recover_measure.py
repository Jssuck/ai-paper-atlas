from itertools import product
import unittest

from recover_measure import Trace, recover


def block_count(a,b):
    blocks = [list(range(i,min(i+b,a))) for i in range(0,a,b)]
    return len(blocks) if all(len(chunk) == b for chunk in blocks) else None


class TestMeasure(unittest.TestCase):
    def test_example(self):
        self.assertEqual(recover(12,4,3),Trace((0,4,8,12),(0,3,6,9,12),4,4))

    def test_grid(self):
        accepted = 0
        for a,b,c in product(range(2,25),repeat=3):
            if block_count(a,b) != c:
                with self.assertRaises(ValueError):
                    recover(a,b,c)
            else:
                t = recover(a,b,c)
                self.assertEqual(t.unit_count,block_count(b,1))
                self.assertEqual(t.transferred_count,block_count(a,c))
                self.assertEqual(t.transferred_count,b)
                self.assertEqual(tuple(y-x for x,y in zip(t.part_cuts,t.part_cuts[1:])),(b,)*c)
                self.assertEqual(tuple(y-x for x,y in zip(t.transferred_cuts,t.transferred_cuts[1:])),(c,)*b)
                accepted += 1
        print(f"Exact grid: {23**3} triples, {accepted} accepted, {23**3-accepted} rejected")

    def test_mismatch(self):
        for xs in ((14,4,3),(12,4,4),(12,8,3)):
            with self.subTest(xs=xs),self.assertRaises(ValueError):
                recover(*xs)

    def test_modern_boundary(self):
        for xs in ((12,1,12),(12,12,1),(1,1,1)):
            with self.subTest(xs=xs):
                with self.assertRaises(ValueError):
                    recover(*xs)
                self.assertEqual(recover(*xs,modern=True).transferred_count,xs[1])

    def test_invalid(self):
        for xs in ((0,4,3),(12,True,3),(12,4,3.0),(-12,4,3)):
            with self.subTest(xs=xs),self.assertRaises(ValueError):
                recover(*xs,modern=True)
