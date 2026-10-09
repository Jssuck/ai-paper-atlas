import unittest
from simulator import (Action, Machine, run, alternating, alternating_spaced,
                       one_then_silent, delayed_forever, silent_forever,
                       enumerate_one_state)


class SimulatorTests(unittest.TestCase):
    def test_alternating_exact_trace(self):
        r = run(alternating(), 6)
        self.assertEqual(r['output'], '010101')
        self.assertEqual([(t['step'], t['state'], t['head'], t['output'])
                          for t in r['trace']],
                         [(0, 'a', 0, ''), (1, 'b', 1, '0'),
                          (2, 'a', 2, '01'), (3, 'b', 3, '010'),
                          (4, 'a', 4, '0101'), (5, 'b', 5, '01010'),
                          (6, 'a', 6, '010101')])
        self.assertEqual(r['trace'][-1]['tape'],
                         {str(i): str(i % 2) for i in range(6)})
        self.assertEqual(r['status'], 'cap_reached')

    def test_source_aligned_spacing(self):
        r = run(alternating_spaced(), 12)
        self.assertEqual(r['output'], '010101')
        self.assertEqual(r['trace'][-1]['tape'],
                         {str(2*i): str(i % 2) for i in range(6)})
        self.assertEqual([t['output'] for t in r['trace'][:5]],
                         ['', '0', '0', '01', '01'])

    def test_nonhalting_finite_output(self):
        r = run(one_then_silent(), 100)
        self.assertEqual((r['steps'], r['output'], r['status']),
                         (100, '0', 'cap_reached'))
        self.assertEqual(r['trace'][-1]['head'], 100)
        self.assertEqual(r['trace'][-1]['tape'], {'0': '0'})

    def test_delay_boundary(self):
        self.assertEqual(run(delayed_forever(20), 20)['output'], '')
        self.assertEqual(run(delayed_forever(20), 21)['output'], '0')
        self.assertEqual(run(delayed_forever(20), 24)['output'], '0000')

    def test_many_finite_delay_counterexamples(self):
        for cap in range(101):
            self.assertEqual(run(delayed_forever(cap), cap)['output'], '')
            self.assertEqual(run(delayed_forever(cap), cap+1)['output'], '0')

    def test_silent_output_observations_match_to_cap(self):
        # Only output histories are identical; control states differ.
        a = run(delayed_forever(20), 20)
        b = run(silent_forever(), 20)
        self.assertEqual([t['output'] for t in a['trace']],
                         [t['output'] for t in b['trace']])

    def test_missing_rule_halts_at_start(self):
        m = Machine({'q'}, {'_'}, 'q', {})
        self.assertEqual((run(m, 10)['steps'], run(m, 10)['status']), (0, 'halted'))

    def test_halt_exactly_at_cap(self):
        m = Machine({'q', 'h'}, {'_'}, 'q', {('q', '_'): Action('h', '_', 0)})
        self.assertEqual(run(m, 1)['status'], 'halted')

    def test_left_moves_negative_indices(self):
        m = Machine({'q'}, {'_', 'x'}, 'q', {('q', '_'): Action('q', 'x', -1)})
        self.assertEqual(run(m, 3)['trace'][-1]['head'], -3)
        self.assertEqual(run(m, 3)['trace'][-1]['tape'], {'-2': 'x', '-1': 'x', '0': 'x'})

    def test_erasure_and_stationary_move(self):
        m = Machine({'q', 'r', 'h'}, {'_', 'x'}, 'q', {
            ('q', '_'): Action('r', 'x', 0), ('r', 'x'): Action('h', '_', 0)})
        r = run(m, 10)
        self.assertEqual((r['steps'], r['status'], r['trace'][-1]['tape']),
                         (2, 'halted', {}))

    def test_reject_invalid_rules(self):
        for a in (Action('bad', '_', 0), Action('q', 'bad', 0),
                  Action('q', '_', 2), Action('q', '_', 0, '01')):
            with self.assertRaises(ValueError):
                Machine({'q'}, {'_'}, 'q', {('q', '_'): a})

    def test_reject_negative_cap_and_delay(self):
        with self.assertRaises(ValueError): run(alternating(), -1)
        with self.assertRaises(ValueError): delayed_forever(-1)

    def test_finite_enumeration_count_and_uniqueness(self):
        machines = list(enumerate_one_state())
        self.assertEqual(len(machines), 324)
        tables = {tuple(m.rules.items()) for m in machines}
        self.assertEqual(len(tables), 324)
        self.assertTrue(all(run(m, 20)['steps'] == 20 for m in machines))

    def test_run_does_not_mutate_table(self):
        m = alternating()
        before = dict(m.rules)
        self.assertEqual(run(m, 6), run(m, 6))
        self.assertEqual(before, m.rules)

    def test_trace_invariants(self):
        for m in [alternating(), alternating_spaced(), one_then_silent(),
                  delayed_forever(20), *enumerate_one_state()]:
            r = run(m, 25)
            for previous, current in zip(r['trace'], r['trace'][1:]):
                self.assertEqual(current['step'], previous['step'] + 1)
                self.assertLessEqual(abs(current['head'] - previous['head']), 1)
                self.assertEqual(current['output'], previous['output'] + current['emitted'])
                self.assertLessEqual(len(current['tape']), current['step'])
                self.assertNotIn('_', current['tape'].values())
                a = m.rules[(previous['state'], previous['scanned'])]
                self.assertEqual((current['state'], current['head'], current['emitted']),
                                 (a.state, previous['head'] + a.move, a.emit))


if __name__ == '__main__':
    unittest.main(verbosity=2)
