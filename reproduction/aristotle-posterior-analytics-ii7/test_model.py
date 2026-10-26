import unittest
from model import *
from run_all import run

class Tests(unittest.TestCase):
    def test_empty_domain(self): self.assertTrue(coextensive([],[],[]))
    def test_empty_predicates_nonempty_domain(self): self.assertTrue(coextensive([0],[],[]))
    def test_empty_not_inhabited(self): self.assertFalse(witness_valid([0],[],0))
    def test_equal_nonempty(self): self.assertTrue(coextensive([0,1],[1],[1]))
    def test_different(self): self.assertFalse(coextensive([0,1],[0],[1]))
    def test_witness_present(self): self.assertTrue(witness_valid([0],[0],0))
    def test_witness_outside_domain(self): self.assertFalse(witness_valid([0],[0],1))
    def test_bad_predicate(self):
        with self.assertRaises(ValueError): coextensive([0],[1],[])
    def test_bad_second_predicate(self):
        with self.assertRaises(ValueError): coextensive([0],[],[1])
    def test_transfer(self): self.assertTrue(transfer_witness([0],[0],[0],0))
    def test_transfer_needs_eq(self): self.assertFalse(transfer_witness([0,1],[0],[0,1],1))
    def test_transfer_needs_witness(self): self.assertFalse(transfer_witness([0],[],[],0))
    def test_partial_observation(self): self.assertTrue(observations_agree([0,1],[0],[0],[0,1]))
    def test_full_observation(self): self.assertFalse(observations_agree([0,1],[0,1],[0],[0,1]))
    def test_no_observations(self): self.assertTrue(observations_agree([0],[],[],[0]))
    def test_bad_observation(self):
        with self.assertRaises(ValueError): observations_agree([0],[1],[],[])
    def test_valid_binding(self): self.assertTrue(binding_valid({'x':'f'},NameClaim('x','f')))
    def test_wrong_binding(self): self.assertFalse(binding_valid({'x':'g'},NameClaim('x','f')))
    def test_missing_binding(self): self.assertFalse(binding_valid({},NameClaim('x','f')))
    def test_name_type(self):
        with self.assertRaises(TypeError): binding_valid({},NameClaim(1,'f'))
    def test_named_witness(self): self.assertTrue(named_witness([0],{'f':{0}},{'x':'f'},NameClaim('x','f'),0))
    def test_named_empty(self): self.assertFalse(named_witness([0],{'f':set()},{'x':'f'},NameClaim('x','f'),0))
    def test_named_wrong(self): self.assertFalse(named_witness([0],{'f':{0}},{'x':'g'},NameClaim('x','f'),0))
    def test_missing_formula(self): self.assertFalse(named_witness([0],{}, {'x':'f'},NameClaim('x','f'),0))
    def test_duplicate_members(self): self.assertTrue(coextensive([0],[0,0],[0]))
    def test_subsets(self): self.assertEqual(len(subsets(3)),8)
    def test_bad_n(self):
        with self.assertRaises(ValueError): subsets(-1)
    def test_exhaustive(self): self.assertEqual(run()['counts']['oracle_mismatches'],0)

if __name__=='__main__': unittest.main()
