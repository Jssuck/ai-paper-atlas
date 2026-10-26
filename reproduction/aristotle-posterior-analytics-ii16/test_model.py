"""Explicit unittest checks remain active under -O and -OO."""
import unittest
from model import Model, orientations, exhaustive_syllogism, examples

class Tests(unittest.TestCase):
    def test_syllogism_all_three_object_models(self):
        self.assertEqual(exhaustive_syllogism(), {'universe_size':3,'assignments':512,'premise_satisfying':64,'conclusion_violations':0})
    def test_one_object_syllogism(self):
        self.assertEqual(exhaustive_syllogism(1)['premise_satisfying'],4)
    def test_reverse_not_automatic(self):
        e=examples()['one_way']; self.assertTrue(e['C_to_A']); self.assertFalse(e['A_to_B']); self.assertEqual(e['A_not_B'],['other'])
    def test_reverse_with_extra_premise(self):
        m=Model({1,2},{'A':{1},'B':{1},'C':{1}})
        self.assertTrue(m.implies('C','A') and m.implies('A','B') and m.implies('C','B'))
    def test_equal_extensions_do_not_select_orientation(self):
        m=Model({1,2},{'A':{1},'B':{1}})
        self.assertEqual(orientations(m,'A','B'),(('A','B'),('B','A')))
    def test_orientation_demo_requires_equality(self):
        with self.assertRaises(ValueError): orientations(Model({1},{'A':{1},'B':set()}),'A','B')
    def test_alternative_sufficient_routes(self):
        e=examples()['alternatives']; self.assertTrue(e['B_to_A'] and e['C_to_A']); self.assertEqual(e['A_not_B'],['c_only']); self.assertEqual(e['A_not_C'],['b_only'])
    def test_routes_need_not_exhaust_effect(self):
        m=Model({1,2,3},{'B':{1},'C':{2},'A':{1,2,3},'union':{1,2}})
        self.assertTrue(m.implies('B','A') and m.implies('C','A')); self.assertFalse(m.implies('A','union'))
    def test_restricted_equivalence(self):
        e=examples()['restriction']; self.assertTrue(e['A_equals_TS'] and e['S_to_A_in_T']); self.assertEqual(e['unrestricted_S_not_A'],['non_tree_s'])
    def test_unknown_predicate(self):
        with self.assertRaises(KeyError): Model({1},{'A':{1}}).implies('A','missing')
    def test_outside_universe(self):
        with self.assertRaises(ValueError): Model({1},{'A':{2}})
    def test_outside_domain(self):
        with self.assertRaises(ValueError): Model({1},{'A':{1}}).implies('A','A',{2})
    def test_invalid_name(self):
        with self.assertRaises(ValueError): Model({1},{'':{1}})
    def test_input_snapshot(self):
        s={1}; d={'A':s}; m=Model({1,2},d); s.add(2); d['B']={2}; self.assertEqual(m.extension('A'),frozenset({1})); self.assertNotIn('B',m.predicates)
    def test_mapping_read_only(self):
        m=Model({1},{'A':{1}})
        with self.assertRaises(TypeError): m.predicates['A']=frozenset()
    def test_empty_antecedent_is_vacuous(self):
        self.assertTrue(Model({1},{'A':set(),'B':{1}}).implies('A','B'))
    def test_empty_universe(self):
        self.assertTrue(Model(set(),{'A':set(),'B':set()}).coextensive('A','B')); self.assertEqual(exhaustive_syllogism(0)['assignments'],1)
    def test_empty_restriction(self):
        self.assertTrue(Model({1},{'A':{1},'B':set()}).implies('A','B',set()))
    def test_invalid_enumeration_size(self):
        for n in (-1,5,True,1.5):
            with self.subTest(n=n), self.assertRaises(ValueError): exhaustive_syllogism(n)

if __name__=='__main__': unittest.main()
