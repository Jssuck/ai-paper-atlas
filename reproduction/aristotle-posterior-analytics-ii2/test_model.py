import unittest
from fractions import Fraction
from model import (powerset, chain, candidates, candidate_count, completions,
                   ratio_in_palette, exhaustive_summary)


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.u = {0, 1, 2}

    def test_powerset(self):
        self.assertEqual(len(powerset(self.u)), 8)
        self.assertEqual(len(powerset([0, 0])), 2)

    def test_valid_chain(self):
        self.assertTrue(chain(self.u, {0}, {0, 1}, self.u))

    def test_invalid_major(self):
        self.assertFalse(chain(self.u, {0}, {0, 1}, {0}))

    def test_invalid_minor(self):
        self.assertFalse(chain(self.u, {0, 1}, {0}, self.u))

    def test_two_candidates(self):
        self.assertEqual(set(candidates(self.u, {0}, {0, 1})),
                         {frozenset({0}), frozenset({0, 1})})

    def test_no_candidate(self):
        self.assertEqual(candidates(self.u, {0}, {1}), ())
        self.assertEqual(candidate_count(self.u, {0}, {1}), 0)

    def test_one_extension_not_cause(self):
        self.assertEqual(candidates(self.u, {0}, {0}), (frozenset({0}),))
        # A single extension is not a claim about causal interpretation.

    def test_empty_subject_vacuity(self):
        self.assertTrue(chain(self.u, set(), set(), set()))
        self.assertEqual(candidate_count(self.u, set(), self.u), 8)

    def test_empty_universe(self):
        self.assertEqual(candidate_count(set(), set(), set()), 1)
        self.assertEqual(exhaustive_summary(0)['valid_chains'], 1)

    def test_outside_domain(self):
        for fn in (candidates, candidate_count):
            with self.assertRaises(ValueError):
                fn(self.u, {3}, set())
        with self.assertRaises(ValueError):
            chain(self.u, set(), {4}, set())

    def test_partial_observation(self):
        worlds = completions(self.u, {0}, {0}, {0})
        self.assertEqual(len(worlds), 16)
        self.assertEqual(sum(m <= a for m, a in worlds), 9)
        self.assertIn((frozenset({0, 1}), frozenset({0})), worlds)

    def test_full_observation(self):
        self.assertEqual(completions(self.u, self.u, {0}, {0}),
                         ((frozenset({0}), frozenset({0})),))

    def test_negative_observation(self):
        worlds = completions({0}, {0}, {0}, set())
        self.assertEqual(worlds, ((frozenset({0}), frozenset()),))
        self.assertFalse(worlds[0][0] <= worlds[0][1])

    def test_bad_labels(self):
        with self.assertRaises(ValueError):
            completions(self.u, {0}, {1}, {0})

    def test_ratio_reduction(self):
        self.assertEqual(ratio_in_palette(440, 220), (Fraction(2), True))
        self.assertEqual(ratio_in_palette(330, 220), (Fraction(3, 2), True))

    def test_rational_not_palette(self):
        self.assertEqual(ratio_in_palette(221, 220), (Fraction(221, 220), False))

    def test_ratio_validation(self):
        for h, l in ((1, 0), (0, 1), (1, 2), (-1, 1)):
            with self.assertRaises(ValueError):
                ratio_in_palette(h, l)
        for h, l in ((True, 1), (2.0, 1), (2, False)):
            with self.assertRaises(TypeError):
                ratio_in_palette(h, l)

    def test_exhaustive(self):
        result = exhaustive_summary()
        self.assertEqual(result['triples'], 512)
        self.assertEqual(result['valid_chains'], 64)
        self.assertEqual(result['nonempty_subject_chains'], 37)
        self.assertEqual(result['candidate_count_checks'], 64)
        self.assertEqual(result['soundness_failures'], 0)
        self.assertEqual(result['candidate_count_failures'], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
