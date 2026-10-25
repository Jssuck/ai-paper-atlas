import unittest
from model import *

class ModelTests(unittest.TestCase):
    def test_closure(self):
        self.assertEqual(strict_closure(3,[(0,1),(1,2)]),frozenset({(0,1),(1,2),(0,2)}))
    def test_cycle_rejected(self):
        with self.assertRaises(ValueError): strict_closure(2,[(0,1),(1,0)])
    def test_self_rejected(self):
        with self.assertRaises(ValueError): strict_closure(1,[(0,0)])
    def test_outside_rejected(self):
        with self.assertRaises(ValueError): strict_closure(2,[(0,2)])
    def test_negative_size(self):
        with self.assertRaises(ValueError): strict_closure(-1,[])
    def test_empty_order(self): self.assertEqual(strict_closure(0,[]),frozenset())
    def test_no_common_middle(self):
        r=strict_closure(3,[(0,2),(1,2)])
        self.assertEqual(common_middles(3,r,0,1,2),())
    def test_common_middle(self):
        r=strict_closure(4,[(0,2),(1,2),(2,3)])
        self.assertEqual(common_middles(4,r,0,1,3),(2,))
    def test_inside_excludes_endpoints(self):
        r=strict_closure(3,[(0,1),(1,2)])
        self.assertEqual(inside(3,r,0,2),(1,))
    def test_one_middle_two_premises(self): self.assertEqual(chain_counts((0,1,2)),{'terms':3,'internal_terms':1,'adjacent_premises':2})
    def test_direct_zero_middle(self): self.assertEqual(chain_counts((0,1))['internal_terms'],0)
    def test_bad_count(self):
        with self.assertRaises(ValueError): chain_counts((0,))
    def test_refinement(self):
        r=strict_closure(4,[(0,1),(1,2),(2,3)])
        self.assertEqual(len(refinement_states(4,r,0,3)),4)
    def test_saturated(self):
        r=strict_closure(3,[(0,1),(1,2)])
        self.assertEqual(refinements(3,r,(0,1,2)),())
    def test_bad_chain(self):
        with self.assertRaises(ValueError): refinements(3,frozenset(),(0,2))
    def test_empty_felapton(self):
        values=rule_values({0},{0},set())
        self.assertEqual(values['Felapton_nonempty_M'],(False,False))
    def test_baroco_not_universal(self):
        s,p,m={0,1},{0},{0}
        self.assertEqual(rule_values(s,p,m)['Baroco'],(True,True))
        self.assertTrue(s&p)
    def test_bocardo(self): self.assertEqual(rule_values({0,1},{0},{1})['Bocardo'],(True,True))
    def test_enumeration_rules(self):
        x=enumerate_rules();self.assertEqual(x['assignments'],4681)
        for item in x['rules'].values():self.assertEqual(item['counterexamples'],0)
    def test_enumeration_orders(self):
        x=enumerate_orders();self.assertEqual(x['generated_dags'],75)
        self.assertEqual(x['counting_violations'],0);self.assertEqual(x['insertion_violations'],0)
        self.assertGreater(x['without_internal_common_middle'],0)

if __name__=='__main__':unittest.main()
