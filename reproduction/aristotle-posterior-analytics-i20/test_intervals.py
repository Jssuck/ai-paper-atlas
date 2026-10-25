"""Tests use unittest checks, which remain active under -O and -OO."""
from fractions import Fraction
import unittest
from intervals import StrictOrder, diamond, dyadic_prefix, buffered_prefix, enumerate_forward_dags


class OrderTests(unittest.TestCase):
    def test_transitive_closure(self):
        p = StrictOrder(4, [(0, 1), (1, 2), (2, 3)])
        self.assertEqual(len(p.relation), 6)
        self.assertEqual(p.middle(0, 3), (1, 2))
        self.assertEqual(p.interval(0, 3)['longest_edges'], 3)

    def test_arbitrary_numbering(self):
        p = StrictOrder(4, [(3, 1), (1, 0), (0, 2)])
        self.assertEqual(p.interval(3, 2)['longest_edges'], 3)
        self.assertTrue(p.interval(3, 2)['is_total'])

    def test_cover_and_duplicate_edges(self):
        p = StrictOrder(2, [(0, 1), (0, 1)])
        self.assertEqual(p.middle(0, 1), ())
        self.assertEqual(p.interval(0, 1)['longest_edges'], 1)

    def test_diamond_width_not_depth(self):
        for m in (1, 2, 8, 32, 126):
            with self.subTest(m=m):
                info = diamond(m).interval(0, m + 1)
                self.assertEqual(info['longest_edges'], 2)
                self.assertEqual(info['middle_count'], m)
                self.assertEqual(info['is_total'], m == 1)

    def test_unsupported_endpoints(self):
        p = StrictOrder(3, [(0, 1)])
        for ends in [(1, 0), (0, 0), (0, 2), (-1, 1), (0, True), (0, 3)]:
            with self.subTest(ends=ends):
                with self.assertRaises(ValueError):
                    p.interval(*ends)

    def test_cycle_rejection(self):
        for edges in [[(0, 0)], [(0, 1), (1, 0)], [(0, 1), (1, 2), (2, 0)]]:
            with self.subTest(edges=edges):
                with self.assertRaises(ValueError):
                    StrictOrder(3, edges)

    def test_input_validation(self):
        for n in (-1, True, 1.5, 129):
            with self.subTest(n=n):
                with self.assertRaises(ValueError):
                    StrictOrder(n, [])
        for edges in [[(0, 3)], [(0, False)], [(0,)], ['ab']]:
            with self.subTest(edges=edges):
                with self.assertRaises(ValueError):
                    StrictOrder(3, edges)

    def test_empty_order(self):
        self.assertEqual(StrictOrder(0, []).relation, frozenset())
        self.assertEqual(enumerate_forward_dags(0)['raw_dags'], 1)

    def test_forward_enumeration(self):
        r = enumerate_forward_dags(4)
        self.assertEqual(r['raw_dags'], 64)
        self.assertEqual(r['distinct_transitive_closures'], 40)
        self.assertEqual(r['total_interval_identity_failures'], 0)
        self.assertGreater(r['nontotal_interval_occurrences'], 0)

    def test_count_bounds(self):
        for n in (-1, True, 6):
            with self.subTest(n=n):
                with self.assertRaises(ValueError):
                    enumerate_forward_dags(n)
        for m in (0, -1, True, 127):
            with self.subTest(m=m):
                with self.assertRaises(ValueError):
                    diamond(m)

    def test_rational_exactness(self):
        self.assertEqual(dyadic_prefix(0), (Fraction(0), Fraction(1)))
        for k in (1, 2, 8, 64, 256):
            with self.subTest(k=k):
                values = dyadic_prefix(k)
                self.assertEqual(values[-2], 1 - Fraction(1, 2**k))
                self.assertTrue(all(a < b for a, b in zip(values, values[1:])))
                self.assertEqual((values[-2] + 1) / 2, 1 - Fraction(1, 2**(k + 1)))

    def test_buffer_preserves_tail(self):
        for k in (0, 1, 8):
            with self.subTest(k=k):
                values = buffered_prefix(k)
                self.assertEqual(values[:2], (Fraction(-1), Fraction(0)))
                self.assertEqual(values[1:], dyadic_prefix(k))

    def test_prefix_validation(self):
        for steps in (-1, True, 1.2, 257):
            with self.subTest(steps=steps):
                with self.assertRaises(ValueError):
                    dyadic_prefix(steps)


if __name__ == '__main__':
    unittest.main(verbosity=2)
