"""Tests exercise the stated finite/structural contract, not ancient causes."""
import unittest
from model import (ChainCertificate, validate, finite_middle_candidates,
                   nearest_choices, transitive_closure, enumerate_four_sets)


class ChainTests(unittest.TestCase):
    def setUp(self):
        self.chain = ChainCertificate(('D', 'C', 'B', 'A'))
        self.ext = {'D': {0}, 'C': {0, 1}, 'B': {0, 1, 2}, 'A': {0, 1, 2, 3}}
        self.edges = {('D', 'C'), ('C', 'B'), ('B', 'A')}

    def test_question_D_has_nearest_C(self):
        result = validate(self.chain, self.ext, self.edges)
        self.assertEqual(result['nearest_declared_reason'], 'C')
        self.assertTrue(result['finite_inclusion_holds'])
        self.assertFalse(result['certifies_real_explanation'])

    def test_question_C_has_nearest_B(self):
        self.assertEqual(validate(self.chain.suffix('C'), self.ext, self.edges)['nearest_declared_reason'], 'B')

    def test_question_B_has_endpoint_B_not_self_loop(self):
        result = validate(self.chain.suffix('B'), self.ext, self.edges)
        self.assertEqual(result['nearest_declared_reason'], 'B')
        self.assertEqual(result['internal_middles'], [])
        self.assertTrue(result['direct_endpoint_convention'])
        self.assertNotIn(('B', 'B'), self.edges)

    def test_both_internal_middles_are_extensionally_valid(self):
        self.assertEqual(finite_middle_candidates('D', 'A', self.ext, ('C', 'B')), ('C', 'B'))

    def test_missing_edge_cannot_be_replaced_by_semantic_truth(self):
        with self.assertRaisesRegex(ValueError, 'undeclared'):
            validate(self.chain, self.ext, self.edges - {('C', 'B')})

    def test_false_adjacent_inclusion_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'false finite'):
            validate(self.chain, dict(self.ext, C={1}), self.edges)

    def test_true_endpoint_does_not_repair_false_middle(self):
        ext = dict(self.ext, C={0, 4})
        self.assertLessEqual(ext['D'], ext['A'])
        with self.assertRaisesRegex(ValueError, 'false finite'):
            validate(self.chain, ext, self.edges)

    def test_reverse_direction_does_not_follow(self):
        reverse = ChainCertificate(('A', 'B', 'C', 'D'))
        with self.assertRaisesRegex(ValueError, 'false finite'):
            validate(reverse, self.ext, {(b, a) for a, b in self.edges})

    def test_acyclic_term_names_required(self):
        with self.assertRaises(ValueError):
            ChainCertificate(('D', 'C', 'D', 'A'))

    def test_reflexive_path_not_a_direct_premise(self):
        with self.assertRaises(ValueError):
            ChainCertificate(('B', 'B'))

    def test_target_only_not_an_explanation(self):
        with self.assertRaises(ValueError):
            ChainCertificate(('A',))

    def test_missing_named_extension_rejected(self):
        with self.assertRaisesRegex(ValueError, 'missing extension'):
            validate(self.chain, {k:v for k,v in self.ext.items() if k != 'C'}, self.edges)

    def test_sets_not_arbitrary_lists(self):
        with self.assertRaises(TypeError):
            validate(self.chain, dict(self.ext, D=[0]), self.edges)

    def test_empty_subject_is_vacuously_valid_not_observation(self):
        result = validate(self.chain, dict(self.ext, D=set()), self.edges)
        self.assertTrue(result['finite_inclusion_holds'])
        self.assertFalse(result['subject_nonempty'])

    def test_all_empty_not_real_explanation_certificate(self):
        result = validate(self.chain, {n:set() for n in 'ABCD'}, self.edges)
        self.assertFalse(result['certifies_real_explanation'])
        self.assertEqual(result['nearest_declared_reason'], 'C')

    def test_equal_extensions_leave_order_underdetermined(self):
        ext = {n:{0} for n in 'ABCD'}
        other = ChainCertificate(('D', 'B', 'C', 'A'))
        edges = self.edges | {('D', 'B'), ('B', 'C'), ('C', 'A')}
        self.assertEqual(validate(self.chain, ext, edges)['nearest_declared_reason'], 'C')
        self.assertEqual(validate(other, ext, edges)['nearest_declared_reason'], 'B')

    def test_closure_shortcut_is_not_declared_direct(self):
        closure = transitive_closure(self.edges)
        self.assertIn(('D', 'A'), closure)
        self.assertNotIn(('D', 'A'), self.edges)
        shortcut = ChainCertificate(('D', 'A'))
        with self.assertRaisesRegex(ValueError, 'undeclared'):
            validate(shortcut, self.ext, self.edges)
        # Mistakenly using closure as primitive edges produces a different
        # endpoint convention. The experiment demonstrates this input error.
        result = validate(shortcut, self.ext, closure)
        self.assertEqual(result['nearest_declared_reason'], 'D')
        self.assertFalse(result['certifies_real_explanation'])

    def test_branching_support_can_have_two_nearest_choices(self):
        other = ChainCertificate(('D', 'E', 'B', 'A'))
        validate(other, dict(self.ext, E={0, 1}), self.edges | {('D','E'),('E','B')})
        self.assertEqual(nearest_choices([self.chain, other], 'D', 'A'), {'C', 'E'})

    def test_same_first_step_deduplicates_but_not_causal_identity(self):
        shortcut = ChainCertificate(('D', 'C', 'A'))
        self.assertEqual(nearest_choices([self.chain, shortcut], 'D', 'A'), {'C'})

    def test_mixed_questions_rejected(self):
        with self.assertRaisesRegex(ValueError, 'mixed questions'):
            nearest_choices([self.chain, self.chain.suffix('C')], 'D', 'A')

    def test_no_supplied_support_is_empty_not_impossibility(self):
        self.assertEqual(nearest_choices([], 'D', 'A'), set())

    def test_enumeration_matches_independent_membership_count(self):
        result = enumerate_four_sets(3)
        self.assertEqual(result['assignments'], 16**3)
        self.assertEqual(result['chain_satisfying'], 5**3)
        self.assertEqual(result['nonempty_subject'], 5**3 - 4**3)
        self.assertEqual(result['transitivity_counterexamples'], 0)

    def test_empty_universe_has_one_vacuous_assignment(self):
        self.assertEqual(enumerate_four_sets(0), dict(universe_size=0, assignments=1,
            chain_satisfying=1, nonempty_subject=0, transitivity_counterexamples=0))

    def test_invalid_enumeration_size_rejected(self):
        for bad in (-1, 5, 1.5, True):
            with self.assertRaises(ValueError):
                enumerate_four_sets(bad)


if __name__ == '__main__':
    unittest.main(verbosity=2)
