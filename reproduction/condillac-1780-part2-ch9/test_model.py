"""Explicit unittest checks remain active under -O and -OO."""
import itertools
import unittest
from fractions import Fraction
import model as m
from examples import results


class ModelTests(unittest.TestCase):
    def test_certain_nonvacuous(self):
        self.assertFalse(m.certain((), {}))
        self.assertTrue(m.certain(('a',), {'a': True}))
        self.assertFalse(m.certain(('a',), {'a': False}))

    def test_observation_filter(self):
        h = ('a', 'b')
        t = {'x': {'a': 1, 'b': 0}}
        self.assertEqual(m.consistent(h, t, []), h)
        self.assertEqual(m.consistent(h, t, [('x', 1)]), ('a',))
        self.assertEqual(m.consistent(h, t, [('x', 2)]), ())
        self.assertEqual(m.consistent(h, t, [('x', 1), ('x', 0)]), ())
        self.assertEqual(m.consistent(h, t, [('x', 1), ('x', 1)]), ('a',))

    def test_contract_rejections(self):
        invalid = [(), ('a', 'a'), ('',), (1,)]
        for h in invalid:
            with self.subTest(h=h), self.assertRaises(ValueError):
                m.partition(h, {})
        for table in ({}, {'a': 1, 'extra': 0}, {'a': []}, {'a': float('nan')}, {'a': 0.5}):
            with self.subTest(table=table), self.assertRaises(ValueError):
                m.partition(('a',), table)
        for truth in (0, 1, None, 'yes'):
            with self.subTest(truth=truth), self.assertRaises(ValueError):
                m.certain(('a',), {'a': truth})
        with self.assertRaises(ValueError):
            m.consistent(('a',), {}, [('unknown', True)])

        with self.assertRaises(ValueError):
            m.consistent(('a',), {'x': {'a': 1}}, [('x', float('nan'))])

    def test_separating_edges(self):
        self.assertEqual(m.minimal_separating(('a',), {}), ())
        self.assertIsNone(m.minimal_separating(('a', 'b'), {}))
        self.assertIsNone(m.minimal_separating(('a', 'b'), {'same': {'a': 0, 'b': 0}}))
        self.assertEqual(m.minimal_separating(('a', 'b'), {'x': {'a': 0, 'b': 1}, 'y': {'a': 1, 'b': 0}}), ('x',))

    def test_exact_ambiguity(self):
        h = ('a', 'b', 'c')
        self.assertEqual(m.expected_ambiguity(h, dict.fromkeys(h, 0)), Fraction(3))
        self.assertEqual(m.expected_ambiguity(h, dict(zip(h, (0, 1, 2)))), Fraction(1))
        self.assertEqual(m.expected_ambiguity(h, dict(zip(h, (0, 0, 1)))), Fraction(5, 3))

    def test_bayes_edges(self):
        h = ('a', 'b')
        self.assertEqual(m.posterior(h, {'a': 1, 'b': 3}, {'a': 1, 'b': 1}), {'a': Fraction(1,4), 'b': Fraction(3,4)})
        for prior, likelihood in [({'a': 0, 'b': 0}, {'a': 1, 'b': 1}), ({'a': 1, 'b': 1}, {'a': 0, 'b': 0}), ({'a': 1, 'b': 0}, {'a': 0, 'b': 1})]:
            with self.subTest(prior=prior, likelihood=likelihood), self.assertRaises(ValueError):
                m.posterior(h, prior, likelihood)
        for value in (-1, 0.5, True, '1'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                m.posterior(('a',), {'a': value}, {'a': 1})
        with self.assertRaises(ValueError):
            m.posterior(('a',), {'a': 1}, {'a': 2})
        with self.assertRaises(ValueError):
            m.posterior(h, {'a': 1}, {'a': 1, 'b': 1})
        self.assertFalse(m.structural_certainty(h, {'a': 0, 'b': 0}, {'a': True, 'b': True}))

    def test_examples(self):
        r = results()
        for key in ('effect_implies_cause', 'similarity_guarantees_inhabitants', 'gold_unobserved_property_certain', 'empty_state_certain', 'zero_prior_structural_certainty'):
            self.assertIs(r[key], False)
        self.assertEqual(r['expected_survivors'], {'first_bit': '2', 'second_bit': '2', 'rare_11': '5/2'})
        self.assertEqual(r['minimal_separating_tests'], ['first_bit', 'second_bit'])
        self.assertEqual(r['positive_prior_posterior'], {'target': '3/4', 'alternative': '1/4'})

    def test_exhaustive_filter_properties_n4(self):
        h = ('a', 'b', 'c', 'd')
        tables = [dict(zip(h, bits)) for bits in itertools.product((False, True), repeat=4)]
        for a, b in itertools.product(tables, repeat=2):
            tests = {'a': a, 'b': b}
            initial = m.consistent(h, tests, [('a', True)])
            final = m.consistent(h, tests, [('a', True), ('b', True)])
            self.assertTrue(set(final) <= set(initial))
            self.assertEqual(final, m.consistent(h, tests, [('b', True), ('a', True)]))
            # Independent direct count, rather than implementation's cell formula.
            survivors = sum(sum(a[x] == a[y] for y in h) for x in h)
            self.assertEqual(m.expected_ambiguity(h, a), Fraction(survivors, 4))
            chosen = m.minimal_separating(h, tests)
            possible = all(any(t[x] != t[y] for t in tests.values()) for x, y in itertools.combinations(h, 2))
            self.assertEqual(chosen is not None, possible)

    def test_bayes_finite_properties(self):
        h = ('a', 'b')
        for pa, pb, la, lb in itertools.product(range(3), repeat=4):
            prior = {'a': pa, 'b': pb}
            likelihood = {'a': Fraction(la,2), 'b': Fraction(lb,2)}
            if pa * la + pb * lb == 0:
                continue
            p = m.posterior(h, prior, likelihood)
            self.assertEqual(sum(p.values()), 1)
            self.assertTrue(all(0 <= v <= 1 for v in p.values()))
            self.assertEqual(p, m.posterior(h, {'a': 7*pa, 'b': 7*pb}, likelihood))
            if pa > 0 and pb > 0:
                for qa, qb in itertools.product((False, True), repeat=2):
                    q = {'a': qa, 'b': qb}
                    self.assertEqual(sum(p[w] for w in h if q[w]) == 1, m.structural_certainty(h, likelihood, q))

if __name__ == '__main__':
    unittest.main(verbosity=2)
