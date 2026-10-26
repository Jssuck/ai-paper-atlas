import unittest
from dataclasses import FrozenInstanceError
from model import Proof,CausalDefinition,to_definition,to_proof,conclusion,chain_report,nominal_lookup,enumerate_chains,enumerate_records

class TestRecords(unittest.TestCase):
    def setUp(self):self.p=Proof('S','M','A','law','observation')
    def test_roundtrip_proof(self):self.assertEqual(to_proof(to_definition(self.p)),self.p)
    def test_roundtrip_definition(self):
        d=to_definition(self.p);self.assertEqual(to_definition(to_proof(d)),d)
    def test_field_order(self):
        self.assertEqual(to_definition(self.p),CausalDefinition('S','A','M','observation','law'))
    def test_sources_retained(self):
        self.assertEqual((to_proof(to_definition(self.p)).major_source,to_proof(to_definition(self.p)).minor_source),('law','observation'))
    def test_projection_collision(self):
        q=Proof('S','N','A','other-law','other-observation')
        self.assertNotEqual(q,self.p);self.assertEqual(conclusion(q),conclusion(self.p))
    def test_source_collision(self):
        q=Proof('S','M','A','another','observation')
        self.assertNotEqual(q,self.p);self.assertEqual(conclusion(q),conclusion(self.p))
    def test_empty_term_rejected(self):
        with self.assertRaises(ValueError):Proof('','M','A','law','obs')
    def test_whitespace_source_rejected(self):
        with self.assertRaises(ValueError):Proof('S','M','A','  ','obs')
    def test_nonstring_rejected(self):
        with self.assertRaises(ValueError):CausalDefinition('S','A',2,'obs','law')
    def test_proof_type_guard(self):
        with self.assertRaises(TypeError):to_definition(('S','M','A'))
    def test_definition_type_guard(self):
        with self.assertRaises(TypeError):to_proof(self.p)
    def test_conclusion_type_guard(self):
        with self.assertRaises(TypeError):conclusion(to_definition(self.p))
    def test_immutable_record(self):
        with self.assertRaises(FrozenInstanceError):self.p.middle='N'
    def test_full_record_space(self):
        self.assertEqual(enumerate_records(),dict(records=108,conclusions=9,roundtrip_errors=0,preimages_per_conclusion=[12]))

class TestFiniteSemantics(unittest.TestCase):
    def setUp(self):self.p=Proof('S','M','A','given-major','given-minor')
    def report(self,s,m,a,u=(0,1,2)):return chain_report(self.p,u,{'S':s,'M':m,'A':a})
    def test_valid_chain(self):self.assertEqual(self.report({0},{0,1},{0,1,2}),dict(minor=True,major=True,conclusion=True,subject_exists=True))
    def test_empty_domain(self):self.assertEqual(self.report(set(),set(),set(),()),dict(minor=True,major=True,conclusion=True,subject_exists=False))
    def test_major_needed(self):self.assertFalse(self.report({0},{0},set())['conclusion'])
    def test_minor_needed(self):self.assertFalse(self.report({0},set(),set())['conclusion'])
    def test_true_conclusion_false_major(self):
        r=self.report({0},{0,1},{0});self.assertTrue(r['conclusion']);self.assertFalse(r['major'])
    def test_true_conclusion_false_minor(self):
        r=self.report({0},set(),{0});self.assertTrue(r['conclusion']);self.assertFalse(r['minor'])
    def test_different_middles_same_conclusion(self):
        r1=self.report({0},{0},{0,1});r2=self.report({0},{0,1},{0,1})
        self.assertTrue(r1['major'] and r1['minor'] and r2['major'] and r2['minor'])
        self.assertEqual(r1['conclusion'],r2['conclusion'])
    def test_outside_domain(self):
        with self.assertRaises(ValueError):self.report({5},{5},{5})
    def test_missing_term(self):
        with self.assertRaises(ValueError):chain_report(self.p,{0},{'S':{0}})
    def test_missing_name(self):self.assertIsNone(nominal_lookup('unlisted',{}))
    def test_nominal_does_not_require_instance(self):
        self.assertEqual(nominal_lookup('goat-stag',{'goat-stag':'a supplied compound phrase'}),'a supplied compound phrase')
        self.assertFalse(self.report(set(),set(),set())['subject_exists'])
    def test_bound_validation(self):
        for x in (-1,7,True,1.5):
            with self.assertRaises(ValueError):enumerate_chains(x)
    def test_independent_oracle_and_counts(self):
        self.assertEqual(enumerate_chains(),dict(total=4681,valid_chains=341,empty_subject_valid=121,transitivity_violations=0,oracle_disagreements=0))
    def test_labels_do_not_change_semantics(self):
        q=Proof('S','M','A','unverified-label','another-label')
        i={'S':{0},'M':{0},'A':{0}}
        self.assertEqual(chain_report(self.p,{0},i),chain_report(q,{0},i))

if __name__=='__main__':unittest.main()
