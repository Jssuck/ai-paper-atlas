import unittest
from model import all_of, none_of, evaluate, object_oracle, enumerate_models, negative_models, examples

class ModelTests(unittest.TestCase):
    def test_subset_true(self): self.assertTrue(all_of(1,3))
    def test_subset_false(self): self.assertFalse(all_of(3,1))
    def test_empty_subject(self): self.assertTrue(all_of(0,0))
    def test_disjoint(self): self.assertTrue(none_of(1,2))
    def test_nondisjoint(self): self.assertFalse(none_of(3,2))
    def test_identity(self): self.assertTrue(evaluate(((1,1,1),))['necessary_ac'])
    def test_no_worlds(self):
        with self.assertRaises(ValueError): evaluate(())
    def test_bad_arity(self):
        with self.assertRaises(ValueError): evaluate(((1,1),))
    def test_bad_mask(self):
        with self.assertRaises(ValueError): evaluate(((4,1,1),))
    def test_negative_mask(self):
        with self.assertRaises(ValueError): evaluate(((-1,1,1),))
    def test_bool_mask(self):
        with self.assertRaises(ValueError): evaluate(((True,1,1),))
    def test_zero_domain(self):
        with self.assertRaises(ValueError): evaluate(((0,0,0),),0)
    def test_necessary_chain(self):
        r=evaluate(((3,1,1),(3,2,2)))
        self.assertTrue(r['necessary_ab'] and r['necessary_bc'] and r['necessary_ac'])
    def test_bridge_disappears(self):
        r=examples()['disappearing_bridge']['evaluation']
        self.assertTrue(r['actual_ab'] and r['actual_bc'] and r['necessary_ac'] and r['all_terms_nonempty'])
        self.assertFalse(r['necessary_ab']); self.assertFalse(r['necessary_bc'])
    def test_actual_only(self):
        r=examples()['actual_only_route']['evaluation']
        self.assertTrue(r['actual_ac']); self.assertFalse(r['necessary_ac'])
    def test_order_of_actual_world(self):
        a=evaluate(((1,1,1),(1,2,1))); b=evaluate(((1,2,1),(1,1,1)))
        self.assertNotEqual(a['actual_ab'],b['actual_ab'])
        self.assertEqual(a['necessary_ab'],b['necessary_ab'])
    def test_duplicate_world(self):
        self.assertEqual(evaluate(((3,1,1),)),evaluate(((3,1,1),(3,1,1))))
    def test_oracle_example(self): self.assertEqual(evaluate(((1,1,1),(1,2,1))),object_oracle(((1,1,1),(1,2,1))))
    def test_complete_enumeration(self):
        r=enumerate_models(); self.assertEqual(r['models'],4096); self.assertEqual(r['nonempty_models'],729)
        self.assertEqual(r['oracle_mismatches'],0); self.assertEqual(r['necessity_preservation_failures'],0)
        self.assertEqual(r['actual_preservation_failures'],0)
        self.assertGreater(r['nonempty_necessary_conclusion_contingent_route'],0)
        self.assertEqual(r['nonnecessary_conclusion_both_necessary_premises'],0)
    def test_two_negatives_underdetermine(self):
        r=negative_models(); self.assertEqual(r['triples'],512)
        for c in r['conclusions'].values(): self.assertGreater(c['true'],0); self.assertGreater(c['false'],0)
    def test_cause_not_represented(self):
        self.assertEqual(examples()['same_extension_different_explanation']['essential_or_causal_status'],'not represented; cannot be inferred')

if __name__=='__main__': unittest.main()
