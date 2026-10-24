"""Executable checks remain active with Python -O and -OO."""
import unittest
from example_transfer import subset, observed, guarantees_target, exhaustive, examples

class TransferTests(unittest.TestCase):
    def test_subset_direction(self):
        self.assertTrue(subset(1,3)); self.assertFalse(subset(3,1))
    def test_empty_subset(self):
        self.assertTrue(subset(0,0)); self.assertTrue(subset(0,7))
    def test_observation_does_not_transfer(self):
        self.assertTrue(observed(1,3,2,1)); self.assertFalse(subset(2,1))
    def test_shared_class_not_universal(self):
        self.assertTrue(observed(1,3,2,1)); self.assertFalse(subset(3,1))
    def test_nonempty_sample_witness(self):
        self.assertTrue(observed(3,5,4,1)); self.assertTrue(3&5)
    def test_empty_sample_no_witness(self):
        self.assertTrue(observed(0,0,0,0)); self.assertFalse(0&0)
    def test_drop_sample_property(self):
        self.assertFalse(observed(0,1,1,1)); self.assertFalse(0&1)
    def test_drop_sample_classification(self):
        self.assertFalse(observed(1,0,0,1)); self.assertFalse(1&0)
    def test_drop_target_classification(self):
        self.assertTrue(subset(1,1)); self.assertFalse(subset(2,1))
    def test_target_coverage_not_class_coverage(self):
        self.assertTrue(guarantees_target(1,1,3)); self.assertFalse(subset(7,1))
    def test_empty_target_guaranteed(self):
        self.assertTrue(guarantees_target(0,0,3))
    def test_missing_target_counterproperty(self):
        c,d=6,3
        self.assertFalse(guarantees_target(c,d,3)); self.assertFalse(subset(c,d))
        self.assertTrue(subset(d,d)); self.assertFalse(subset(c,d))
    def test_two_examples_not_coverage(self):
        self.assertTrue(observed(3,7,4,1)); self.assertTrue(observed(3,7,4,2))
        self.assertFalse(guarantees_target(4,1|2,3))
    def test_union_target_covered(self):
        self.assertTrue(guarantees_target(3,1|2,3))
    def test_invalid_bound(self):
        for value in (-1,5,'4',True,False,4.0,None):
            with self.assertRaises(ValueError): exhaustive(value)
    def test_full_counts_and_zero_failures(self):
        r=exhaustive(4)['counts']
        self.assertEqual(r['worlds'],69905); self.assertEqual(r['bridge_pairs'],341)
        for k in ('existential_failures','deductive_failures','coverage_failures','bridge_equivalence_failures'):
            self.assertEqual(r[k],0)
        self.assertGreater(r['target_failures'],0); self.assertGreater(r['universal_failures'],0)
    def test_example_certificates(self):
        data=examples(); self.assertEqual(len(data),8)
        self.assertTrue(data[0]['observed']); self.assertFalse(data[0]['all_C_is_A'])
        self.assertFalse(data[-1]['target_guaranteed_over_all_A'])

if __name__ == '__main__': unittest.main(verbosity=2)
