import unittest
from fractions import Fraction
from itertools import product

from witness import Magnitude as M, bounded_witness, certifies, construct, sample_cases, witness_signs


class V8Tests(unittest.TestCase):
    def check_witness(self, a, b, c):
        p = construct(a, b, c)
        self.assertLess(p.small_multiple, p.shared_multiple)
        self.assertLess(p.shared_multiple, p.large_multiple)
        self.assertEqual(witness_signs(a, c, b, c, p.m, p.n), (1, -1))
        self.assertEqual(witness_signs(c, b, c, a, p.n, p.m), (1, -1))
        return p

    def test_three_gap_branches(self):
        for label, triple in sample_cases():
            with self.subTest(label=label):
                self.assertEqual(self.check_witness(*triple).branch, label)

    def test_rational_grid(self):
        values = tuple(sorted({Fraction(p, q) for p, q in product(range(1, 6), repeat=2)}))
        self.assertEqual(len(values), 19)
        tested = 0
        for a, b, c in product(map(M, values), repeat=3):
            if a.value > b.value:
                self.check_witness(a, b, c)
                tested += 1
        self.assertEqual(tested, 3249)

    def test_choose_first_multiple_strictly_beyond(self):
        p = self.check_witness(M(8), M(3), M(2))
        self.assertEqual((p.m, p.n), (1, 3))
        self.assertEqual(p.shared_multiple, 6)

    def test_weak_second_comparison_may_be_equal(self):
        a, b, c = M(3), M(2), M(2)
        self.assertEqual(witness_signs(a, c, b, c, 1, 1), (1, 0))
        self.assertTrue(certifies(a, c, b, c, 1, 1))
        self.assertFalse(certifies(c, b, c, a, 1, 1))

    def test_strict_first_comparison_cannot_be_equal(self):
        self.assertFalse(certifies(M(3), M(3), M(2), M(3), 1, 1))

    def test_bounded_search_can_miss(self):
        a, b, c = M(102), M(101), M(100)
        self.assertIsNone(bounded_witness(a, c, b, c, 20))
        self.assertEqual(bounded_witness(a, c, b, c, 52), (51, 52))
        self.check_witness(a, b, c)

    def test_equal_and_reversed_are_not_constructor_inputs(self):
        for a, b in ((2, 2), (1, 2)):
            with self.assertRaises(ValueError):
                construct(M(a), M(b), M(3))

    def test_mix_kinds_within_ratio_is_rejected(self):
        with self.assertRaises(ValueError):
            construct(M(5), M(2), M(3, "area"))
        with self.assertRaises(ValueError):
            certifies(M(5), M(2, "area"), M(3), M(1), 2, 1)

    def test_different_kinds_across_homogeneous_ratios(self):
        self.assertTrue(certifies(M(3), M(2), M(4, "area"), M(4, "area"), 1, 1))

    def test_invalid_magnitudes(self):
        for bad in (0, -1, 1.5, True):
            with self.assertRaises(ValueError):
                M(bad)

    def test_invalid_probe_parameters(self):
        ratio = (M(2), M(3), M(1), M(3))
        for bad in (0, -1, 1.5, True):
            with self.assertRaises(ValueError):
                certifies(*ratio, bad, 1)
            with self.assertRaises(ValueError):
                bounded_witness(*ratio, bad)
