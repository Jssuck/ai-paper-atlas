import unittest
from model import Proof, shapes, label, tree_experiment, subset, disjoint, set_experiment, cost_example, counterexamples
class Tests(unittest.TestCase):
 def test_leaf_A(self): self.assertEqual(Proof('A').leaves(),('A',))
 def test_leaf_E(self): self.assertEqual(Proof('E').leaves(),('E',))
 def test_AA(self): self.assertEqual(Proof('A',(Proof('A'),Proof('A'))).leaves(),('A','A'))
 def test_EA(self): self.assertEqual(Proof('E',(Proof('E'),Proof('A'))).leaves(),('E','A'))
 def test_AE(self): self.assertEqual(Proof('E',(Proof('A'),Proof('E'))).leaves(),('A','E'))
 def test_reject_EE(self):
  with self.assertRaises(ValueError): Proof('E',(Proof('E'),Proof('E'))).validate()
 def test_reject_A_from_E(self):
  with self.assertRaises(ValueError): Proof('A',(Proof('E'),Proof('A'))).validate()
 def test_reject_E_from_AA(self):
  with self.assertRaises(ValueError): Proof('E',(Proof('A'),Proof('A'))).validate()
 def test_reject_unary(self):
  with self.assertRaises(ValueError): Proof('A',(Proof('A'),)).validate()
 def test_reject_label(self):
  with self.assertRaises(ValueError): Proof('X').validate()
 def test_catalan(self): self.assertEqual([len(shapes(i)) for i in range(7)],[1,1,2,5,14,42,132])
 def test_invalid_shape_count(self):
  with self.assertRaises(ValueError): shapes(-1)
 def test_invalid_leaf_index(self):
  with self.assertRaises(ValueError): label(None,1)
 def test_tree_invariant(self): self.assertEqual(sum(x['violations'] for x in tree_experiment()),0)
 def test_tree_counts(self):
  r=tree_experiment();self.assertEqual(sum(x['affirmative_proofs'] for x in r),197);self.assertEqual(sum(x['negative_proofs'] for x in r),1275)
 def test_empty_sets(self): self.assertTrue(subset(0,0));self.assertTrue(disjoint(0,0))
 def test_subset_direction(self): self.assertTrue(subset(1,3));self.assertFalse(subset(3,1))
 def test_set_counts(self):
  r=set_experiment();self.assertEqual(r['direct_celarent']['assignments'],4681);self.assertEqual(r['expanded_celarent']['assignments'],33825);self.assertEqual(sum(x['counterexamples'] for x in r.values()),0)
 def test_two_negatives(self):
  r=counterexamples()['two_negative_premises'];self.assertTrue(r['premises_true']);self.assertFalse(r['claimed_negative_conclusion'])
 def test_redundant(self):
  r=counterexamples()['redundant_negative_premise'];self.assertTrue(r['premises_true']);self.assertTrue(r['conclusion_true']);self.assertEqual(r['negative_assumptions_listed'],2)
 def test_cost_condition(self):
  r=cost_example();self.assertLess(r['equal_unit_cost']['short'],r['equal_unit_cost']['long']);self.assertGreater(r['unequal_cost']['short'],r['unequal_cost']['long'])
if __name__=='__main__': unittest.main(verbosity=2)
