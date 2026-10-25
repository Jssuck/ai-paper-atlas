"""Tests of the explicitly defined finite models, not of Aristotle's entire theory."""
import unittest
from dataclasses import replace
from itertools import product
from model import World, Judgment, conflicts, modal_profile, exhaustive_summary, demonstration

class ModelTests(unittest.TestCase):
    def test_barbara_all_4096_two_world_models(self):
        r = exhaustive_summary()
        self.assertEqual(r['paired_models'], 4096)
        self.assertEqual(r['necessary_premise_models'], 256)
        self.assertEqual(r['necessary_premise_failures'], 0)
        self.assertEqual(r['actual_premise_models'], 1024)
        self.assertGreater(r['actual_premise_nonnecessary_conclusion'], 0)

    def test_boolean_modal_profiles_exhaustive(self):
        # 2+4+8+16 truth vectors; each valid actual-world choice.
        checked = 0
        for n in range(1, 5):
            for v in product((False, True), repeat=n):
                for actual in range(n):
                    r = modal_profile(v, actual)
                    self.assertEqual(r['actual'], v[actual])
                    self.assertEqual(r['necessary_in_model'], all(v))
                    self.assertEqual(r['can_be_false_in_model'], any(not t for t in v))
                    if r['necessary_in_model']:
                        self.assertTrue(r['actual'])
                    checked += 1
        self.assertEqual(checked, 98)

    def test_reject_empty_context_and_bad_indices(self):
        for truths, actual in [((), 0), ((True,), -1), ((True,), 1)]:
            with self.assertRaises(ValueError): modal_profile(truths, actual)
        with self.assertRaises(TypeError): modal_profile([1])

    def test_actual_true_not_necessary_countermodel(self):
        self.assertEqual(modal_profile([True, False]), {'actual': True, 'necessary_in_model': False, 'can_be_false_in_model': True})

    def test_world_vacuity_is_explicit(self):
        # Universal inclusion allows empty subjects; no existential conclusion.
        self.assertTrue(World(frozenset(), frozenset(), frozenset()).premises())

    def test_conflict_only_in_same_context(self):
        j = Judgment('a', 't', 'r', 'object', 'p', 'necessary')
        opposite = replace(j, mode='can_be_otherwise')
        self.assertEqual(conflicts([j, opposite]), [j.key()])
        for field in ('agent', 'time', 'respect', 'object_id', 'proposition'):
            self.assertEqual(conflicts([j, replace(opposite, **{field: 'different'})]), [])
        self.assertEqual(conflicts([j, j]), [])

    def test_all_mode_pairs_with_context_variations(self):
        # All 9 pairs in each of 6 contexts (same; each key-field changed).
        for left, right in product(('necessary', 'can_be_otherwise', 'uncommitted'), repeat=2):
            j = Judgment('a', 't', 'r', 'o', 'p', left)
            k = replace(j, mode=right)
            self.assertEqual(bool(conflicts([j, k])), {left, right} == {'necessary', 'can_be_otherwise'})
            for field in ('agent', 'time', 'respect', 'object_id', 'proposition'):
                self.assertFalse(conflicts([j, replace(k, **{field: 'other'})]))

    def test_same_object_not_same_proposition(self):
        j = Judgment('a', 't', 'r', 'diagonal', 'commensurable', 'necessary')
        k = replace(j, proposition='not commensurable')
        self.assertEqual(j.object_id, k.object_id)
        self.assertNotEqual(j.proposition, k.proposition)
        # This is identity bookkeeping, not a full logical negation checker.
        self.assertFalse(conflicts([j, k]))

    def test_reason_chain_does_not_determine_mode(self):
        r = demonstration()
        self.assertTrue(r['shared_reason_trace'])
        self.assertTrue(r['empty_reason_is_not_required_for_opinion'])
        self.assertEqual(r['different_agents_conflicts'], 0)
        self.assertEqual(r['same_agent_conflicts'], 1)

    def test_false_necessity_claim_is_representable(self):
        j = Judgment('a', 't', 'r', 'o', 'p', 'necessary')
        self.assertFalse(modal_profile([True, False])['necessary_in_model'])
        self.assertEqual(j.mode, 'necessary')  # Does not turn it into knowledge.

    def test_uncommitted_is_not_opinion(self):
        j = Judgment('a', 't', 'r', 'o', 'p', 'uncommitted')
        self.assertFalse(conflicts([j, replace(j, mode='necessary')]))
        self.assertFalse(conflicts([]))

    def test_necessary_truth_misapprehended(self):
        r = demonstration()['necessary_truth_can_be_misapprehended']
        self.assertTrue(r['truth_profile']['necessary_in_model'])
        self.assertEqual(r['asserted_mode'], 'can_be_otherwise')

    def test_unknown_mode_rejected(self):
        with self.assertRaises(ValueError): Judgment('a', 't', 'r', 'o', 'p', 'omniscient')

if __name__ == '__main__': unittest.main(verbosity=2)
