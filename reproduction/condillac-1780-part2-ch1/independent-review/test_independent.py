"""Independent boundary tests. No author test/helper/oracle is imported."""
import json
import os
from pathlib import Path
import sys
import unittest
from dataclasses import FrozenInstanceError
from unittest.mock import patch

MODEL_DIR = Path(os.environ.get('AUDIT_MODEL_DIR', Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(MODEL_DIR))
from model import FixedPoint, HornSystem, Rule, filter_evidence


class BoundaryTests(unittest.TestCase):
    def test_01_evidence_trace_and_default(self):
        self.assertEqual(filter_evidence(['p', 'q'], [['p'], [], ['p']]),
                         (frozenset({'p', 'q'}), frozenset({'p'}), frozenset(), frozenset()))
        self.assertEqual(filter_evidence(['p'], []), (frozenset({'p'}),))
        self.assertEqual(filter_evidence(['p'], [], []), (frozenset(),))

    def test_02_evidence_generators_and_snapshot(self):
        H, C, E = ['p', 'p', 'q'], {'q'}, {'p', 'q'}
        out = filter_evidence(iter(H), (x for x in [E]), iter(C))
        H.clear(); C.clear(); E.clear()
        self.assertEqual(out, (frozenset({'q'}), frozenset({'q'})))
        self.assertIs(type(out), tuple)
        self.assertTrue(all(type(x) is frozenset for x in out))

    def test_03_late_evidence_validation(self):
        def observations():
            yield []
            yield ['foreign']
        with self.assertRaises(ValueError):
            filter_evidence(['p'], observations())

    def test_04_bare_strings_rejected(self):
        cases = [('pq', []), (['p'], 'p'), (['p'], ['p']), (['p'], [], 'p')]
        for args in cases:
            with self.subTest(args=args), self.assertRaises(TypeError):
                filter_evidence(*args)
        for value in ('p', b'p'):
            with self.assertRaises(TypeError):
                Rule(value, 'p')
            with self.assertRaises(TypeError):
                HornSystem(value, [])

    def test_05_invalid_evidence_labels(self):
        for value in ('', None, 3, b'p'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                filter_evidence([value], [])
        with self.assertRaises(TypeError):
            filter_evidence([[]], [])

    def test_06_foreign_input_labels(self):
        with self.assertRaises(ValueError):
            filter_evidence(['p'], [], ['foreign'])
        with self.assertRaises(ValueError):
            filter_evidence(['p'], [['foreign']])

    def test_07_empty_rule_bodies_rejected(self):
        for body in ([], (), frozenset(), iter(())):
            with self.assertRaises(ValueError):
                Rule(body, 'p')

    def test_08_invalid_rule_labels(self):
        for body, head in (([''], 'p'), ([None], 'p'), (['p'], ''), (['p'], 0)):
            with self.subTest(body=body, head=head), self.assertRaises(ValueError):
                Rule(body, head)

    def test_09_rule_membership_and_types(self):
        for rule in (Rule(['q'], 'p'), Rule(['p'], 'q')):
            with self.assertRaises(ValueError):
                HornSystem(['p'], [rule])
        with self.assertRaises(TypeError):
            HornSystem(['p'], [('p', 'p')])

    def test_10_frozen_and_copied_data(self):
        body, claims = {'p'}, {'p', 'q'}
        rule = Rule(body, 'q'); rules = [rule]
        system = HornSystem(claims, rules)
        result = system.fixed_point('least', ['p'])
        body.clear(); claims.clear(); rules.clear()
        self.assertEqual(rule.body, {'p'})
        self.assertEqual(system.claims, {'p', 'q'})
        self.assertEqual(system.rules, (rule,))
        manual_state = {'p'}
        manual_states = [manual_state]
        manual = FixedPoint('least', manual_states)
        manual_state.clear(); manual_states.clear()
        self.assertEqual(manual.states, (frozenset({'p'}),))
        self.assertIs(type(manual.states), tuple)
        for kind, states in (('invalid', [set()]), ('least', []), ('least', [{' '} , {''}])):
            with self.assertRaises(ValueError):
                FixedPoint(kind, states)
        for states in ('p', ['p']):
            with self.assertRaises(TypeError):
                FixedPoint('least', states)
        self.assertIs(type(result.states), tuple)
        self.assertTrue(all(type(s) is frozenset for s in result.states))
        for item, field, value in ((rule, 'head', 'p'), (system, 'claims', frozenset()),
                                   (result, 'states', ())):
            with self.assertRaises(FrozenInstanceError):
                setattr(item, field, value)

    def test_11_empty_universes(self):
        self.assertEqual(filter_evidence([], [[], []]), (frozenset(),) * 3)
        s = HornSystem([], [])
        for kind in ('least', 'greatest'):
            self.assertEqual(s.fixed_point(kind).states, (frozenset(),))
        self.assertEqual(s.immediate([]), frozenset())

    def test_12_least_chain_exact(self):
        s = HornSystem('p q r'.split(), [Rule(['p'], 'q'), Rule(['q'], 'r')])
        p = s.fixed_point('least', ['p'])
        self.assertEqual(p.states, (frozenset(), frozenset({'p'}),
                                   frozenset({'p', 'q'}), frozenset({'p', 'q', 'r'})))
        self.assertEqual(p.kind, 'least'); self.assertEqual(p.changes, 3)

    def test_13_greatest_chain_exact(self):
        s = HornSystem('p q r'.split(), [Rule(['p'], 'q'), Rule(['q'], 'r')])
        p = s.fixed_point('greatest')
        self.assertEqual(p.states, (frozenset({'p', 'q', 'r'}), frozenset({'q', 'r'}),
                                   frozenset({'r'}), frozenset()))
        self.assertEqual(p.kind, 'greatest'); self.assertEqual(p.changes, 3)

    def test_14_cycle_and_anchor_removal(self):
        s = HornSystem(['p', 'q'], [Rule(['p'], 'q'), Rule(['q'], 'p')])
        self.assertEqual(s.fixed_point('least').result, set())
        self.assertEqual(s.fixed_point('greatest').result, {'p', 'q'})
        self.assertEqual(s.fixed_point('least', ['p']).result, {'p', 'q'})
        self.assertEqual(s.fixed_point('least').result, set())
        self.assertEqual(s.immediate(['p', 'q']), {'p', 'q'})
        self.assertEqual(s.fixed_point('greatest', withdrawn=['p']).result, set())

    def test_15_arbitrary_start_can_oscillate(self):
        s = HornSystem(['p', 'q'], [Rule(['p'], 'q'), Rule(['q'], 'p')])
        sequence = [frozenset({'p'})]
        for _ in range(4):
            sequence.append(s.immediate(sequence[-1]))
        self.assertEqual(sequence, [frozenset({'p'}), frozenset({'q'}),
                                   frozenset({'p'}), frozenset({'q'}), frozenset({'p'})])

    def test_16_withdrawal_priority_and_premises(self):
        s = HornSystem(['p', 'q', 'r'], [Rule(['p'], 'q'), Rule(['q'], 'r')])
        self.assertEqual(s.immediate(['p'], ['p', 'q'], ['q']), {'p'})
        self.assertEqual(s.fixed_point('least', ['p', 'q'], ['q']).result, {'p'})
        self.assertEqual(s.fixed_point('greatest', ['p', 'q'], ['q']).result, {'p'})
        with self.assertRaises(ValueError):
            s.immediate(['q'], withdrawn=['q'])

    def test_17_conjunction_and_alternatives(self):
        both = HornSystem(['p', 'q', 'r'], [Rule(['p', 'q'], 'r')])
        either = HornSystem(['p', 'q', 'r'], [Rule(['p'], 'r'), Rule(['q'], 'r')])
        self.assertEqual(both.immediate(['p']), set())
        self.assertEqual(both.immediate(['p', 'q']), {'r'})
        self.assertEqual(either.immediate(['p']), {'r'})
        self.assertEqual(either.immediate(['q']), {'r'})

    def test_18_graph_cycle_insufficient_for_conjunction(self):
        s = HornSystem(['p', 'q'], [Rule(['p', 'q'], 'p')])
        self.assertEqual(s.fixed_point('greatest').states,
                         (frozenset({'p', 'q'}), frozenset({'p'}), frozenset()))

    def test_19_alternative_anchor_survives(self):
        s = HornSystem(['p', 'q', 'r'], [Rule(['p'], 'q'), Rule(['q'], 'p'), Rule(['r'], 'q')])
        for kind in ('least', 'greatest'):
            self.assertEqual(s.fixed_point(kind, ['r'], ['p']).result, {'q', 'r'})

    def test_20_duplicate_and_order_invariance(self):
        rules = [Rule(['p'], 'q'), Rule(['q'], 'r')]
        a = HornSystem(['p', 'q', 'r'], rules)
        b = HornSystem(['p', 'q', 'r'], rules[::-1] + rules)
        for kind in ('least', 'greatest'):
            self.assertEqual(a.fixed_point(kind, ['p']), b.fixed_point(kind, ['p']))
        self.assertEqual(filter_evidence(['p', 'q'], [['q'], ['p', 'q'], ['q']])[-1], {'q'})

    def test_21_context_and_kind_validation(self):
        s = HornSystem(['p'], [])
        for context in ({'anchors': ['q']}, {'withdrawn': ['q']}):
            with self.assertRaises(ValueError):
                s.fixed_point('least', **context)
            with self.assertRaises(ValueError):
                s.immediate([], **context)
        for kind in ('Least', '', None, 0):
            with self.assertRaises(ValueError):
                s.fixed_point(kind)
        with self.assertRaises(ValueError):
            s.immediate(['q'])
        for context in ({'anchors': 'p'}, {'withdrawn': 'p'}):
            with self.assertRaises(TypeError):
                s.fixed_point('least', **context)

    def test_22_operator_evaluation_bound_is_tight(self):
        s = HornSystem(['p', 'q', 'r'], [Rule(['p'], 'q'), Rule(['q'], 'r')])
        original = HornSystem._step
        calls = []
        def counted(system, state, anchors, withdrawn):
            calls.append(state)
            return original(system, state, anchors, withdrawn)
        for kind, anchors in (('least', ['p']), ('greatest', [])):
            calls.clear()
            with patch.object(HornSystem, '_step', counted):
                point = s.fixed_point(kind, anchors)
            self.assertEqual(len(calls), 4)
            self.assertEqual(point.changes, 3)
            self.assertEqual(len(point.states), 4)


def run():
    class TrackingResult(unittest.TextTestResult):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw); self.started = []; self.completed = []
        def startTest(self, test):
            self.started.append(test.id().split('.')[-1]); super().startTest(test)
        def stopTest(self, test):
            self.completed.append(test.id().split('.')[-1]); super().stopTest(test)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BoundaryTests)
    if '--empty' in sys.argv:
        suite = unittest.TestSuite()
    result = unittest.TextTestRunner(verbosity=2, resultclass=TrackingResult).run(suite)
    record = {'tests': result.testsRun, 'started': result.started, 'completed': result.completed,
              'failures': len(result.failures), 'errors': len(result.errors),
              'skipped': len(result.skipped), 'expected_failures': len(result.expectedFailures),
              'unexpected_successes': len(result.unexpectedSuccesses), 'optimize': sys.flags.optimize}
    print('AUDIT_RESULT=' + json.dumps(record, sort_keys=True))
    if '--duplicate-marker' in sys.argv:
        print('AUDIT_RESULT=' + json.dumps(record, sort_keys=True))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run())
