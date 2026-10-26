import unittest
from dataclasses import replace
from model import Middle, Problem, Proposition, Chain, classify, examples, shares_genus

class ClassificationTests(unittest.TestCase):
    def setUp(self):
        self.p, self.q, self.h, self.homonym, self.chain = examples()
    def test_shared_middle(self):
        self.assertEqual(classify(self.p, self.q), 'exact')
    def test_exact_also_generic(self):
        self.assertTrue(shares_genus(self.p, self.q))
    def test_three_generic_pairs(self):
        for i in range(3):
            for j in range(i+1, 3):
                with self.subTest(i=i, j=j):
                    self.assertEqual(classify(self.h[i], self.h[j]), 'generic')
    def test_homonym_does_not_merge(self):
        self.assertEqual(self.h[0].middle.label, self.homonym.middle.label)
        self.assertEqual(classify(self.h[0], self.homonym), 'unrelated')
    def test_domain_guard(self):
        with self.assertRaisesRegex(ValueError, 'domain'):
            classify(replace(self.p, domain='unlicensed'), self.q)
    def test_condition_guard(self):
        with self.assertRaisesRegex(ValueError, 'condition'):
            classify(replace(self.p, available_conditions=frozenset()), self.q)
    def test_identity_conflict_guard(self):
        bad = replace(self.q, middle=replace(self.q.middle, species='different'))
        with self.assertRaisesRegex(ValueError, 'conflicting'):
            classify(self.p, bad)
    def test_empty_identity_guard(self):
        with self.assertRaisesRegex(ValueError, 'empty'):
            classify(replace(self.p, key=''), self.q)
    def test_symmetry(self):
        all_problems = [self.p, self.q, *self.h, self.homonym]
        for a in all_problems:
            for b in all_problems:
                self.assertEqual(classify(a,b), classify(b,a))
    def test_generic_not_exact(self):
        self.assertNotEqual(self.h[0].middle.key, self.h[1].middle.key)
        self.assertNotEqual(classify(self.h[0], self.h[1]), 'exact')

class DependencyTests(unittest.TestCase):
    def setUp(self):
        self.chain = examples()[-1]
    def test_direct(self):
        self.assertTrue(self.chain.explains('moon', 'weather'))
    def test_composed(self):
        self.assertTrue(self.chain.explains('moon', 'nile'))
    def test_reverse_is_not_inferred(self):
        self.assertFalse(self.chain.explains('nile', 'moon'))
    def test_no_self_explanation(self):
        self.assertFalse(self.chain.explains('moon', 'moon'))
    def test_cycle_guard(self):
        with self.assertRaisesRegex(ValueError, 'cycle'):
            Chain(self.chain.nodes.values(), [*self.chain.edges, ('nile','moon')])
    def test_wrong_direction_guard(self):
        with self.assertRaisesRegex(ValueError, 'direction'):
            Chain(self.chain.nodes.values(), [('nile','weather')])
    def test_unknown_node_guard(self):
        with self.assertRaisesRegex(ValueError, 'unknown'):
            Chain(self.chain.nodes.values(), [('unknown','nile')])
    def test_unknown_query_guard(self):
        with self.assertRaisesRegex(ValueError, 'unknown'):
            self.chain.explains('unknown','nile')
    def test_duplicate_identity_guard(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            Chain([Proposition('a','one',0), Proposition('a','two',1)], [])
    def test_disconnected(self):
        chain = Chain([Proposition('a','one',0), Proposition('b','two',1)], [])
        self.assertFalse(chain.explains('a','b'))

if __name__ == '__main__':
    unittest.main()
