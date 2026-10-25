"""Independent bitmask and truth-table oracles; assertions survive -O and -OO."""
import unittest
from itertools import product, combinations
from model import nonempty_subsets, syllogism_counts, closure, minimal_supports, successor_prefix, report


def truth_models(atoms, facts, rules):
    """Semantic oracle: enumerate assignments, without forward chaining."""
    answer = []
    for bits in product([False, True], repeat=len(atoms)):
        val = dict(zip(atoms, bits))
        if all(val[f] for f in facts) and all(not all(val[b] for b in body) or val[head]
                                            for body, head in rules):
            answer.append(val)
    return answer


class TeachingTests(unittest.TestCase):
    def test_syllogisms_independent_bitmask_oracle(self):
        # 1 + 27 + 343 + 3375 = 3746 triples, no empty term extensions.
        total = 0
        for n in range(1, 5):
            expected = dict.fromkeys(syllogism_counts(n), 0)
            for a, b, c in product(range(1, 1 << n), repeat=3):
                p, q, r = (a & b) == b, (b & c) == c, (a & c) == c
                expected['triples'] += 1
                expected['both_premises_true'] += p and q
                expected['false_conclusions'] += not r
                expected['true_conclusion_both_premises_false'] += r and not p and not q
                expected['validity_violations'] += p and q and not r
                if not r:
                    self.assertFalse(p and q)
            self.assertEqual(syllogism_counts(n), expected)
            self.assertEqual(expected['validity_violations'], 0)
            total += expected['triples']
        self.assertEqual(total, 3746)

    def test_two_false_premises(self):
        a, b, c = {0}, {1}, {0}
        self.assertFalse(b <= a)
        self.assertFalse(c <= b)
        self.assertTrue(c <= a)
        self.assertGreater(syllogism_counts(2)['true_conclusion_both_premises_false'], 0)

    def test_horn_all_directed_graphs_truth_table(self):
        # 64 rule graphs * 8 fact sets = 512 independent semantic comparisons.
        atoms = ['a', 'b', 'c']
        edges = [(frozenset([x]), y) for x in atoms for y in atoms if x != y]
        count = 0
        for mask in range(1 << len(edges)):
            rules = [e for i, e in enumerate(edges) if mask & (1 << i)]
            for bits in product([False, True], repeat=3):
                facts = {x for x, v in zip(atoms, bits) if v}
                models = truth_models(atoms, facts, rules)
                self.assertTrue(models)  # all-true assignment always exists
                entailed = frozenset(x for x in atoms if all(m[x] for m in models))
                self.assertEqual(closure(facts, rules), entailed)
                count += 1
        self.assertEqual(count, 512)

    def test_conjunctive_and_empty_rule_bodies(self):
        rules = [(frozenset(), 'a'), (frozenset(['a', 'b']), 'c')]
        self.assertEqual(closure([], rules), frozenset(['a']))
        self.assertEqual(closure(['b'], rules), frozenset(['a', 'b', 'c']))
        self.assertEqual(minimal_supports(['a', 'b'], rules, 'a'), [frozenset()])

    def test_minimal_supports_independent_semantics(self):
        atoms = ['a', 'b', 'c', 'd']
        rules = [(frozenset(['a']), 'c'), (frozenset(['b']), 'c'),
                 (frozenset(['c']), 'd')]
        facts = ['a', 'b', 'c']
        expected = []
        allsets = [frozenset(s) for k in range(4) for s in combinations(facts, k)]
        sufficient = [s for s in allsets if all(v['d'] for v in truth_models(atoms, s, rules))]
        expected = [s for s in sufficient if not any(t < s for t in sufficient)]
        self.assertEqual(set(minimal_supports(facts, rules, 'd')), set(expected))
        self.assertEqual(set(expected), {frozenset(['a']), frozenset(['b']), frozenset(['c'])})
        self.assertEqual(minimal_supports(facts, [], 'missing'), [])

    def test_shared_rules_not_shared_facts_and_explicit_bridge(self):
        r = report()
        self.assertEqual(r['rules_alone'], [])
        self.assertEqual(r['geometry_facts_only'], ['geom:p', 'geom:q'])
        self.assertEqual(r['supports']['geom:q'], [['geom:p']])
        self.assertEqual(r['supports']['arith:s'], [['arith:r']])
        self.assertIn('arith:s', r['with_explicit_bridge'])
        self.assertEqual(r['bridge_alternative_supports'], [['arith:r'], ['geom:p']])

    def test_successor_prefix_and_bounds(self):
        for depth in range(26):
            terms = successor_prefix(depth)
            self.assertEqual(len(terms), depth + 1)
            self.assertEqual(len(set(terms)), depth + 1)
            self.assertEqual([t.count('S') for t in terms], list(range(depth + 1)))
        for invalid in [-1, 101, 1.5, True]:
            with self.assertRaises(ValueError): successor_prefix(invalid)
        for invalid in [0, 7, 1.5, True]:
            with self.assertRaises(ValueError): nonempty_subsets(invalid)


if __name__ == '__main__':
    unittest.main(verbosity=2)
