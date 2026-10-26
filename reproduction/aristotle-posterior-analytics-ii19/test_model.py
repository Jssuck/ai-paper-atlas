import unittest
from model import analyse, compatible_explanations, group_memories


class ModelTests(unittest.TestCase):
    def test_empty_domain(self):
        r = analyse([], [])
        self.assertEqual((r['compatible_count'], r['universal_true_count'], r['status']), (1, 1, 'certified_finite_domain'))
    def test_no_observation(self):
        self.assertEqual(analyse(['a','b'], [])['compatible_count'], 4)
    def test_one_positive(self):
        self.assertEqual(analyse(['a','b'], [('a',True)])['status'], 'underdetermined')
    def test_repeated_positive(self):
        r = analyse(['a','b'], [('a',True)] * 100)
        self.assertEqual((r['observation_count'],r['covered_count'],r['compatible_count']), (100,1,2))
    def test_negative_refutes(self):
        r=analyse(['a','b'], [('a',False)])
        self.assertEqual((r['universal_true_count'],r['universal_false_count'],r['status']), (0,2,'refuted'))
    def test_complete_positive(self):
        self.assertEqual(analyse(['a','b'], [('a',True),('b',True)])['status'], 'certified_finite_domain')
    def test_complete_negative(self):
        self.assertEqual(analyse(['a','b'], [('a',False),('b',False)])['compatible_count'],1)
    def test_mixed_complete(self):
        r=analyse(['a','b'], [('a',True),('b',False)])
        self.assertEqual((r['status'], r['compatible_count']), ('refuted',1))
    def test_order_invariance(self):
        self.assertEqual(analyse(['a','b'], [('a',True),('b',False)]),analyse(['b','a'], [('b',False),('a',True)]))
    def test_conflict_rejected(self):
        with self.assertRaises(ValueError): analyse(['a'], [('a',True),('a',False)])
    def test_outside_rejected(self):
        with self.assertRaises(ValueError): analyse(['a'], [('b',True)])
    def test_empty_domain_observation_rejected(self):
        with self.assertRaises(ValueError): analyse([], [('a',True)])
    def test_duplicate_domain_rejected(self):
        with self.assertRaises(ValueError): analyse(['a','a'], [])
    def test_integer_label_rejected(self):
        with self.assertRaises(ValueError): analyse(['a'], [('a',1)])
    def test_missing_label_rejected(self):
        with self.assertRaises(ValueError): analyse(['a'], [('a',)])
    def test_bad_domain_name_rejected(self):
        with self.assertRaises(ValueError): analyse([''], [])
    def test_positive_formula(self):
        r=analyse(list('abcde'), [('a',True),('c',True)])
        self.assertEqual((r['compatible_count'],r['universal_true_count'],r['universal_false_count']), (8,1,7))
    def test_explicit_opposite_completions(self):
        hs=compatible_explanations(['a','b'], [('a',True)])
        self.assertEqual(hs, [{'a':True,'b':False},{'a':True,'b':True}])
    def test_repeat_negative(self):
        r=analyse(['a','b'], [('a',False)]*7)
        self.assertEqual((r['covered_count'],r['universal_true_count']), (1,0))
    def test_group_fixed_classes(self):
        g=group_memories(list('abc'), [('a',True),('a',True),('b',True)], {'a':'X','b':'X','c':'Y'})
        self.assertEqual(g, {'X':{'memory_count':3,'objects':['a','b']}})
    def test_class_map_incomplete_rejected(self):
        with self.assertRaises(ValueError): group_memories(['a','b'], [], {'a':'X'})
    def test_class_map_extra_rejected(self):
        with self.assertRaises(ValueError): group_memories(['a'], [], {'a':'X','b':'Y'})
    def test_no_memory_groups(self):
        self.assertEqual(group_memories(['a'], [], {'a':'X'}), {})
    def test_input_not_mutated(self):
        u=['a','b']; obs=[('a',True)]
        analyse(u,obs)
        self.assertEqual((u,obs), (['a','b'], [('a',True)]))

if __name__ == '__main__': unittest.main()
