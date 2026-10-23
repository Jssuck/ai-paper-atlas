import unittest
import reproduce as r

class ModelTests(unittest.TestCase):
    def test_model_counts(self):
        self.assertEqual([len(r.models(p)) for p in ('empty_allowed','all_nonempty','B_nonempty')],[255,218,240])
    def test_contradictories(self):
        for m in r.models():
            for k in r.KINDS:
                self.assertNotEqual(r.truth(m,(k,'A','B')),r.truth(m,(r.NEG[k],'A','B')))
    def test_empty_subject(self):
        self.assertEqual([r.truth([0],(k,'A','B')) for k in r.KINDS],[True,True,False,False])
    def test_candidate_count(self):
        self.assertEqual(len(r.candidates('empty_allowed')),64)
    def test_four_original_routes(self):
        for c in r.named_checks()[:4]:
            self.assertTrue(c['valid']); self.assertGreater(c['premise_models'],0)
    def test_existence_sensitivity(self):
        cs={c['name']:c for c in r.named_checks()}
        for q in ('I','O'):
            self.assertFalse(cs[q+'_with_universal_background']['valid'])
            self.assertTrue(cs[q+'_with_B_exists']['valid'])
    def test_wrong_strength(self):
        for c in r.named_checks()[8:11]: self.assertFalse(c['valid'])
    def test_wrong_universal_hypothesis_needs_existence(self):
        cs={c['name']:c for c in r.named_checks()}
        self.assertFalse(cs['wrong_E_internal_needs_B']['valid'])
        self.assertTrue(cs['wrong_E_internal_with_B_exists']['valid'])
        self.assertFalse(cs['wrong_U_internal_needs_B']['valid'])
        self.assertTrue(cs['wrong_U_internal_with_B_exists']['valid'])
        self.assertFalse(cs['O_target_does_not_refute_I']['valid'])
        self.assertFalse(cs['two_existentials_different_witnesses']['valid'])
    def test_coexistence(self):
        self.assertTrue(r.truth([2,7],('I','A','B')))
        self.assertTrue(r.truth([2,7],('O','A','B')))
    def test_countermodel_replay(self):
        for policy in ('empty_allowed','all_nonempty'):
            for row in r.candidates(policy):
                for key, ps, c in [('internal',[row['hypothesis'],row['other']],row['result']),('external',[row['other'],row['known']],row['target'])]:
                    m=row[key]['minimal_countermodel']
                    if m is not None:
                        self.assertTrue(all(r.truth(m,p) for p in ps)); self.assertFalse(r.truth(m,c))
    def test_certificates_require_consistency(self):
        for row in r.candidates('empty_allowed'):
            if row['certificate']:
                self.assertGreater(row['internal']['premise_models'],0)
                self.assertGreater(row['external']['premise_models'],0)
                self.assertTrue(row['internal']['valid']); self.assertTrue(row['external']['valid'])
    def test_invalid_input(self):
        for m in ([],[8],[True],[0,0], 'abc'):
            with self.assertRaises(ValueError):r.truth(m,('U','A','B'))
        for p in (('X','A','B'),('U','D','B'),('U','A'),('','A','B'),(None,'A','B'),('U',[], 'B')):
            with self.assertRaises(ValueError):r.truth([0],p)
        for policy in ('unknown', [], None, True):
            with self.assertRaises(ValueError):r.models(policy)
        with self.assertRaises(ValueError):r.entailment(None, ('U','A','B'))
        # Invalid conclusion must not be hidden by inconsistent premises.
        with self.assertRaises(ValueError):r.entailment([('I','A','B'),('E','A','B')], ('X','A','B'))
    def test_minimal_witness_order(self):
        ms=r.models()
        self.assertEqual(ms, sorted(ms,key=lambda m:(len(m),m)))
        for c in r.named_checks():
            w=c['minimal_countermodel']
            if w is not None:
                for m in r.models(c['policy']):
                    if list(m)==w:break
                    self.assertFalse(all(r.truth(m,p) for p in c['premises']) and not r.truth(m,c['conclusion']))

if __name__=='__main__':unittest.main()
