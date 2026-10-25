import unittest
from model import all_of, none_of, certificate, witness_trace, implication, diagnose, background_models, subsets, run

class Tests(unittest.TestCase):
    def test_all_direction(self):
        self.assertTrue(all_of({0, 1}, {0}))
        self.assertFalse(all_of({0}, {0, 1}))
    def test_none_symmetric(self):
        self.assertEqual(none_of({0}, {1}), none_of({1}, {0}))
    def test_empty_overlap(self):
        self.assertTrue(all_of({1}, set()))
        self.assertTrue(none_of({1}, set()))
    def test_direct(self):
        self.assertTrue(certificate({2}, {0,1}, {0})['direct_valid'])
    def test_reductio(self):
        self.assertTrue(certificate({1}, {0,1}, {0})['reductio_valid'])
    def test_overstrong(self):
        v=certificate({1}, {0,1}, {0})
        self.assertTrue(v['reductio_background'])
        self.assertTrue(v['not_all_b_are_a'])
        self.assertFalse(v['tempting_universal_negative'])
    def test_no_empty_contradiction(self):
        v=certificate({0}, {0}, set())
        self.assertFalse(v['reductio_background'])
        self.assertFalse(v['not_all_b_are_a'])
    def test_witness(self):
        self.assertEqual(witness_trace({2},{0,1},{0},0),dict(in_c=True,in_b=True,in_a=False,intersection_witness=False))
    def test_bad_witness(self):
        with self.assertRaises(ValueError): witness_trace({2},{0},{0},1)
    def test_bad_background(self):
        with self.assertRaises(ValueError): witness_trace({0},{0},{0},0)
    def test_set_type(self):
        with self.assertRaises(TypeError): certificate([],set(),set())
    def test_proposition_type(self):
        with self.assertRaises(TypeError): implication(1,True,False)
    def test_rule(self):
        self.assertFalse(implication(True,True,False))
        self.assertTrue(implication(False,True,False))
    def test_fixed_q(self):
        self.assertTrue(diagnose(q=True,r=False)['not_p_supported'])
    def test_missing_q(self):
        self.assertFalse(diagnose(r=False)['not_p_supported'])
    def test_wrong_blame(self):
        self.assertIn(dict(p=True,q=False,r=False),background_models(r=False))
    def test_inconsistent(self):
        self.assertEqual(diagnose(p=True,q=True,r=False)['status'],'inconsistent_background')
        self.assertIsNone(diagnose(p=True,q=True,r=False)['not_p_supported'])
    def test_fact_type(self):
        with self.assertRaises(TypeError): diagnose(q=1)
    def test_subsets(self):
        self.assertEqual(len(subsets(3)),8)
        self.assertEqual(subsets(0),[frozenset()])
        with self.assertRaises(ValueError): subsets(True)
    def test_run_bounds(self):
        with self.assertRaises(ValueError): run(-1)
        with self.assertRaises(ValueError): run(6)
    def test_enumeration(self):
        result=run()
        self.assertEqual(result['totals']['assignments'],4681)
        for key in ('direct_counterexamples','reductio_counterexamples','witness_violations'):
            self.assertEqual(result['totals'][key],0)
        self.assertGreater(result['totals']['overstrong_counterexamples'],0)
        self.assertTrue(all(r['reductio_valid'] for r in result['truth_rows']))

if __name__=='__main__': unittest.main()
