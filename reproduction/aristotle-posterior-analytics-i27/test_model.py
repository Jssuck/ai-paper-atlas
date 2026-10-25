import unittest
from itertools import product
from model import (scm, causal_summary, forget_positions, first_distance,
                   position_summary, closure, horn_summary, prediction_summary, results)

class TeachingTests(unittest.TestCase):
    def test_natural_equivalence(self):
        for u in (0, 1): self.assertEqual(scm('direct', u), scm('common', u))
    def test_direct_intervention(self):
        for u, x in product((0,1), repeat=2): self.assertEqual(scm('direct', u, x), (x,x))
    def test_common_intervention(self):
        for u, x in product((0,1), repeat=2): self.assertEqual(scm('common', u, x), (x,u))
    def test_intervention_differences(self): self.assertEqual(causal_summary()['intervention_disagreements'],2)
    def test_invalid_model(self):
        with self.assertRaises(ValueError): scm('bad',0)
    def test_invalid_u(self):
        with self.assertRaises(ValueError): scm('direct',2)
    def test_invalid_do(self):
        with self.assertRaises(ValueError): scm('common',0,2)
    def test_forget_equivalent(self): self.assertEqual(forget_positions((0,0)), forget_positions((0,1)))
    def test_distance_witness(self): self.assertNotEqual(first_distance((0,0)), first_distance((0,1)))
    def test_distance_requires_pair(self):
        with self.assertRaises(ValueError): first_distance((1,))
    def test_label_count_preserved(self): self.assertEqual(forget_positions((2,0,1)), (0,1,2))
    def test_positions_count(self): self.assertEqual(position_summary()['configurations'],120)
    def test_ambiguous_fibers(self): self.assertEqual(position_summary()['ambiguous_distance_fibers'],3)
    def test_empty_closure(self): self.assertEqual(closure(set(), [('a','b')]), set())
    def test_chain(self): self.assertEqual(closure({'a'}, [('a','c'),('c','b')]), {'a','b','c'})
    def test_cycle_terminates(self): self.assertEqual(closure({'a'}, [('a','b'),('b','a')]), {'a','b'})
    def test_seed_preserved(self): self.assertEqual(closure({'a'}, []), {'a'})
    def test_horn_enumeration(self):
        h=horn_summary();self.assertEqual(h['rule_configurations'],64)
        self.assertEqual(h['conservative_at_fixed_seed'],24)
        self.assertEqual(h['nonconservative_at_fixed_seed'],40)
        self.assertEqual(h['old_conclusion_loss_cases'],0)
    def test_predictions(self):
        p=prediction_summary();self.assertEqual(p['simple_mse'],'1/2');self.assertEqual(p['richer_mse'],'0')
    def test_output_sections(self): self.assertEqual(set(results()), {'causal','positions','horn','prediction'})

if __name__ == '__main__': unittest.main(verbosity=2)
