import unittest
from fractions import Fraction as Q
from itertools import product
from arcs import Arc, copy_smaller, inspect

def arc(r, start, sweep):
    return Arc(Q(r), Q(start), Q(start) + Q(sweep))

class Arcs(unittest.TestCase):
    def test_equal_across_origins(self):
        self.assertEqual(inspect(arc(3, 0, '1/5'), arc(3, '9/10', '1/5')),
                         dict(premises=True, central=True, inscribed=True))

    def test_wraparound_witness(self):
        large = arc(2, '11/12', '1/4')
        small = arc(2, '1/2', '1/12')
        self.assertTrue(large.contains_interior(copy_smaller(small, large).end))
        self.assertEqual(inspect(large, small),
                         dict(premises=False, central=False, inscribed=False,
                              copy_matches_small=True, copy_shorter_than_large=True))

    def test_unequal_radius_equal_lengths(self):
        a, b = arc(2, 0, '1/4'), arc(1, 0, '1/2')
        self.assertEqual(a.length_over_tau, b.length_over_tau)
        self.assertNotEqual(a.sweep, b.sweep)
        self.assertEqual(inspect(a, b), dict(premises=False, reason="radius"))

    def test_wrong_arc_same_endpoints(self):
        a = arc(2, 0, '1/4')
        b = Arc(a.radius, a.end, a.start)
        self.assertEqual(b.sweep, Q(3, 4))
        self.assertFalse(inspect(a, b)["premises"])

    def test_cross_type_not_equal(self):
        a = arc(2, 0, '1/2')
        self.assertEqual(a.inscribed, Q(1, 4))
        self.assertNotEqual(a.inscribed, a.sweep)

    def test_invalid_input(self):
        for r, s, e in [(Q(0), Q(0), Q(1, 2)), (Q(1), Q(0), Q(1))]:
            with self.assertRaises(ValueError):
                Arc(r, s, e)
        with self.assertRaises(TypeError):
            Arc(Q(1), 0.0, Q(1, 2))

    def test_non_subarc_copy_rejected(self):
        a = arc(1, 0, '1/4')
        with self.assertRaises(ValueError):
            copy_smaller(a, a)

    def test_exhaustive_grid(self):
        counts = [0, 0]
        for r, offset, i, j in product((1, 3), range(12), range(1, 12), range(1, 12)):
            a = arc(r, Q(offset, 12), Q(i, 12))
            b = arc(r, Q(11-offset, 12), Q(j, 12))
            report = inspect(a, b)
            self.assertEqual((report["premises"], report["central"], report["inscribed"]),
                             (i == j,) * 3)
            if i != j:
                self.assertTrue(report["copy_matches_small"])
                self.assertTrue(report["copy_shorter_than_large"])
            counts[int(i != j)] += 1
        self.assertEqual(counts, [264, 2640])

if __name__ == "__main__":
    unittest.main()
