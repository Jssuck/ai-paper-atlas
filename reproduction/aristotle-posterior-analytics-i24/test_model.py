import unittest
from model import subsets, restriction_census, closure, knowledge_example, geometry_examples, homonym_example, extension_not_cause

class TeachingTests(unittest.TestCase):
    def test_subsets_empty(self): self.assertEqual(subsets(0), [frozenset()])
    def test_subsets_three(self): self.assertEqual(len(set(subsets(3))), 8)
    def test_subsets_invalid(self):
        for n in (-1, 2.5, True):
            with self.assertRaises(ValueError): subsets(n)
    def test_census_invalid(self):
        for n in (-1, 7, True):
            with self.assertRaises(ValueError): restriction_census(n)
    def test_census_size(self): self.assertEqual(restriction_census(4)['assignments'], sum(8**n for n in range(5)))
    def test_forward_count(self): self.assertEqual(restriction_census(4)['forward_premise_cases'], sum(4**n for n in range(5)))
    def test_forward_sound(self): self.assertEqual(restriction_census(4)['forward_violations'], 0)
    def test_nonempty_converse(self):
        w = restriction_census(2)['first_nonempty_counterexample']
        self.assertTrue(set(w['S']) <= set(w['G']))
        self.assertTrue(set(w['S']) <= set(w['P']))
        self.assertFalse(set(w['G']) <= set(w['P']))
        self.assertTrue(w['S'])
    def test_closure_identity(self): self.assertEqual(closure({'x'}, []), frozenset({'x'}))
    def test_closure_chain(self): self.assertEqual(closure({'a'}, [({'a'}, 'b'), ({'b'}, 'c')]), frozenset('abc'))
    def test_closure_cycle(self): self.assertEqual(closure([], [({'a'}, 'b'), ({'b'}, 'a')]), frozenset())
    def test_closure_empty_premise(self): self.assertEqual(closure([], [(set(), 'a')]), frozenset('a'))
    def test_closure_conjunction(self): self.assertNotIn('c', closure({'a'}, [({'a','b'}, 'c')]))
    def test_knowledge_bridge(self):
        r=knowledge_example(); self.assertFalse(r['target_derivable_without_bridge']); self.assertTrue(r['target_derivable_with_bridge'])
    def test_explicit_not_closed(self):
        explicit={'a'}; self.assertNotIn('b', explicit); self.assertIn('b', closure(explicit,[({'a'},'b')])); self.assertEqual(explicit, {'a'})
    def test_triangle_not_polygon(self): self.assertEqual(geometry_examples()['interior_180_sides'], [3])
    def test_exterior_sum(self): self.assertTrue(geometry_examples()['all_exterior_360'])
    def test_homonym(self):
        r=homonym_example(); self.assertFalse(r['typed_machine_has_feathers']); self.assertTrue(r['collapsed_name_has_feathers'])
    def test_coextension_not_cause(self):
        r=extension_not_cause(); self.assertTrue(r['equal_extensions']); self.assertEqual(r['causal_status'],'undetermined')
    def test_closure_monotone_and_idempotent(self):
        rules=[({'a'},'b'),({'b','c'},'d')]
        small=closure({'a'},rules); large=closure({'a','c'},rules)
        self.assertLessEqual(small,large); self.assertEqual(closure(large,rules),large)

if __name__ == '__main__': unittest.main(verbosity=2)
