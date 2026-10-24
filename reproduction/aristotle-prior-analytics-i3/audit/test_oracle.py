import unittest
from independent_oracle import formula, worlds, check
class IndependentChecks(unittest.TestCase):
    def test_model_counts(self):
        self.assertEqual([sum(1 for _ in worlds(n,w)) for n in range(1,4) for w in (1,2)], [4,16,16,256,64,4096])
    def test_cross_world_witness(self):
        s=[frozenset({0}),frozenset({1})]
        self.assertTrue(formula('dc','N','I',s,s))
        self.assertFalse(formula('dr','N','I',s,s))
    def test_constant_interpretation_collapse(self):
        for s,p in worlds(3,1):
            for scope in ('dc','dr'):
                for k in 'AEIO':
                    a=formula(scope,'N',k,s*2,p*2)
                    self.assertEqual(a,formula(scope,'P',k,s*2,p*2))
                    # Universal de re contingency is vacuously true for an empty
                    # actual subject; this is not contingency of a whole sentence.
                    self.assertEqual(formula(scope,'C',k,s*2,p*2), scope == 'dr' and k in 'AE' and not s[0])
    def test_negation_duality(self):
        for s,p in worlds(2,2):
            self.assertEqual(formula('dc','P','E',s,p), not formula('dc','N','I',s,p))
            self.assertEqual(formula('dc','P','O',s,p), not formula('dc','N','A',s,p))
    def test_all_counts_and_witnesses(self):
        result=check()
        self.assertEqual(result['models'],4452)
        self.assertEqual(result['count_fields_compared'],60)
        self.assertEqual(result['mismatches'],0)
if __name__=='__main__': unittest.main(verbosity=2)
