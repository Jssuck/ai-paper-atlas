"""Tests use unittest methods, so -O/-OO do not remove their checks."""
import unittest
from model import eligible_middles, examples, exhaustive_counts, subsets, verify_middle


class MiddleTests(unittest.TestCase):
    def test_valid_certificate(self):
        r = verify_middle({1, 2, 3}, {1, 2}, {1}, {1})
        self.assertTrue(r['certificate'])
        self.assertTrue(r['conclusion'])

    def test_false_minor_rejected(self):
        r = verify_middle({1, 2}, {1, 2}, {2}, {1})
        self.assertTrue(r['conclusion'])
        self.assertTrue(r['major_premise'])
        self.assertFalse(r['minor_premise'])
        self.assertFalse(r['certificate'])

    def test_false_major_rejected(self):
        r = verify_middle({1, 2}, {1}, {1, 2}, {1})
        self.assertTrue(r['minor_premise'])
        self.assertTrue(r['conclusion'])
        self.assertFalse(r['certificate'])

    def test_empty_middle_rejected_for_existing_subject(self):
        r = verify_middle({1}, {1}, set(), {1})
        self.assertFalse(r['certificate'])

    def test_empty_subject_policy(self):
        r = verify_middle({1}, set(), set(), set())
        self.assertTrue(r['minor_premise'])
        self.assertTrue(r['major_premise'])
        self.assertTrue(r['conclusion'])
        self.assertFalse(r['subject_exists'])
        self.assertFalse(r['certificate'])

    def test_empty_universe_policy(self):
        self.assertFalse(verify_middle(set(), set(), set(), set())['certificate'])

    def test_outside_domain_rejected(self):
        for a, b, c in [({2}, set(), set()), (set(), {2}, set()), (set(), set(), {2})]:
            with self.assertRaises(ValueError):
                verify_middle({1}, a, b, c)

    def test_multiple_candidates_not_unique_cause(self):
        u, a, c, library = examples()
        self.assertEqual(eligible_middles(u, a, c, library), ['sun_lit', 'singleton_fit'])

    def test_missing_candidate_is_not_impossibility(self):
        u, a, c, library = examples()
        self.assertEqual(eligible_middles(u, a, c, {'empty': set()}), [])
        self.assertTrue(verify_middle(u, a, library['sun_lit'], c)['certificate'])

    def test_social_talking_does_not_entail_borrowing(self):
        r = verify_middle({'visitor'}, {'visitor'}, set(), {'visitor'})
        self.assertTrue(r['conclusion'])
        self.assertFalse(r['minor_premise'])

    def test_common_enemy_does_not_entail_friendship(self):
        common_enemy, friends = {'pair'}, set()
        self.assertFalse(common_enemy <= friends)

    def test_subsets_complete(self):
        self.assertEqual(len(set(subsets({0, 1, 2}))), 8)
        self.assertIn(frozenset(), subsets({0}))

    def test_all_triples_three_objects(self):
        self.assertEqual(exhaustive_counts(), {'universe_size': 3, 'triples': 512,
                         'certificates': 37, 'soundness_failures': 0})

    def test_model_change_breaks_major(self):
        before = verify_middle({1}, {1}, {1}, {1})
        after = verify_middle({1, 2}, {1}, {1, 2}, {1})
        self.assertTrue(before['certificate'])
        self.assertFalse(after['certificate'])


if __name__ == '__main__':
    unittest.main()
