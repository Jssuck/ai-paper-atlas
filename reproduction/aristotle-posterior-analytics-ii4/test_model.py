"""Explicit unittest checks survive Python -O and -OO."""
import unittest
from itertools import product
from model import Premise, ROLES, classify_chain, compose, enumerate_chains, independent_oracle

class TestModel(unittest.TestCase):
    def setUp(self):
        self.eq = {'C': {0}, 'B': {0}, 'A': {0}}
    def pair(self, lo='attribute', hi='attribute', low_sources=('minor',)):
        return (Premise('C', 'B', lo, low_sources), Premise('B', 'A', hi, ('major',)))
    def test_strict_chain(self):
        self.assertEqual(classify_chain({0}, {0,1}, {0,1,2}),
                         {'chain': True, 'conclusion': True, 'endpoints_equal': False, 'all_equal': False})
    def test_broken_chain(self):
        self.assertFalse(classify_chain({0}, {1}, {1,2})['chain'])
    def test_false_conclusion(self):
        self.assertFalse(classify_chain({0}, {1}, {1})['conclusion'])
    def test_empty_domain(self):
        self.assertTrue(classify_chain([], [], [])['all_equal'])
    def test_sandwich(self):
        self.assertTrue(classify_chain({0,1}, {0,1}, {0,1})['all_equal'])
    def test_bad_maximum(self):
        for x in (-1,7,True,1.5):
            with self.assertRaises(ValueError): enumerate_chains(x)
    def test_counts(self):
        r = enumerate_chains()
        self.assertEqual(r['triples'], sum(8**n for n in range(5)))
        self.assertEqual(r['chains'], sum(4**n for n in range(5)))
        self.assertEqual(r['equal_endpoint_chains'], sum(2**n for n in range(5)))
        self.assertEqual(r['nonempty_c_chains'], sum(4**n-3**n for n in range(5)))
        self.assertEqual(r['nonempty_equal_endpoint_chains'], sum(2**n-1 for n in range(5)))
        self.assertEqual(r['transitivity_failures'], 0)
        self.assertEqual(r['sandwich_failures'], 0)
    def test_independent_oracle(self):
        for n in range(5): self.assertEqual(enumerate_chains(n), independent_oracle(n))
    def test_equal_extension_no_promotion(self):
        self.assertEqual(compose(*self.pair(), self.eq)['declared_result_role'], 'attribute')
    def test_essential_part_not_definition(self):
        self.assertEqual(compose(*self.pair('essential_part','essential_part'), self.eq)['declared_result_role'], 'essential_part')
    def test_all_role_pairs(self):
        for a,b in product(ROLES, repeat=2):
            r = compose(*self.pair(a,b), self.eq)
            self.assertEqual(r['declared_result_role'], ROLES[min(ROLES.index(a), ROLES.index(b))])
            self.assertFalse(r['actual_essence_certified'])
    def test_full_definition_presupposition(self):
        r=compose(*self.pair('full_definition','full_definition'), self.eq)
        self.assertEqual(r['declared_result_role'],'full_definition')
        self.assertTrue(r['minor_already_declares_subject_definition'])
    def test_source_union(self):
        r=compose(*self.pair(low_sources=('minor','major')),self.eq)
        self.assertEqual(r['sources'], ['major','minor'])
    def test_explicit_target_dependency(self):
        self.assertTrue(compose(*self.pair(low_sources=('target:C-definition',)),self.eq)['explicit_target_dependency'])
        self.assertFalse(compose(*self.pair(),self.eq)['explicit_target_dependency'])
    def test_role_validation(self):
        with self.assertRaises(ValueError): self.pair('truth')
    def test_source_validation(self):
        for s in ((), ['minor'], ('',)):
            with self.assertRaises(ValueError): self.pair(low_sources=s)
    def test_term_validation(self):
        with self.assertRaises(ValueError): Premise('', 'A', 'attribute', ('x',))
    def test_middle_mismatch(self):
        with self.assertRaises(ValueError): compose(Premise('C','X','attribute',('x',)), self.pair()[1],self.eq)
    def test_missing_and_false_extension(self):
        with self.assertRaises(ValueError): compose(*self.pair(), {'C':{0}})
        with self.assertRaises(ValueError): compose(*self.pair(), {'C':{0},'B':{1},'A':{1}})
    def test_full_definition_minimum(self):
        with self.assertRaises(ValueError): compose(*self.pair('full_definition'), {'C':{0},'B':{0,1},'A':{0,1}})
        self.assertEqual(compose(*self.pair('essential_part','essential_part'), {'C':{0},'B':{0,1},'A':{0,1,2}})['declared_result_role'], 'essential_part')
    def test_bad_record_and_target(self):
        with self.assertRaises(TypeError): compose(None, self.pair()[1], self.eq)
        with self.assertRaises(ValueError): compose(*self.pair(), self.eq, target_source='')

if __name__ == '__main__': unittest.main(verbosity=2)
