import unittest
from model import Slice, relation, summarize, event_summary, continuation, enumerate_models

F = frozenset
class TemporalTests(unittest.TestCase):
    def test_chain(self):
        self.assertEqual(relation(Slice(F({0,1}), F({0}), F({0}))), (True, True, True))
    def test_empty_predicates(self):
        self.assertEqual(relation(Slice(F(), F(), F())), (True, True, True))
    def test_major_failure(self):
        self.assertEqual(relation(Slice(F(), F({0}), F({0}))), (False, True, False))
    def test_minor_failure(self):
        self.assertEqual(relation(Slice(F(), F(), F({0}))), (True, False, False))
    def test_true_conclusion_does_not_certify_premises(self):
        self.assertEqual(relation(Slice(F({0}), F({1}), F({0}))), (False, False, True))
    def test_snapshot_not_global(self):
        good = Slice(F({0}), F({0}), F({0}))
        bad = Slice(F(), F({0}), F({0}))
        self.assertTrue(all(relation(good)))
        self.assertFalse(summarize((good,bad))['conclusion_all'])
    def test_failure_premise_can_vary_by_time(self):
        summary = summarize((Slice(F(),F({0}),F({0})), Slice(F(),F(),F({0}))))
        self.assertEqual(summary['premise_failure_times'], {'major':[0], 'minor':[1]})
        self.assertEqual(summary['conclusion_failure_times'], [0,1])
    def test_empty_horizon_rejected(self):
        with self.assertRaises(ValueError): summarize(())
    def test_event_condition_without_permanence(self):
        self.assertEqual(event_summary((False,True,False),(False,True,False)),
                         {'conditional_all':True,'event_all':False,'event_some':True,'trigger_some':True})
    def test_vacuity_not_existence(self):
        summary = event_summary((False,False),(False,False))
        self.assertTrue(summary['conditional_all'])
        self.assertFalse(summary['event_some'])
    def test_trigger_not_sufficient_if_law_false(self):
        self.assertFalse(event_summary((True,),(False,))['conditional_all'])
    def test_wrong_lengths_rejected(self):
        with self.assertRaises(ValueError): event_summary((True,), (True,False))
    def test_empty_event_rejected(self):
        with self.assertRaises(ValueError): event_summary((),())
    def test_boolean_validation(self):
        with self.assertRaises(ValueError): event_summary((1,), (True,))
    def test_equal_prefixes(self):
        for t in range(8):
            self.assertEqual(continuation((True,)*8,True,t),continuation((True,)*8,False,t))
    def test_future_divergence(self):
        self.assertTrue(continuation((True,)*8,True,8))
        self.assertFalse(continuation((True,)*8,False,8))
    def test_index_validation(self):
        for t in (-1,1.5,True):
            with self.assertRaises(ValueError): continuation((),True,t)
    def test_enumeration(self):
        r = enumerate_models(); m=r['temporal_models']
        self.assertEqual(m['traces'],4096)
        for k in ('oracle_mismatches','preservation_failures','contrapositive_failures'):
            self.assertEqual(m[k],0)
        self.assertGreater(m['snapshot_upgrade_counterexamples'],0)
        self.assertEqual(r['event_cases'],64)
        self.assertEqual(r['event_oracle_mismatches'],0)

if __name__ == '__main__': unittest.main(verbosity=2)
