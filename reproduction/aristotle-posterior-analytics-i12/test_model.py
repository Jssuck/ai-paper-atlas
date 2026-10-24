import unittest
from model import included, shared_attribute, same_middle, question_route, closure, enumerate_models


class ModelTests(unittest.TestCase):
    def test_shared_attribute_counterexample(self):
        self.assertTrue(shared_attribute(1, 2, 3))
        self.assertFalse(included(1, 2))

    def test_correct_chain(self):
        self.assertTrue(included(1, 3) and included(3, 7))
        self.assertTrue(included(1, 7))

    def test_reverse_counterexample_nonempty(self):
        self.assertTrue(included(1, 3))
        self.assertFalse(included(3, 1))

    def test_equivalence(self):
        self.assertTrue(included(3, 3))

    def test_empty_subject_is_explicit(self):
        self.assertTrue(included(0, 0))
        self.assertTrue(included(0, 7))
        self.assertFalse(included(1, 0))

    def test_invalid_masks(self):
        for x in (-1, 8, True, 1.2, '1'):
            with self.subTest(x=x), self.assertRaises(ValueError):
                included(x, 7)
        with self.assertRaises(ValueError):
            included(0, 0, 0)

    def test_ambiguous_middle(self):
        self.assertFalse(same_middle(('circle', 'geometric-circle'), ('circle', 'epic-cycle')))

    def test_synonym_ids(self):
        self.assertTrue(same_middle(('circle', 'circle'), ('圆', 'circle')))

    def test_invalid_term(self):
        for term in ('circle', ('circle',), ('circle', ''), ('circle', 3)):
            with self.subTest(term=term), self.assertRaises(ValueError):
                same_middle(term, ('circle', 'circle'))

    def test_domain_route(self):
        self.assertEqual(question_route('geometry', 'geometry', 'derived'), 'eligible-for-domain-explanation')
        self.assertEqual(question_route('geometry', 'music', 'derived'), 'outside-declared-scope')

    def test_bridge_direction(self):
        bridge = (('geometry', 'optics'),)
        self.assertEqual(question_route('geometry', 'optics', 'derived', bridge), 'eligible-for-domain-explanation')
        self.assertEqual(question_route('optics', 'geometry', 'derived', bridge), 'outside-declared-scope')

    def test_principle_not_proved_here(self):
        self.assertEqual(question_route('geometry', 'geometry', 'principle'), 'principle-not-proved-here')

    def test_foreign_does_not_become_true(self):
        self.assertEqual(question_route('geometry', 'geometry', 'foreign'), 'outside-declared-scope')

    def test_invalid_route(self):
        for args in [('', 'g', 'derived'), ('g', 'g', 'truth'), ('g', 'g', 'derived', ['bad'])]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                question_route(*args)

    def test_longitudinal_extension(self):
        self.assertIn(('d', 'a'), closure({'a', 'b', 'c', 'd'}, {('d', 'c'), ('c', 'b'), ('b', 'a')}))

    def test_lateral_extension(self):
        c = closure({'a', 'b', 'c', 'd', 'e'}, {('c', 'b'), ('b', 'a'), ('e', 'd'), ('d', 'a')})
        self.assertIn(('c', 'a'), c)
        self.assertIn(('e', 'a'), c)
        self.assertNotIn(('c', 'e'), c)

    def test_cycles_not_evidence(self):
        c = closure({'a', 'b'}, {('a', 'b'), ('b', 'a')})
        self.assertEqual(len(c), 4)

    def test_invalid_graph(self):
        with self.assertRaises(ValueError):
            closure({'a'}, {('a', 'b')})
        with self.assertRaises(ValueError):
            closure(set(), set())

    def test_finite_oracles(self):
        r = enumerate_models()
        for key in ('subset_oracle_mismatches', 'valid_chain_countermodels', 'two_way_inclusion_inequality_countermodels', 'closure_oracle_mismatches'):
            self.assertEqual(r[key], 0, key)
        self.assertGreater(r['shared_attribute_nonempty_countermodels'], 0)
        self.assertGreater(r['reverse_inclusion_nonempty_countermodels'], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
