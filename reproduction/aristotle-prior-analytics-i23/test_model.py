import unittest
from model import Model, all_models, entails, skeleton, check_chain, raa_certificate, parity_probe

class Tests(unittest.TestCase):
    def test_nonempty_domain(self):
        with self.assertRaises(ValueError): Model(('P','M','S'),0)
    def test_bool_mask(self):
        with self.assertRaises(ValueError): Model(('P',),True)
    def test_invalid_names(self):
        for ts in (['P'],('P','P'),('',),('P',1),()):
            with self.assertRaises(ValueError): Model(ts,1)
    def test_bad_masks(self):
        for x in (-1,4,1.0,'1',None):
            with self.assertRaises(ValueError): Model(('P',),x)
    def test_unknown_term(self):
        with self.assertRaises(ValueError): Model(('P',),1).extension('Q')
    def test_bad_quality(self):
        with self.assertRaises(ValueError): Model(('P',),1).holds('', 'P','P')
    def test_empty_subject(self):
        m=Model(('P','S'),1)
        self.assertTrue(m.holds('A','P','S'));self.assertTrue(m.holds('E','P','S'))
        self.assertFalse(m.holds('I','P','S'));self.assertFalse(m.holds('O','P','S'))
    def test_all_counts(self):
        self.assertEqual(len(list(all_models())),255)
        self.assertEqual(len(list(all_models(require_nonempty_terms=True))),218)
    def test_policy_bool(self):
        with self.assertRaises(ValueError): list(all_models(require_nonempty_terms=1))
    def test_barbara(self):
        self.assertEqual(entails((('A','P','M'),('A','M','S')),('A','P','S')),(True,None))
    def test_bad_common_predicate(self):
        self.assertFalse(entails((('A','M','P'),('A','M','S')),('A','P','S'))[0])
    def test_existence(self):
        ps=(('A','P','M'),('A','S','M'))
        self.assertFalse(entails(ps,('I','P','S'))[0])
        self.assertTrue(entails(ps,('I','P','S'),True)[0])
    def test_four_skeletons(self):
        for e,n in [((('S','M'),('M','P')),'chain_forward'),((('P','M'),('M','S')),'chain_reverse'),((('S','M'),('P','M')),'common_predicate'),((('M','S'),('M','P')),'common_subject')]:
            self.assertEqual(skeleton(e),n);self.assertEqual(skeleton(e[::-1]),n)
    def test_bad_skeleton(self):
        for x in ((),(('S','M'),('S','M')),(('S','P'),('P','M')),(('S','S'),('M','P'))):
            with self.assertRaises(ValueError): skeleton(x)
    def test_chain(self):
        self.assertEqual(check_chain(Model(('S','C','M','P'),1<<15),('S','C','M','P')),{'premises':True,'conclusion':True})
    def test_invalid_chain(self):
        with self.assertRaises(ValueError): check_chain(Model(('P','S'),1),('S','S'))
    def test_raa_not_proof(self):
        r=raa_certificate(Model(('P','S'),1<<3),('A','P','S'),('O','P','S'),('A','P','S'))
        self.assertTrue(r['contradictory_pair']);self.assertFalse(r['outer_discharge_verified'])
        self.assertFalse(r['assumption_true']);self.assertTrue(r['derived_true'])
    def test_parity(self):
        r=parity_probe(20);self.assertEqual(r['reduced_solutions'],[]);self.assertFalse(r['general_irrationality_proved'])
    def test_bad_limit(self):
        for x in (0,True,1.0,1001):
            with self.assertRaises(ValueError): parity_probe(x)
    def test_bad_propositions(self):
        for ps in ((),['A'],(('X','P','S'),)):
            with self.assertRaises(ValueError): entails(ps,('A','P','S'))

if __name__=='__main__': unittest.main(verbosity=2)
