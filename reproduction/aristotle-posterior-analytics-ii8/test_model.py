import unittest
from model import subsets,chain,candidate_middles,DeclaredRole,report,binary_world,enumerate_chains

class Tests(unittest.TestCase):
    def test_empty_powerset(self): self.assertEqual(subsets(0),(frozenset(),))
    def test_powerset_count(self): self.assertEqual(len(subsets(4)),16)
    def test_negative_n(self):
        with self.assertRaises(ValueError): subsets(-1)
    def test_bool_n(self):
        with self.assertRaises(ValueError): subsets(True)
    def test_chain(self): self.assertTrue(chain({0},{0,1},{0,1,2})['premises'])
    def test_empty_chain(self): self.assertTrue(chain(set(),set(),set())['premises'])
    def test_empty_no_witness(self): self.assertFalse(bool(set()))
    def test_false_minor(self): self.assertFalse(chain({0},set(),{0})['minor'])
    def test_false_major(self): self.assertFalse(chain({0},{0,1},{0})['major'])
    def test_true_conclusion_false_premise(self):
        r=chain({0},set(),{0}); self.assertTrue(r['conclusion']); self.assertFalse(r['premises'])
    def test_reverse_fails(self): self.assertFalse({0,1}<={0})
    def test_multiple_middles(self):
        self.assertEqual(candidate_middles({0},{0,1,2},{'x':{0,1},'y':{0,2}}),('x','y'))
    def test_no_candidates(self): self.assertEqual(candidate_middles({0},{0},{}),())
    def test_reject_bad_candidate(self): self.assertEqual(candidate_middles({0},{0},{'bad':{1}}),())
    def test_same_extension_distinct_names(self):
        self.assertEqual(candidate_middles({0},{0},{'s':{0},'c':{0}}),('c','s'))
    def test_unknown_role(self): self.assertEqual(DeclaredRole('unknown',False,'teaching').role,'unknown')
    def test_bad_role(self):
        with self.assertRaises(ValueError): DeclaredRole('proved',True,'x')
    def test_bad_immediacy(self):
        with self.assertRaises(ValueError): DeclaredRole('cause',1,'x')
    def test_bad_source(self):
        with self.assertRaises(ValueError): DeclaredRole('cause',True,' ')
    def test_no_causal_upgrade(self):
        self.assertFalse(report({0},{0},{0},DeclaredRole('cause',True,'assumption'))['causal_truth_verified'])
    def test_no_essence_upgrade(self):
        self.assertFalse(report({0},{0},{0},DeclaredRole('cause',True,'assumption'))['essence_verified'])
    def test_role_does_not_change_truth(self):
        for role in ('sign','cause','unknown'):
            self.assertTrue(report({0},{0},{0},DeclaredRole(role,True,'x'))['premises'])
    def test_observations_equal(self):
        self.assertEqual([binary_world('directed',u) for u in (0,1)],[binary_world('common',u) for u in (0,1)])
    def test_do_zero(self): self.assertNotEqual(binary_world('directed',1,0),binary_world('common',1,0))
    def test_do_one(self): self.assertNotEqual(binary_world('directed',0,1),binary_world('common',0,1))
    def test_compatible_intervention(self): self.assertEqual(binary_world('directed',1,1),binary_world('common',1,1))
    def test_bad_kind(self):
        with self.assertRaises(ValueError): binary_world('other',0)
    def test_bad_u(self):
        with self.assertRaises(ValueError): binary_world('directed',2)
    def test_bad_do(self):
        with self.assertRaises(ValueError): binary_world('common',0,2)
    def test_enumeration(self):
        r=enumerate_chains();self.assertEqual(r['triples'],4681);self.assertEqual(r['valid_chains'],341)
        self.assertEqual(r['transitivity_violations'],0);self.assertEqual(r['oracle_differences'],0)

if __name__=='__main__': unittest.main(verbosity=2)
