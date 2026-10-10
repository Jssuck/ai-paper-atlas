"""Exact examples, invalid inputs, boundaries, and exhaustive finite checks."""
import unittest
from itertools import product
from logic import (And, Atom, BOTTOM, Formula, Frame, Imp, Model, Not, Or,
                   class_case, formula_suite, implication, labeled_preorders,
                   powerset, truth_table, two_world_model)
from oracle import denotation, exhaustive_small_frames
from run_examples import finite_classes, results


class LogicTests(unittest.TestCase):
    def test_classical_four_rows(self):
        rows = truth_table()
        self.assertEqual([(r['p'], r['q']) for r in rows],
                         [(False, False), (False, True), (True, False), (True, True)])
        self.assertEqual([r['p_implies_q'] for r in rows], [True, True, False, True])
        self.assertEqual([r['not_q_implies_not_p'] for r in rows],
                         [True, True, False, True])

    def test_converse_is_different(self):
        self.assertTrue(implication(False, True))
        self.assertFalse(implication(True, False))
        r = class_case({0, 1}, {0}, {0, 1})
        self.assertTrue(r['all_A_are_B'])
        self.assertFalse(r['converse_all_B_are_A'])

    def test_boolean_input_validation(self):
        for bad in (0, 1, None, 'true', []):
            with self.assertRaises(ValueError):
                implication(bad, True)
            with self.assertRaises(ValueError):
                implication(False, bad)

    def test_empty_domain_and_empty_classes(self):
        for u, a, b in [(set(), set(), set()), ({0}, set(), set()),
                        ({0}, set(), {0}), ({0}, {0}, {0})]:
            r = class_case(u, a, b)
            self.assertTrue(r['all_A_are_B'])
            self.assertTrue(r['all_not_B_are_not_A'])
            self.assertEqual(r['positive_counterexamples'], frozenset())
        self.assertFalse(class_case({0}, {0}, set())['all_A_are_B'])

    def test_shared_counterexample_identity(self):
        r = class_case({0, 1, 2}, {0, 1}, {1, 2})
        self.assertEqual(r['positive_counterexamples'], frozenset({0}))
        self.assertEqual(r['contrapositive_counterexamples'], frozenset({0}))
        self.assertFalse(r['all_A_are_B'])
        self.assertFalse(r['all_not_B_are_not_A'])

    def test_common_domain_validation(self):
        for a, b in [({1}, set()), (set(), {1})]:
            with self.assertRaises(ValueError):
                class_case({0}, a, b)

    def test_all_5461_class_pairs(self):
        r = finite_classes()
        self.assertEqual(r['total_class_pairs'], 5461)
        self.assertEqual(r['mismatches'], 0)
        self.assertEqual([x['both_true'] for x in r['by_size']],
                         [1, 3, 9, 27, 81, 243, 729])
        self.assertEqual([x['class_pairs'] for x in r['by_size']],
                         [1, 4, 16, 64, 256, 1024, 4096])

    def test_formula_validation(self):
        for make in [lambda: Atom(''), lambda: Formula('xor'),
                     lambda: Formula('and', (Atom('p'),)),
                     lambda: Formula('bottom', name='p'),
                     lambda: Formula('imp', [Atom('p'), Atom('q')])]:
            with self.assertRaises(ValueError):
                make()

    def test_reflexivity_required(self):
        with self.assertRaisesRegex(ValueError, 'reflexive'):
            Frame(2, frozenset({(0, 1)}))

    def test_transitivity_required(self):
        with self.assertRaisesRegex(ValueError, 'transitive'):
            Frame(3, frozenset({(0, 0), (1, 1), (2, 2), (0, 1), (1, 2)}))

    def test_frame_world_validation(self):
        for n, relation in [(0, set()), (True, {(0, 0)}),
                            (1, {(0, 0), (0, 1)}), (1, {(0, 0), (-1, 0)})]:
            with self.assertRaises(ValueError):
                Frame(n, relation)
        with self.assertRaises(ValueError):
            two_world_model().frame.future(2)

    def test_persistence_required(self):
        frame = two_world_model().frame
        with self.assertRaisesRegex(ValueError, 'persistent'):
            Model.from_mapping(frame, {'p': {0}, 'q': set()})
        with self.assertRaisesRegex(ValueError, 'persistent'):
            Model.from_mapping(frame, {'p': {2}})

    def test_missing_and_duplicate_atoms_rejected(self):
        frame = Frame(1, {(0, 0)})
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            Model(frame, (('p', set()), ('p', {0})))
        model = Model.from_mapping(frame, {'p': set()})
        # Unknown q must not be hidden by the false antecedent.
        with self.assertRaisesRegex(ValueError, 'missing'):
            model.force(0, Imp(Atom('p'), Atom('q')))
        with self.assertRaises(ValueError):
            model.force(8, BOTTOM)

    def test_root_countermodel(self):
        m, f = two_world_model(), formula_suite()
        self.assertTrue(m.force(0, f['not_q_implies_not_p']))
        self.assertFalse(m.force(0, f['p_implies_q']))
        self.assertFalse(m.force(0, f['reverse_contraposition']))
        self.assertTrue(m.force(0, f['forward_contraposition']))
        self.assertTrue(m.force(1, f['p_implies_q']))

    def test_not_forced_is_not_negation(self):
        m, q = two_world_model(), Atom('q')
        self.assertFalse(m.force(0, q))
        self.assertFalse(m.force(0, Not(q)))
        self.assertTrue(m.force(0, Not(Not(q))))
        direct = Imp(Atom('p'), q)
        self.assertFalse(m.force(0, direct))
        self.assertFalse(m.force(0, Not(direct)))

    def test_future_worlds_are_checked(self):
        frame = two_world_model().frame
        m = Model.from_mapping(frame, {'p': {1}, 'q': set()})
        self.assertFalse(m.force(0, Imp(Atom('p'), Atom('q'))))
        self.assertFalse(m.force(0, Not(Atom('p'))))

    def test_current_world_is_checked(self):
        m = Model.from_mapping(Frame(1, {(0, 0)}), {'p': {0}, 'q': set()})
        self.assertFalse(m.force(0, Imp(Atom('p'), Atom('q'))))
        self.assertFalse(m.force(0, Not(Atom('p'))))

    def test_branching_checks_every_successor(self):
        frame = Frame(3, {(0, 0), (1, 1), (2, 2), (0, 1), (0, 2)})
        m = Model.from_mapping(frame, {'p': {1, 2}, 'q': {1}})
        self.assertFalse(m.force(0, Imp(Atom('p'), Atom('q'))))
        self.assertTrue(m.force(1, Imp(Atom('p'), Atom('q'))))
        self.assertFalse(m.force(2, Imp(Atom('p'), Atom('q'))))

    def test_cyclic_preorder_and_immutability(self):
        relation = set(product(range(2), repeat=2))
        frame = Frame(2, relation)
        p_worlds = {0, 1}
        m = Model.from_mapping(frame, {'p': p_worlds, 'q': set()})
        relation.clear()
        p_worlds.clear()
        self.assertEqual(len(m.frame.relation), 4)
        self.assertTrue(m.force(0, Atom('p')))
        with self.assertRaises(ValueError):
            Model.from_mapping(frame, {'p': {0}})

    def test_nested_connectives(self):
        m, p, q = two_world_model(), Atom('p'), Atom('q')
        self.assertFalse(m.force(0, And(p, q)))
        self.assertTrue(m.force(0, Or(p, q)))
        self.assertTrue(m.force(1, And(p, q)))
        self.assertFalse(m.force(0, Or(q, Not(q))))
        self.assertTrue(m.force(0, Imp(And(p, q), q)))

    def test_single_world_matches_classical(self):
        for p, q in product((False, True), repeat=2):
            m = Model.from_mapping(Frame(1, {(0, 0)}),
                                   {'p': {0} if p else set(), 'q': {0} if q else set()})
            self.assertEqual(m.force(0, Imp(Atom('p'), Atom('q'))), implication(p, q))
            self.assertEqual(m.force(0, Not(Atom('q'))), not q)

    def test_oracle_countermodel_denotations(self):
        m, f = two_world_model(), formula_suite()
        self.assertEqual(denotation(m, f['p_implies_q']), frozenset({1}))
        self.assertEqual(denotation(m, f['not_q_implies_not_p']), frozenset({0, 1}))
        self.assertEqual(denotation(m, f['not_q']), frozenset())
        self.assertEqual(denotation(m, f['not_of_p_implies_q']), frozenset())

    def test_exhaustive_preorders_and_oracle(self):
        r = exhaustive_small_frames()
        self.assertEqual([x['frames'] for x in r['by_size']], [1, 4, 29])
        self.assertEqual([x['models'] for x in r['by_size']], [4, 38, 632])
        self.assertEqual([x['reverse_counterexamples'] for x in r['by_size']], [0, 2, 90])
        self.assertEqual(r['totals'], {
            'frames': 34, 'models': 674, 'world_evaluations': 1976,
            'formula_world_comparisons': 49400, 'forward_counterexamples': 0,
            'reverse_counterexamples': 92, 'persistence_violations': 0})
        self.assertEqual(len({f.relation for f in labeled_preorders(3)}), 29)
        for bad in (0, 4, True):
            with self.assertRaises(ValueError):
                exhaustive_small_frames(bad)

    def test_powerset_and_determinism(self):
        self.assertEqual(list(powerset([])), [frozenset()])
        self.assertEqual(len(set(powerset(range(3)))), 8)
        self.assertEqual(results(), results())


if __name__ == '__main__':
    unittest.main()
