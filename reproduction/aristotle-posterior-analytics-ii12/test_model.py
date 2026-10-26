import unittest
from fractions import Fraction
from model import *

class ModelTests(unittest.TestCase):
    def test_house_backward(self): self.assertEqual(closure({'house'},HOUSE_RULES),set(NODES))
    def test_stones_no_forward(self): self.assertEqual(closure({'stones'},HOUSE_RULES),{'stones'})
    def test_empty(self): self.assertEqual(closure(set(),HOUSE_RULES),set())
    def test_idempotent(self): self.assertEqual(closure(closure({'house'},HOUSE_RULES),HOUSE_RULES),set(NODES))
    def test_cycle_needs_seed(self): self.assertEqual(closure(set(),(('house','stones'),('stones','house'))),set())
    def test_cycle_seed(self): self.assertEqual(closure({'house'},(('house','stones'),('stones','house'))),{'house','stones'})
    def test_unknown_seed(self): self.assertRaises(ValueError,closure,{'unknown'},HOUSE_RULES)
    def test_unknown_rule(self): self.assertRaises(ValueError,closure,set(),(('x','house'),))
    def test_valid_house(self): self.assertTrue(valid_trace(dict(zip(NODES,(0,1,2)))))
    def test_stones_only(self): self.assertTrue(valid_trace(dict(zip(NODES,(0,None,None)))))
    def test_missing_predecessor(self): self.assertFalse(valid_trace(dict(zip(NODES,(None,1,2)))))
    def test_simultaneous_invalid(self): self.assertFalse(valid_trace(dict(zip(NODES,(0,0,1)))))
    def test_time_reversal(self): self.assertFalse(valid_trace(dict(zip(NODES,(2,1,0)))))
    def test_bad_time(self): self.assertRaises(ValueError,valid_trace,dict(zip(NODES,(-1,None,None))))
    def test_bad_keys(self): self.assertRaises(ValueError,valid_trace,{'house':1})
    def test_before_house(self): self.assertEqual(completed(dict(zip(NODES,(0,1,2))),1),{'stones','foundation'})
    def test_dense_midpoint(self): self.assertEqual(midpoint(Fraction(1,3),Fraction(2,3)),Fraction(1,2))
    def test_bad_interval(self): self.assertRaises(ValueError,midpoint,1,1)
    def test_cycle_tokens_distinct(self): self.assertNotEqual(cycle_tokens(4)[0],cycle_tokens(4)[4])
    def test_cycle_type_repeats(self): self.assertEqual(cycle_tokens(4)[0][1],cycle_tokens(4)[4][1])
    def test_bad_cycle_length(self): self.assertRaises(ValueError,cycle_tokens,-1)
    def test_majority_counterexample(self):
        c,b,a={0},{0,1,2},{1,2}
        self.assertTrue(majority(c,b)); self.assertTrue(majority(b,a)); self.assertFalse(majority(c,a))
    def test_majority_empty(self): self.assertFalse(majority(set(),set()))
    def test_majority_half(self): self.assertFalse(majority({0,1},{0}))
    def test_exhaustive(self):
        r=experiments()
        self.assertEqual(r['graph_instances'],512); self.assertEqual(r['oracle_mismatches'],0)
        self.assertEqual(r['traces'],64); self.assertEqual(r['completed_backward_errors'],0)
        self.assertEqual(r['subset_triples'],585); self.assertEqual(r['universal_errors'],0)
        self.assertGreater(r['majority_counterexamples'],0); self.assertEqual(r['midpoint_errors'],0)

if __name__=='__main__': unittest.main()
