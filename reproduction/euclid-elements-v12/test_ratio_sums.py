from fractions import Fraction as F
from itertools import product
import unittest

from ratio_sums import (
    CLOSE, COMMON, MIXED, bounded_component_mismatch, exact_sum, probe_sum,
    same_unit,
)


class RatioSumTest(unittest.TestCase):
    def test_common_exact(self):
        self.assertEqual(exact_sum(COMMON), ((F(2, 3),)*3, F(2, 3), True))

    def test_three_cases(self):
        for m, n, sign in ((1, 1, -1), (3, 2, 0), (2, 1, 1)):
            with self.subTest(m=m, n=n):
                self.assertEqual(probe_sum(COMMON, m, n), ((sign,)*3, sign))

    def test_masked_counterexample(self):
        self.assertEqual(exact_sum(MIXED), ((F(1, 2), F(1), F(6, 5)), F(1), False))
        self.assertEqual(probe_sum(MIXED, 1, 1), ((-1, 0, 1), 0))

    def test_weighted_not_simple_mean(self):
        ratios, total, _ = exact_sum(MIXED)
        weights = (F(2, 10), F(3, 10), F(5, 10))
        self.assertEqual(total, sum(w*r for w, r in zip(weights, ratios)))
        self.assertNotEqual(total, sum(ratios)/3)

    def test_bounded_false_negative(self):
        self.assertIsNone(bounded_component_mismatch(CLOSE, 20))
        self.assertEqual(bounded_component_mismatch(CLOSE, 40), (34, 35, (-1,-1,1), -1))
        self.assertFalse(exact_sum(CLOSE)[2])

    def test_nonempty_and_variable_length(self):
        with self.assertRaises(ValueError):
            exact_sum(())
        for k in (1, 2, 4, 8):
            p = same_unit(*((i, 2*i) for i in range(1, k+1)))
            self.assertEqual(exact_sum(p), ((F(1, 2),)*k, F(1, 2), True))

    def test_exact_fraction_inputs(self):
        p = same_unit((F(2, 3), 1), (1, F(3, 2)))
        self.assertEqual(exact_sum(p), ((F(2, 3), F(2, 3)), F(2, 3), True))

    def test_type_rules(self):
        with self.assertRaisesRegex(ValueError, "each ratio"):
            exact_sum(((2, 3, "length", "area"),))
        with self.assertRaisesRegex(ValueError, "summands"):
            exact_sum(((2, 3, "length", "length"), (4, 6, "area", "area")))

    def test_reject_invalid_numbers(self):
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                exact_sum(same_unit((bad, 1)))
        for bad in (0.5, True):
            with self.assertRaises(TypeError):
                exact_sum(same_unit((bad, 1)))
        for bad in (0, 2.0, True):
            with self.assertRaises(ValueError):
                probe_sum(COMMON, bad, 1)
            with self.assertRaises(ValueError):
                bounded_component_mismatch(COMMON, bad)

    def test_grid(self):
        vals = tuple(product(range(1, 5), repeat=2))
        chains = matching = checks = 0
        for rows in product(vals, repeat=3):
            p = same_unit(*rows)
            aa, bb = zip(*rows)
            expected = tuple(map(F, aa, bb))
            expected_total = F(sum(aa), sum(bb))
            same = len(set(expected)) == 1
            self.assertEqual(exact_sum(p), (expected, expected_total, same))
            chains += 1
            matching += same
            for m, n in product(range(1, 4), repeat=2):
                threshold = F(n, m)
                signs = tuple((r > threshold)-(r < threshold) for r in expected)
                last = (expected_total > threshold)-(expected_total < threshold)
                self.assertEqual(probe_sum(p, m, n), (signs, last))
                if same:
                    self.assertEqual(signs, (last,)*3)
                checks += 1
        self.assertEqual((chains, matching, checks), (4096, 88, 36864))
